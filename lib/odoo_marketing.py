"""lib/odoo_marketing.py — marketing data the Odoo "Marketing OS" app keeps (spec: docs/odoo-marketing-audit.md).

  wa_clicks_by_bag(start, end)   website "order on WhatsApp" taps per bag (denri_marketing_wa_click, from 23 Oct 2026)
  followers_daily()              Facebook / Instagram followers, new follows, reach, views per day (denri_meta_account_day)
  website_weekly(country)        the weekly website snapshot (GA4 sessions, carts, checkouts, orders, WhatsApp orders)
  meta_posts_by_bag(start, end)  Facebook + Instagram posts per bag, from the bag tags marketing adds in Odoo
  website_till_by_payment(s, e)  WEBSITE SALES till per Mon–Sun week: orders / bags / KES paid on the site (Pesapal)
                                 vs paid to the M-Pesa till (orders taken by people on WhatsApp / phone)

Every function returns an empty result if Postgres is unreachable, so pages never fail on it.
"""
from __future__ import annotations

import re

from lib import db

WEBSITE_TILL = "WEBSITE SALES"
# Website (Shopify) titles that don't start with the bag's own name.
WA_ALIAS = {"LAPTOP BACKPACK FOR SCHOOL": "CODE 3", "ANKARA LAPTOP BACKPACK": "CODE 4 ANKARA", "STANDARD TRAVEL": "TRAVEL",
            "ANKARA DESIGN": "ANKARA TRAVEL", "PATTERN BABY BAG": "BABY BAG", "WAIST BELT BAG": "BELT BAG"}


def _q(sql, params=None):
    try:
        df = db.run_query(sql, params or {})
    except Exception as ex:                                  # noqa: BLE001
        print(f"  Odoo marketing data unavailable ({ex})")
        return None
    return df


def _title_bag(title, key):
    """Shopify title → bag key, via the dashboard's bag key: the longest run of words in the title's name part
    (before the first '|', 'Denri' dropped) that is a bag, then the first word + a usual suffix (HB, Sling, BP …)."""
    parts = [x for x in (re.sub(r"DENRI|X", " ", seg.upper()) for seg in str(title).split("|")) if x.strip()]
    t = re.sub(r"[^A-Z0-9 ]", " ", parts[0] if parts else "").split()
    head = " ".join(t)
    for k, v in WA_ALIAS.items():
        if head.startswith(k):
            return key(v) or v
    for n in range(len(t), 0, -1):                           # longest run of words anywhere in the name part
        for i in range(len(t) - n + 1):
            b = key(" ".join(t[i:i + n])) or key("".join(t[i:i + n]))
            if b:
                return b
    for w in t[:2]:
        for suf in ("HANDBAG", "HB", "SLING", "SLING BAG", "BP", "BACKPACK", "TRAVEL", "BAG"):
            b = key(f"{w} {suf}")
            if b:
                return b
    return None


def wa_clicks_by_bag(start, end, key=None):
    """({bag: {"clicks", "visitors", "colours": {colour: clicks}}}, combo_clicks, unmatched {title: clicks})
    for taps between start and end (Nairobi dates). Combo pages ('A + B') are counted apart, not per bag."""
    if key is None:
        from lib import product_targets
        key = product_targets.bag_key_fn()
    df = _q('SELECT "date" AS d, product_name, variant_name, visitor FROM denri_marketing_wa_click '
            'WHERE "date" BETWEEN :s AND :e', {"s": start, "e": end})
    out, combos, unmatched = {}, 0, {}
    if df is None:
        return out, combos, unmatched
    for _, r in df.iterrows():
        title = str(r["product_name"] or "")
        if "+" in title.split("|")[0]:
            combos += 1
            continue
        bag = _title_bag(title, key)
        if not bag:
            unmatched[title[:60]] = unmatched.get(title[:60], 0) + 1
            continue
        b = out.setdefault(bag, {"clicks": 0, "visitors": set(), "colours": {}})
        b["clicks"] += 1
        b["visitors"].add(r["visitor"])
        col = str(r["variant_name"] or "").strip().upper()
        if col and col != "DEFAULT TITLE":
            b["colours"][col] = b["colours"].get(col, 0) + 1
    for b in out.values():
        b["visitors"] = len(b["visitors"])
    return out, combos, unmatched


def followers_daily():
    """[{platform, date, followers, newFollows, reach, views}] oldest first (from 18 Oct 2026)."""
    df = _q("SELECT platform, date, followers, new_follows, reach, views FROM denri_meta_account_day ORDER BY date, platform")
    if df is None:
        return []
    num = lambda v: None if v != v or v is None else int(v)   # noqa: E731 — NaN → None
    return [{"platform": r["platform"], "date": r["date"].isoformat(), "followers": num(r["followers"]),
             "newFollows": num(r["new_follows"]), "reach": num(r["reach"]), "views": num(r["views"])}
            for _, r in df.iterrows()]


