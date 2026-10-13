"""lib/shop_corporate.py — corporate orders the SHOPS handle (Sales popover, "Shop corporate" tab).

Corporate clients are quoted in Odoo Sales (sale_order, S0…) and then pay at a shop till, so
these orders never reach the Denri Corporate app. Per client this works out what was quoted,
what has been paid at the tills (when, where, how), the balance still owed, and which shop
"hunted" the client:

  1. Quote / invoice in the Corporate app        → left out (counted there, never twice).
  2. Lead in the Corporate app                   → Corporate, even if a shop took the money.
  3. Paid or part-paid                           → the shop whose till took the money.
  4. Not paid yet → shop named on the quote note → shop where the client bought before
                    (same customer, phone or email) → the client's town.
  5. None of these                               → Corporate (not in any shop's totals).

Matching rules (the data has no shared key):
  • Quotes of one client are grouped by Odoo customer, name, phone, work-email domain or
    acronym (ESK COMPANY = Economists Society of Kenya). Repeat quotes within 25% of each
    other's amount are versions of one order — only the confirmed / latest one counts.
  • Till receipts belong to a client by customer, phone, email, work-email domain (the
    ELITE TRAVEL till customer ↔ @elitetravel.co.ke) or a multi-word name, from 14 days
    before the first quote. A bulk receipt (≥50 bags) within 0.5% of an unpaid quote's
    amount is matched to it too (flagged "matched by amount").
  • A refunded receipt never counts. A bulk till order (100+ bags) with no quote still
    shows, flagged "no quote in Odoo".
"""

from __future__ import annotations

import datetime as _dt
import re
from difflib import SequenceMatcher

from lib import db

# Product lines that aren't bags (fees, branding, delivery…), same spirit as the POS rules.
_NON_BAG = r"(fee|delivery|embroid|branding|logo|origination|sample|strap|sponsor|customi[sz])"

# Tills that aren't Kenyan retail shops: other countries, internal and channel tills.
_NOT_SHOP = {"SINZA", "DAR-ES-ALAM", "UGANDA", "UGANDDA", "STAFF POS", "REJECTS", "MARKETING", "SHOOT"}
_SHOP_NAME = {"WEBSITE SALES": "Website", "KTDA SHOP": "KTDA", "STARMALL": "Star Mall",
              "HILTON SHOP": "Hilton", "FLASH SALE HILTON": "Hilton", "FLASH SALE MOMBASA": "Mombasa",
              "CORPORATE SALES": "Corporate"}

_GENERIC_MAIL = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "ymail.com",
                 "live.com", "aol.com", "protonmail.com", "yahoo.co.uk", "me.com", "mail.com"}
_LEGAL = {"ltd", "limited", "plc", "company", "co", "inc", "llc", "llp"}
_STOP = _LEGAL | {"the", "of", "and", "kenya", "ke"}


def shop_label(raw: str) -> str:
    raw = (raw or "").upper().strip()
    return _SHOP_NAME.get(raw, raw.title())


def _txt(v) -> str:
    return "" if v is None or v != v else str(v)


def _tokens(s: str, drop=_STOP) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", _txt(s).lower()) if t not in drop]