def website_weekly(country="KE"):
    """[{week (Monday), sessions, users, orders, revenue, carts, checkouts, abandoned, waOrders, tillOrders,
    tillNet, onlineShare, payGateway, payOffline}] oldest first."""
    df = _q("""SELECT week_start, sessions_ga4, active_users_ga4, orders, net_revenue, add_to_carts, checkouts_started,
                      abandoned_checkouts, whatsapp_orders, pos_orders, pos_total_net, online_share, pay_gateway, pay_offline
               FROM denri_marketing_web_snapshot WHERE country = :c ORDER BY week_start""", {"c": country})
    if df is None:
        return []
    num = lambda v: None if v is None or v != v else round(float(v), 4)   # noqa: E731
    keys = [("sessions", "sessions_ga4"), ("users", "active_users_ga4"), ("orders", "orders"), ("revenue", "net_revenue"),
            ("carts", "add_to_carts"), ("checkouts", "checkouts_started"), ("abandoned", "abandoned_checkouts"),
            ("waOrders", "whatsapp_orders"), ("tillOrders", "pos_orders"), ("tillNet", "pos_total_net"),
            ("onlineShare", "online_share"), ("payGateway", "pay_gateway"), ("payOffline", "pay_offline")]
    return [{"week": r["week_start"].isoformat(), **{k: num(r[c]) for k, c in keys}} for _, r in df.iterrows()]


# WEBSITE SALES till, split by how the order was paid: Pesapal = paid on the site; the M-Pesa till = taken by people.
TILL_SQL = """
WITH o AS (
  SELECT p.id, date_trunc('week', (p.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi'))::date AS wk,
         CASE WHEN bool_or(pm."name" ILIKE '%%pesapal%%') THEN 'site' ELSE 'people' END AS how
  FROM pos_order p
  JOIN pos_session s ON s.id = p.session_id
  JOIN pos_config pc ON pc.id = s.config_id
  LEFT JOIN pos_payment pp ON pp.pos_order_id = p.id
  LEFT JOIN pos_payment_method pm ON pm.id = pp.payment_method_id
  WHERE pc."name" = :till AND p.state IN ('done', 'paid', 'invoiced')
    AND (p.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
  GROUP BY p.id, wk
)
SELECT o.wk, o.how, COUNT(DISTINCT o.id) AS orders,
       SUM(l.qty) FILTER (WHERE l.full_product_name NOT LIKE '%%+%%'
                          AND l.full_product_name !~* '(delivery|strap|customi[sz]ation|gift bag|kes discount)') AS bags,
       ROUND(SUM(l.price_subtotal_incl)) AS kes
FROM o JOIN pos_order_line l ON l.order_id = o.id
GROUP BY 1, 2 ORDER BY 1, 2
"""


def website_till_by_payment(start, end):
    """{week ISO: {"site": {orders, bags, kes}, "people": {…}}}."""
    df = _q(TILL_SQL, {"till": WEBSITE_TILL, "s": start, "e": end})
    out = {}
    if df is None:
        return out
    for _, r in df.iterrows():
        out.setdefault(r["wk"].isoformat(), {})[r["how"]] = {
            "orders": int(r["orders"] or 0), "bags": int(r["bags"] or 0), "kes": int(r["kes"] or 0)}
    return out


def meta_posts_by_bag(start, end, key=None):
    """({bag: {"posts", "reach", "views"}}, {"posts", "tagged"}) — Facebook + Instagram posts (Kenya's page and account)
    between start and end (Nairobi dates), counted once per bag they're tagged with in Odoo
    (denri_meta_post_product_rel → the product's bag via the dashboard's bag key)."""
    if key is None:
        from lib import product_targets
        key = product_targets.bag_key_fn()
    df = _q("""SELECT p.id, p.reach, p.views, pt."name" AS product
               FROM denri_meta_post p
               LEFT JOIN denri_meta_post_product_rel r ON r.post_id = p.id
               LEFT JOIN product_template pt ON pt.id = r.product_tmpl_id
               WHERE (p.posted_at AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e""",
            {"s": start, "e": end})
    bags, totals = {}, {"posts": 0, "tagged": 0}
    if df is None:
        return bags, totals
    num = lambda v: 0 if v is None or v != v else int(v)    # noqa: E731
    for pid, g in df.groupby("id"):
        totals["posts"] += 1
        names = [n for n in g["product"] if isinstance(n, str) and n]
        if names:
            totals["tagged"] += 1
        for bag in {key(n) for n in names} - {None}:
            b = bags.setdefault(bag, {"posts": 0, "reach": 0, "views": 0})
            b["posts"] += 1
            b["reach"] += num(g["reach"].iloc[0])
            b["views"] += num(g["views"].iloc[0])
    return bags, totals