def _squash(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", _txt(s).lower())


def _phone9(*vals) -> set[str]:
    out = set()
    for v in vals:
        d = re.sub(r"\D", "", _txt(v))
        if len(d) >= 9:
            out.add(d[-9:])
    return out


def _domain(email: str) -> str:
    e = _txt(email).lower().strip()
    if "@" not in e:
        return ""
    d = e.split("@", 1)[1]
    return "" if d in _GENERIC_MAIL else d


def _acronym(a: str, b: str) -> bool:
    """'ESK COMPANY' is the acronym of 'Economists Society of Kenya'."""
    ta = _tokens(a, _LEGAL)
    tb = [t for t in re.findall(r"[a-z0-9]+", _txt(b).lower()) if t not in _LEGAL | {"of", "the", "and"}]
    return len(ta) == 1 and 2 <= len(ta[0]) <= 5 and len(tb) >= 2 and "".join(t[0] for t in tb) == ta[0]


def same_name(a: str, b: str) -> bool:
    ta, tb = set(_tokens(a)), set(_tokens(b))
    if not ta or not tb:
        return False
    if ta == tb:
        return True
    small, big = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    if len(small) >= 2 and small <= big:
        return True
    sa, sb = _squash(a), _squash(b)
    if min(len(sa), len(sb)) >= 8 and sa[:3] == sb[:3]:
        m = SequenceMatcher(None, sa, sb)
        if m.real_quick_ratio() >= 0.9 and m.quick_ratio() >= 0.9 and m.ratio() >= 0.9:
            return True
    return _acronym(a, b) or _acronym(b, a)


# ── queries ───────────────────────────────────────────────────
_LOCAL = "(({c}) AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date"

QUOTES_SQL = f"""
SELECT so.id, so.name, {_LOCAL.format(c='so.date_order')} AS d, {_LOCAL.format(c='so.create_date')} AS created,
       so.state, ROUND(so.amount_total)::bigint AS kes,
       so.partner_id AS pid, rp.commercial_partner_id AS cpid, rp.name AS cust,
       rp.phone, rp.mobile, rp.email, rp.city,
       regexp_replace(COALESCE(so.note::text, ''), '<[^>]+>', ' ', 'g') AS note, up.name AS sp,
       (SELECT COALESCE(SUM(l.product_uom_qty), 0) FROM sale_order_line l
          LEFT JOIN product_product pp ON pp.id = l.product_id
          LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
         WHERE l.order_id = so.id AND l.display_type IS NULL
           AND COALESCE(pt.name::text, l.name, '') !~* '{_NON_BAG}') AS bags
FROM sale_order so
LEFT JOIN res_partner rp ON rp.id = so.partner_id
LEFT JOIN res_users u ON u.id = so.user_id LEFT JOIN res_partner up ON up.id = u.partner_id
WHERE so.state <> 'cancel' AND so.amount_total > 0
  AND {_LOCAL.format(c='so.date_order')} BETWEEN :s AND :e
"""

TILL_SQL = f"""
WITH o AS (
    SELECT p.id, p.name, p.date_order, p.partner_id, p.session_id, p.user_id, p.amount_total
    FROM pos_order p
    WHERE p.date_order >= :s0 AND p.date_order < :e1 AND p.partner_id IS NOT NULL
      AND p.state IN ('done', 'paid', 'invoiced')
), bags AS (
    SELECT l.order_id, SUM(CASE WHEN COALESCE(l.full_product_name, pt.name::text, '') !~* '{_NON_BAG}'
                                THEN l.qty ELSE 0 END) AS bags
    FROM pos_order_line l JOIN o ON o.id = l.order_id
    LEFT JOIN product_product pp ON pp.id = l.product_id
    LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
    GROUP BY 1
), pays AS (
    SELECT pay.pos_order_id, STRING_AGG(DISTINCT pm.name::text, ' + ') AS paid_by
    FROM pos_payment pay JOIN o ON o.id = pay.pos_order_id
    JOIN pos_payment_method pm ON pm.id = pay.payment_method_id
    GROUP BY 1
)
SELECT o.id, o.name AS receipt, {_LOCAL.format(c='o.date_order')} AS d, UPPER(pc.name) AS shop,
       o.partner_id AS pid, rp.commercial_partner_id AS cpid, rp.name AS cust, rp.phone, rp.mobile, rp.email,
       ROUND(o.amount_total)::bigint AS kes, cp.name AS cashier, COALESCE(bags.bags, 0) AS bags, pays.paid_by
FROM o
JOIN res_partner rp ON rp.id = o.partner_id
LEFT JOIN pos_session ps ON ps.id = o.session_id LEFT JOIN pos_config pc ON pc.id = ps.config_id
LEFT JOIN res_users u ON u.id = o.user_id LEFT JOIN res_partner cp ON cp.id = u.partner_id
LEFT JOIN bags ON bags.order_id = o.id LEFT JOIN pays ON pays.pos_order_id = o.id
"""   # refunds ("<receipt> REFUND") come back too; build() drops them and the receipts they refund

# Any-time till history of the unpaid clients, for "the shop where the client bought before".
PAST_SQL = """
SELECT UPPER(pc.name) AS shop, p.partner_id AS pid, rp.commercial_partner_id AS cpid,
       rp.phone, rp.mobile, LOWER(rp.email) AS email
FROM pos_order p JOIN res_partner rp ON rp.id = p.partner_id
LEFT JOIN pos_session ps ON ps.id = p.session_id LEFT JOIN pos_config pc ON pc.id = ps.config_id
WHERE p.amount_total > 0 AND (
      rp.commercial_partner_id = ANY(CAST(:cpids AS int[]))
   OR RIGHT(regexp_replace(COALESCE(rp.phone, ''),  '\\D', '', 'g'), 9) = ANY(CAST(:phones AS text[]))
   OR RIGHT(regexp_replace(COALESCE(rp.mobile, ''), '\\D', '', 'g'), 9) = ANY(CAST(:phones AS text[]))
   OR LOWER(rp.email) = ANY(CAST(:emails AS text[])))
"""

CORP_APP_SQL = """
SELECT 'quote' AS kind, q.name AS ref, q.company, NULL::text AS phone FROM denri_corporate_quote q
 WHERE q.status::text NOT IN ('cancelled', 'declined') AND q.date_quote >= :s
UNION ALL
SELECT 'invoice', i.name, i.company, i.contact_phone FROM denri_corporate_invoice i
 WHERE i.status::text <> 'cancelled' AND i.date_invoice >= :s
"""

LEADS_SQL = """
SELECT l.name, l.phone, l.phone2, l.email, l.create_date::date AS created, up.name AS owner
FROM denri_corporate_lead l
LEFT JOIN res_users u ON u.id = l.user_id LEFT JOIN res_partner up ON up.id = u.partner_id
WHERE COALESCE(l.active, TRUE)
"""

SHOPS_SQL = "SELECT DISTINCT UPPER(name) AS shop FROM pos_config"


# ── helpers ───────────────────────────────────────────────────
class _UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, i):
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def _d(v) -> str:
    """date → '12 Oct'."""
    return f"{v.day} {v.strftime('%b')}" if v else ""


def _rows(df):
    return [] if df is None else df.to_dict("records")


def _versions(quotes: list[dict]) -> tuple[list[dict], list[str]]:
    """Repeat quotes within 25% of each other's amount are one order: keep a confirmed one,
    else the latest. Returns (kept, merged-away quote numbers)."""
    kept, merged = [], []
    for q in sorted(quotes, key=lambda q: (q["d"], q["name"])):
        twin = next((k for k in kept if abs(k["kes"] - q["kes"]) <= 0.25 * max(k["kes"], q["kes"])), None)
        if twin is None:
            kept.append(q)
            continue
        if twin["state"] == "sale" and q["state"] != "sale":
            merged.append(q["name"])                 # keep the confirmed one
        else:
            merged.append(twin["name"])
            kept[kept.index(twin)] = q
    return kept, merged


def build(today: _dt.date | None = None) -> dict | None:
    """Everything the "Shop corporate" tab needs, or None when the DB isn't reachable."""
    today = today or _dt.date.today()
    start = (today.replace(day=1) - _dt.timedelta(days=1)).replace(day=1)   # start of last month
    p = {"s": start.isoformat(), "e": today.isoformat(),
         "s0": (start - _dt.timedelta(days=14)).isoformat(), "e1": (today + _dt.timedelta(days=2)).isoformat()}

    quotes = db.run_query(QUOTES_SQL, p)
    till = db.run_query(TILL_SQL, p)
    if quotes is None or till is None:
        return None
    quotes, till = _rows(quotes), _rows(till)
    corp_app = _rows(db.run_query(CORP_APP_SQL, p))
    leads = _rows(db.run_query(LEADS_SQL))
    shops = [s for s in (r["shop"] for r in _rows(db.run_query(SHOPS_SQL))) if s and s not in _NOT_SHOP]

    for q in quotes:
        q["phones"] = _phone9(q["phone"], q["mobile"])
        q["dom"] = _domain(q["email"])
        q["kes"] = int(q["kes"] or 0)

    # 1) group quotes into clients
    uf = _UF(len(quotes))
    for i, a in enumerate(quotes):
        for j in range(i):
            b = quotes[j]
            if (a["cpid"] == b["cpid"] or same_name(a["cust"], b["cust"]) or (a["phones"] & b["phones"])
                    or (a["dom"] and a["dom"] == b["dom"])):
                uf.union(i, j)
    groups: dict[int, list[dict]] = {}
    for i, q in enumerate(quotes):
        groups.setdefault(uf.find(i), []).append(q)

    clients = []
    for qs in groups.values():
        kept, merged = _versions(qs)
        latest = max(kept, key=lambda q: q["d"])
        clients.append({
            "quotes": kept, "merged": merged, "name": latest["cust"],
            "names": {q["cust"] for q in qs}, "pids": {q["pid"] for q in qs}, "cpids": {q["cpid"] for q in qs},
            "phones": set().union(*(q["phones"] for q in qs)), "doms": {q["dom"] for q in qs if q["dom"]},
            "emails": {_txt(q["email"]).lower() for q in qs if _txt(q["email"])},
            "city": next((_txt(q["city"]) for q in qs if _txt(q["city"])), ""),
            "notes": " ".join(_txt(q["note"]) for q in qs),
            "first": min(min(q["d"], q["created"] or q["d"]) for q in qs),
            "quotedKes": sum(q["kes"] for q in kept), "quotedBags": int(sum(q["bags"] or 0 for q in kept)),
            "pays": [], "flags": [],
        })

    # 2) till receipts → clients
    def owns(c, t):
        if t["d"] < c["first"] - _dt.timedelta(days=14):
            return False
        if t["pid"] in c["pids"] or t["cpid"] in c["cpids"]:
            return True
        if _phone9(t["phone"], t["mobile"]) & c["phones"]:
            return True
        em = _txt(t["email"]).lower()
        if em and (em in c["emails"] or (_domain(em) and _domain(em) in c["doms"])):
            return True
        if t["sq"] and any(t["sq"] == d.split(".")[0] for d in c["doms"]):
            return True
        # name match only for multi-word names ("BENARD" alone is anybody) that share a word
        return any(len(_tokens(n)) >= 2 and (t["tok"] & set(_tokens(n))) and same_name(t["cust"], n)
                   for n in c["names"])

    refunded = {_txt(t["receipt"])[:-len(" REFUND")] for t in till if _txt(t["receipt"]).endswith(" REFUND")}
    loose = []
    for t in till:
        t["kes"], t["bags"] = int(t["kes"] or 0), int(t["bags"] or 0)
        t["sq"], t["tok"] = _squash(t["cust"]), set(_tokens(t["cust"]))
        if (t["shop"] in _NOT_SHOP or t["kes"] <= 0 or t["d"] > today
                or _txt(t["receipt"]).endswith(" REFUND") or t["receipt"] in refunded):
            continue
        c = next((c for c in clients if owns(c, t)), None)
        if c:
            c["pays"].append(t)
        else:
            loose.append(t)

    # bulk receipt ≈ an unpaid quote's amount → that quote (customer saved under another name)
    for t in sorted(loose, key=lambda t: -t["kes"]):
        if t["bags"] < 50 or t["kes"] < 100_000:
            continue
        c = next((c for c in clients if not c["pays"] and c["quotedKes"]
                  and abs(t["kes"] - c["quotedKes"]) <= 0.005 * c["quotedKes"] and t["d"] >= c["first"]), None)
        if c:
            c["pays"].append(t)
            c["flags"].append(f'matched by amount (till: "{_txt(t["cust"]).strip()}")')
            t["used"] = True

    # bulk till orders with no quote at all
    by_cust: dict = {}
    for t in loose:
        if not t.get("used") and t["bags"] >= 100 and t["d"] >= start:
            by_cust.setdefault(t["cpid"], []).append(t)
    for ts in by_cust.values():
        clients.append({"quotes": [], "merged": [], "name": _txt(ts[0]["cust"]).strip(), "names": {ts[0]["cust"]},
                        "pids": set(), "cpids": set(), "phones": set(), "doms": set(), "emails": set(),
                        "city": "", "notes": "", "first": min(t["d"] for t in ts),
                        "quotedKes": 0, "quotedBags": 0, "pays": ts, "flags": ["no quote in Odoo"]})

    # 3) Corporate app: quotes/invoices → left out; leads → hunted by Corporate
    lead_rows = [(l, _phone9(l["phone"], l["phone2"]), _txt(l["email"]).lower(),
                  set(_tokens(l["name"])), _squash(l["name"])[:3]) for l in leads]

    def _maybe(n, tok, pre):          # cheap pre-check before the full same_name()
        nt = set(_tokens(n))
        return bool(nt & tok) or _squash(n)[:3] == pre or len(_tokens(n, _LEGAL)) == 1
    rows, left_out = [], []
    past_needed = []
    for c in clients:
        clash = next((a for a in corp_app if any(same_name(n, a["company"]) for n in c["names"])
                      or (_phone9(a["phone"]) & c["phones"])), None)
        if clash:
            left_out.append({"client": c["name"], "quotes": [q["name"] for q in c["quotes"]], "kes": c["quotedKes"],
                             "ref": f'{clash["ref"]} ({clash["company"]})'})
            continue
        c["lead"] = next((l for l, ph, em, tok, pre in lead_rows
                          if (ph & c["phones"]) or (em and em in c["emails"])
                          or any(_maybe(n, tok, pre) and same_name(n, l["name"]) for n in c["names"])), None)
        c["paid"] = sum(t["kes"] for t in c["pays"])
        if not c["lead"] and not c["paid"]:
            past_needed.append(c)
        rows.append(c)

    # 4) "bought there before" for unpaid clients (any time)
    past = []
    if past_needed:
        past = _rows(db.run_query(PAST_SQL, {
            "cpids": sorted({int(x) for c in past_needed for x in c["cpids"] if x == x and x is not None}),
            "phones": sorted({ph for c in past_needed for ph in c["phones"]}),
            "emails": sorted({e for c in past_needed for e in c["emails"]})}))

    shop_re = [(s, re.compile(r"\b" + re.escape(shop_label(s)) + r"\b", re.I)) for s in shops
               if shop_label(s) != "Corporate"]
    out = []
    for c in rows:
        pays = sorted(c["pays"], key=lambda t: t["d"])
        paid, quoted = c["paid"], c["quotedKes"]
        status = "paid" if (paid and (not quoted or paid >= 0.99 * quoted)) else ("part" if paid else "unpaid")
        paid_shop = ""
        if pays:
            per = {}
            for t in pays:
                per[shop_label(t["shop"])] = per.get(shop_label(t["shop"]), 0) + t["kes"]
            paid_shop = max(per, key=per.get)
        top = max(pays, key=lambda t: t["kes"]) if pays else None
        if c["lead"]:
            hunted, how = "Corporate", f'Corporate app lead {_d(c["lead"]["created"])}' + (
                f' · {c["lead"]["owner"]}' if _txt(c["lead"]["owner"]) else "")
        elif paid:
            hunted, how = paid_shop, "paid there" + (f' · {top["cashier"]}' if top and _txt(top["cashier"]) else "")
        else:
            hunted, how = "", ""
            hit = next((shop_label(s) for s, rx in shop_re if rx.search(c["notes"])), None)
            if hit:
                hunted, how = hit, "named on the quote note"
            if not hunted:
                seen = {}
                for r in past:
                    if r["shop"] in _NOT_SHOP:
                        continue
                    why = ("same customer" if r["cpid"] in c["cpids"] else
                           "same phone" if _phone9(r["phone"], r["mobile"]) & c["phones"] else
                           "same email" if _txt(r["email"]) in c["emails"] else None)
                    if why:
                        k = shop_label(r["shop"])
                        seen[k] = (seen.get(k, (0, why))[0] + 1, why)
                if seen:
                    k = max(seen, key=lambda k: seen[k][0])
                    hunted, how = k, f"bought there before ({seen[k][1]})"
            if not hunted and c["city"]:
                hit = next((shop_label(s) for s, rx in shop_re if rx.fullmatch(c["city"].strip())), None)
                if hit:
                    hunted, how = hit, "client's town"
            if not hunted:
                hunted, how = "Corporate", "no shop link"
        latest_q = max((q["d"] for q in c["quotes"]), default=None)
        out.append({
            "client": c["name"].strip(),
            "quotes": [{"no": q["name"], "on": _d(q["d"]), "kes": q["kes"], "state": q["state"],
                        "by": _txt(q["sp"])} for q in sorted(c["quotes"], key=lambda q: q["d"])],
            "merged": sorted(c["merged"]),
            "quotedKes": quoted, "quotedBags": c["quotedBags"],
            "paidKes": paid, "bags": sum(t["bags"] for t in pays),
            "balance": max(quoted - paid, 0), "status": status,
            "payments": [{"receipt": t["receipt"], "on": _d(t["d"]), "shop": shop_label(t["shop"]), "kes": t["kes"],
                          "by": _txt(t["paid_by"]), "cashier": _txt(t["cashier"]), "cust": _txt(t["cust"]).strip()}
                         for t in pays],
            "hunted": hunted, "how": how,
            "paidAt": paid_shop if hunted != paid_shop else "",
            "age": (today - latest_q).days if latest_q and status == "unpaid" else None,
            "flags": c["flags"],
        })

    order = {"paid": 0, "part": 1, "unpaid": 2}
    out.sort(key=lambda r: (order[r["status"]], -(r["paidKes"] if r["status"] != "unpaid" else r["balance"])))

    summary: dict[str, dict] = {}
    for r in out:
        s = summary.setdefault(r["hunted"], {"shop": r["hunted"], "paid": 0, "bags": 0, "owed": 0, "clients": 0})
        s["paid"] += r["paidKes"]; s["bags"] += r["bags"]; s["owed"] += r["balance"]; s["clients"] += 1
    shops_out = sorted((s for s in summary.values() if s["shop"] != "Corporate"), key=lambda s: -(s["paid"] + s["owed"]))
    if "Corporate" in summary:
        shops_out.append(summary["Corporate"])

    months = start.strftime("%b") + ("–" + today.strftime("%b") if today.month != start.month else "")
    return {"rows": out, "shops": shops_out, "leftOut": left_out, "period": months,
            "asOf": _d(today)}


if __name__ == "__main__":                                   # quick check: python -m lib.shop_corporate
    import json
    res = build()
    print(json.dumps(res, indent=1, default=str)[:6000] if res else "DB not reachable")
