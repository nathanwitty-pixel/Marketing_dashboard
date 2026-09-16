"""
offer_picking.py
─────────────────────────────────────────────────────────────────
Offer Picking — a planning tool for which offers/combos to run.

Two jobs (built incrementally):
  1. PROFIT RANKING of the offers currently running — real profit per combo
     = selling price − production cost (BOM). So you can see which offers make
     the most money (a cheap-to-make combo can beat a high-revenue one) and
     which to keep, push, or drop.
  2. NEXT-MONTH PICKER (scaffolded) — take the combos that ran in a reference
     month (e.g. Oct 2025) and match them to CURRENT Odoo stock, so you only
     plan combos you can actually assemble now. Awaiting the reference list.

Data sources:
  • self_made_combos.html  → the SMC payload (running combos: units, revenue,
    component bags + live Odoo stock). Reused so numbers stay consistent and we
    don't re-query — so this runs AFTER self_made_combos.py.
  • "Updated BOMs" sheet   → per-bag production cost (col A = bag, col G = cost).
  • Offers sheet (pending) → official price (D) + offer price (F). When shared,
    swap the price source from actual-sales to the official offer price.

Injects `OP` into offer_picking.html between the OP_DATA markers.
─────────────────────────────────────────────────────────────────
"""
import os
import re
import json

BASE = os.path.dirname(os.path.abspath(__file__))
SMC_HTML = os.path.join(BASE, "self_made_combos.html")
HTML = os.path.join(BASE, "offer_picking.html")
# Local downloaded copy of the offers-sheet prices — refreshed on every successful run,
# consulted automatically when the Google Sheet is unreachable (see _read_offers).
OFFERS_CACHE = os.path.join(BASE, "offers_prices.json")

# Google Sheets: production BOM (accessible) + offers (pending share)
BOM_SHEET_ID = "1GjurDUQOtdsdmS8sn9h4amMmLXYSKNxt63WhdODum8I"
BOM_GID = 678614335
OFFERS_SHEET_ID = "1I68VLBA1UaEcVklTT09chGXXXotVj0Ha4t7vr5NOTtg"

# category/colour words dropped when matching a combo alternative to a BOM bag type
_STOP = {"HANDBAG", "BAG", "TRAVEL", "BACKPACK", "SLING", "SLINGBAG", "COMBO", "OR", "THE",
         "MINI", "BLACK", "GREY", "GREEN", "BROWN", "NUDE", "RED", "BLUE", "MAROON",
         "SPICE", "BEIGE", "CRACKED", "WOOVEN", "PRO", "MAN"}
# Bag-name aliases — reuses the stock-levels name-matching (self_made_combos BAG_ALIASES):
# the attendants' combo wording → the BOM/catalogue bag type. e.g. "Standard" is sold as
# "Standard Travel" but the BOM lists it as TRAVEL, so both map to TRAVEL — that's how a
# bag missing its own BOM row is matched under another name.
_ALIAS = {"STANDARD TRAVEL": "TRAVEL", "STANDARD": "TRAVEL",
          "LAPTOP BACKPACK": "CODE 3", "NEO MAN BAG": "NEO MAN", "CAIRO BACKPACK": "CAIRO BP",
          "ANTI THEFT": "ANTITHEFT", "MIN UMBRA": "MINI UMBRA", "ZIPPED": "ZIPPED LUNCHSET"}


def _apply_alias(up):
    """Apply bag aliases, longest key first (so 'STANDARD TRAVEL' wins over 'STANDARD')."""
    for a, b in sorted(_ALIAS.items(), key=lambda kv: -len(kv[0])):
        up = re.sub(r"\b" + re.escape(a) + r"\b", b, up)
    return up

# Reference-month combos to consider for next month, matched against current Odoo stock.
# (October 2025, user-supplied.) Each line: bags joined by '+', alternatives by '/'.
OCT_2025_COMBOS = [
    "Amaya + Nizana/Zipped",
    "Code 3 + Man Bag/Nizana",
    "Fabela + Code 3/Double Press + Luna/Nizana",
    "Jumbo + Standard/Antitheft",
    "Lola + Mini Zuri/Trecento",
    "Mega/Kai + Man Bag/Nizana/Mini Umbra",
    "Safiri + Standard/Liam/Antitheft",
    "Sierra + Nizana",
    "Standard + Liam + Kaz",
    "Standard + Code 3/Double Press + Mini Umbra/Man Bag",
]

# The full 2025 monthly combo calendar (user-supplied) — for the seasonality analysis.
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHLY_COMBOS_2025 = {
    "Jan": ["Butterfly/Moonbag + Man Bag/Zane", "Gym Bag + Lunchset/Zipped", "Fayola + Man Bag",
            "Lola + Mini Zuri/Oval", "Code 3 + Man Bag", "Travel + Code 3/Double Press + Man Bag/Nizana",
            "Jumbo + Antitheft/Double Press", "Antitheft/Tyler + Man Bag/Zane", "Amaya + Nizana/Zipped",
            "Travel + Nizana/Man Bag"],
    "Feb": ["Baby Bag get Travel free", "Butterfly/Moonbag + Man Bag/Zane", "Code 9/Cairo + Travel",
            "Elyse + Zipped/Lunchset", "Lola + Mini Zuri/Trecento", "Oval + Travel/Fabela",
            "Safiri + Antitheft", "Travel + Code 3/Double Press + Man Bag/Nizana", "Travel + Nizana/Man Bag",
            "Zane/Big Man + Ace/Nizana"],
    "Mar": ["Bonita/Pocket + Antitheft", "Baby Bag get Travel free", "Elyse + Zipped/Lunchset",
            "Jumbo + Jumbo", "Lola + Avana/Mini Zuri", "Oval/Moon + Luna/Zane", "Reo + Kaz",
            "Safiri + Code 3", "Travel + Code 3/Double Press + Man Bag/Nizana", "Zuri + Liam/Nizana"],
    "Apr": ["Baby Bag get Travel free", "Gym Bag get Washbag free", "Elyse + Nizana/Zipped/Lunchset",
            "Fabela + Code 3/Double Press + Luna/Nizana", "Fabela + Code 9/Code 3", "Jumbo + Antitheft",
            "Jumbo + Travel/Liam", "Liam + Kaz", "Moon/Butterfly + Man Bag/Zane", "Safiri + Travel"],
    "May": ["Sierra get Liam/Travel free", "Code 3 + Man Bag/Nizana", "Elyse + Zipped/Lunchset/Nizana",
            "Gym Bag + Splash Bag", "Jumbo + Standard", "Jumbo + Jumbo", "Lola + Cathy",
            "Lola + Aurora/Moon", "Standard + Code 3/Double Press + Nizana/Man Bag", "Zuri get Zipped free"],
    "Jun": ["Big Man + Code 3/Double Press", "Feroz get Washbag free", "Elyse + Zipped",
            "Jumbo + Standard/Antitheft", "Jumbo + Fabela/Liam + Man Bag/Washbag", "Lola + Mini Zuri/Trecento",
            "Reo + Man Bag", "Safiri + Code 3", "Standard + Double Press/Code 3 + Man Bag/Nizana",
            "Standard + Antitheft"],
    "Jul": ["Amaya + Nizana/Zipped", "Baby get Liam free", "Code 3 + Man Bag/Nizana", "Elyse + Nizana/Zipped",
            "Fabela + Code 3/Double Press + Luna/Nizana", "Jumbo + Code 3/Double Press",
            "Lola + Mini Zuri/Trecento", "Safiri + Standard/Liam", "Safiri + Code 3",
            "Travel + Double Press/Code 3 + Man Bag/Nizana"],
    "Aug": ["Baby get Liam free", "Cathy/Skye + Nizana/Mandy", "Claire + Zipped", "Code 3 + Man Bag/Nizana",
            "Fabela + Code 3/Double Press + Luna/Nizana", "Jumbo + Jumbo", "Jumbo + Standard + Luna/Nizana",
            "Lola + Trecento/Mini Zuri", "Safiri + Standard/Antitheft", "Standard/Liam + Code 3/Double Press + Man Bag"],
    "Sep": ["Antitheft + Man Bag", "Baby Bag get Liam Travel free", "Elyse + Nizana/Zipped",
            "Fabela + Code 3/Code 9", "Gym Bag + Mini Umbra", "Jumbo + Jumbo", "Jumbo + Standard + Luna/Nizana",
            "Mini Zuri + Avana/Lola", "Safiri + Standard/Antitheft", "Standard + Code 3/Double Press + Man Bag"],
    "Oct": ["Amaya + Nizana/Zipped", "Code 3 + Man Bag/Nizana", "Fabela + Code 3/Double Press + Luna/Nizana",
            "Jumbo + Standard/Antitheft", "Lola + Mini Zuri/Trecento", "Mega/Kai + Man Bag/Nizana/Mini Umbra",
            "Safiri + Standard/Liam/Antitheft", "Sierra + Nizana", "Standard + Liam + Kaz",
            "Standard + Code 3/Double Press + Mini Umbra/Man Bag"],
    "Nov": ["Baby get Liam free", "Cathy/Skye + Nizana/Mandy", "Elyse + Zipped",
            "Fabela + Code 3/Double Press + Luna/Nizana", "Jumbo + Standard", "Jumbo + Standard + Luna/Mini Umbra",
            "Lola + Trecento/Mini Zuri", "Safiri + Standard/Antitheft",
            "Standard/Liam + Code 3/Double Press + Man Bag", "Standard + Liam + Kaz"],
    "Dec": ["Bonita + Code 3", "Claire + Nizana/Zipped", "Code 3 + Man Bag/Nizana",
            "Fabela + Code 3/Double Press + Luna/Nizana", "Jumbo + Monah/Cairo", "Lola + Mini Zuri/Trecento",
            "Safiri + Standard/Liam/Antitheft", "Standard + Liam + Kaz", "Standard + Mini Umbra",
            "Standard + Code 3/Double Press + Man Bag"],
}


def _read_bom_costs():
    """{BAG TYPE (upper): production cost} from the BOM sheet, col A vs col G."""
    from google_auth import get_gspread_client
    gc = get_gspread_client()
    ws = gc.open_by_key(BOM_SHEET_ID).get_worksheet_by_id(BOM_GID)
    out = {}
    for r in ws.get_all_values()[1:]:
        if len(r) > 6 and str(r[0]).strip():
            try:
                out[str(r[0]).strip().upper()] = float(str(r[6]).replace(",", "").strip() or 0)
            except ValueError:
                pass
    return out


def _read_bag_prices():
    """{BAG (upper): official full price} from bag_original_prices.json (fallback)."""
    p = os.path.join(BASE, "bag_original_prices.json")
    try:
        raw = json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}
    return {str(k).strip().upper(): v for k, v in raw.items()
            if not str(k).startswith("_") and isinstance(v, (int, float))}


def _write_offers_cache(offers):
    """Save a local, human-editable copy of the offers prices to OFFERS_CACHE."""
    import datetime as _dt
    payload = {
        "_note": ("Local copy of the offers-sheet prices (price = full price col D, "
                  "offer = offer price col F, category = col C). Auto-refreshed on every "
                  "successful run and consulted automatically when the Google Sheet is "
                  "unreachable. Set \"_lock\": true to use THIS file as the source of truth — "
                  "your hand edits then win and are never overwritten by the sheet."),
        "_updated": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "_source": "offers sheet %s (worksheet 0)" % OFFERS_SHEET_ID,
        "_lock": False,
        "offers": offers,
    }
    try:
        with open(OFFERS_CACHE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
    except Exception:                                        # noqa: BLE001
        pass


def _read_offers_cache():
    """Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)."""
    try:
        raw = json.load(open(OFFERS_CACHE, encoding="utf-8"))
    except Exception:                                        # noqa: BLE001
        return {}, False
    src = raw.get("offers", {}) if isinstance(raw, dict) else {}
    out = {}
    for k, v in (src.items() if isinstance(src, dict) else []):
        if not isinstance(v, dict):
            continue
        try:
            out[str(k).strip().upper()] = {
                "category": str(v.get("category", "")).strip().upper(),
                "price": float(v.get("price") or 0),
                "offer": float(v.get("offer") or 0),
            }
        except (ValueError, TypeError):
            pass
    return out, bool(raw.get("_lock")) if isinstance(raw, dict) else False


def _read_offers():
    """{BAG (upper): {category, price(full, col D), offer(col F)}} → (offers, source).

    The offers sheet is the source of truth; a local downloaded copy (OFFERS_CACHE) is
    refreshed on every successful read and used as a fallback when the sheet is unreachable.
    If the local copy sets "_lock": true it wins outright — a hand-edited override the sheet
    never clobbers. Category drives handbag detection; offer price is what handbags value at."""
    from google_auth import get_gspread_client

    def _num(x):
        try:
            return float(str(x).replace(",", "").strip() or 0)
        except (ValueError, TypeError):
            return 0.0

    cached, locked = _read_offers_cache()
    if locked and cached:
        return cached, "downloaded copy offers_prices.json (locked — hand-edited override)"
    try:
        gc = get_gspread_client()
        rows = gc.open_by_key(OFFERS_SHEET_ID).get_worksheet(0).get_all_values()
    except Exception:                                        # noqa: BLE001
        if cached:
            return cached, "downloaded copy offers_prices.json (sheet unreachable)"
        return {}, "unavailable (sheet unreachable, no downloaded copy yet)"
    out = {}
    for r in rows[1:]:
        bag = (r[1] if len(r) > 1 else "").strip().upper()
        if not bag or bag == "BAG TYPE":
            continue
        out[bag] = {"category": (r[2] if len(r) > 2 else "").strip().upper(),
                    "price": _num(r[3] if len(r) > 3 else 0),
                    "offer": _num(r[5] if len(r) > 5 else 0)}
    if out:
        _write_offers_cache(out)                             # keep the downloaded copy fresh
        return out, "offers sheet (live — downloaded copy refreshed)"
    if cached:
        return cached, "downloaded copy offers_prices.json (sheet returned no rows)"
    return {}, "offers sheet (empty)"


def _read_smc_payload():
    """Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)."""
    html = open(SMC_HTML, encoding="utf-8").read()
    i = html.find("const SMC =")
    j = html.find("{", i)
    depth, instr, esc, k = 0, False, False, j
    while k < len(html):
        c = html[k]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(html[j:k + 1])
        k += 1
    return {}


def _alt_cost(alt, cost):
    """One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost."""
    up = _apply_alias(str(alt).upper().strip())
    words = [w for w in re.split(r"[^A-Z0-9]+", up) if w]
    core = " ".join(w for w in words if w not in _STOP).strip()
    for cand in (up, core):
        if cand in cost:
            return cost[cand], cand
    best, blen = None, 0
    for k in cost:
        if core and (core.startswith(k) or k.startswith(core)) and len(k) > blen:
            best, blen = k, len(k)
    return (cost[best], best) if best else (None, None)


def _combo_slots(name):
    """Combo name → list of slots, each a list of alternative strings."""
    slots = []
    for grp in re.split(r"\s*\+\s*|\s+[x×]\s+", str(name), flags=re.I):
        alts = [a.strip() for a in re.split(r"\s+or\s+|/", grp, flags=re.I) if a.strip()]
        if alts:
            slots.append(alts)
    return slots


def _combo_cost(name, cost):
    """Production cost = Σ over slots of the average matched-alternative cost.
    Same-bag combos (Jumbo+Jumbo) therefore count each slot → the ×2 you expect."""
    total, missing = 0.0, []
    for alts in _combo_slots(name):
        vals = []
        for a in alts:
            bc, _ = _alt_cost(a, cost)
            if bc is None:
                missing.append(a)
            else:
                vals.append(bc)
        total += (sum(vals) / len(vals)) if vals else 0
    return total, missing


def _resolve_bag(name, cost, bomkeys):
    """Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).
    Reuses the stock-levels aliases (STANDARD→TRAVEL, etc.)."""
    up = _apply_alias(str(name).upper().strip())
    if up in cost:
        return up, cost[up], True
    for k in bomkeys:                                       # bomkeys sorted longest-first
        if up == k or up.startswith(k + " ") or k.startswith(up + " ") or up.startswith(k) or k.startswith(up):
            return k, cost[k], True
    return up, None, False                                  # real bag not in the BOM


def _build_catalog(cost, prod, bomkeys, offers):
    """Every bag the user can pick for a slot, with two prices from the offers sheet:
    `valueWas` = full price (col D) and `valueNow` = offer price (col F). Bags not on the
    sheet fall back to 2 × production cost for both. `value` mirrors valueNow."""
    bag_stock = {}
    for nm, q in prod.items():
        canon, _, _ = _resolve_bag(nm, cost, bomkeys)
        bag_stock[canon] = bag_stock.get(canon, 0) + int(q or 0)
    names = set(cost.keys()) | set(bag_stock.keys()) | set(offers.keys())
    cat = []
    for n in sorted(names):
        c = round(cost[n]) if n in cost else None
        o = offers.get(n, {})
        fallback = (2 * cost[n]) if n in cost else None
        was = o.get("price") or fallback                      # col D full price
        now = o.get("offer") or o.get("price") or fallback    # col F offer price
        cat.append({"name": n, "cost": c, "stock": int(bag_stock.get(n, 0)),
                    "valueWas": (round(was) if was else None),
                    "valueNow": (round(now) if now else None),
                    "value": (round(now) if now else None),
                    "isHandbag": o.get("category", "") == "HANDBAG",
                    "category": o.get("category", "")})
    return cat, bag_stock


def _next_month(cost, offers, ref_month="October 2025"):
    """Reference-month combos matched to current Odoo stock, laid out like the offers sheet
    — a fixed 3-pair grid (slot/slot ➕ slot/slot ➕ slot/slot), each slot pickable (or Zero).
    Prices: NOW = Σ MAX(offer price per pair), WAS = Σ MAX(full price per pair). Pre-fills the
    grid from each October combo; the page lets the user change every slot freely."""
    from lib import stock as _stock
    prod = _stock.odoo_stock_by_product("kenya")            # {PRODUCT NAME: qty} live Kenya
    bomkeys = sorted(cost.keys(), key=len, reverse=True)
    catalog, _ = _build_catalog(cost, prod, bomkeys, offers)
    cat = {c["name"]: c for c in catalog}

    def bag(canon):
        return cat.get(canon, {"name": canon, "cost": 0, "stock": 0, "valueNow": 0, "valueWas": 0})

    cands = []
    for combo in OCT_2025_COMBOS:
        # map the combo's '+' slots (each with '/' alternatives) into a 3×2 grid
        grid = [["Zero", "Zero"], ["Zero", "Zero"], ["Zero", "Zero"]]
        for gi, grp in enumerate(re.split(r"\s*\+\s*", combo)[:3]):
            alts = []
            for a in re.split(r"/", grp):
                a = a.strip()
                if not a:
                    continue
                canon, _, _ = _resolve_bag(a, cost, bomkeys)
                if canon not in alts:
                    alts.append(canon)
            for ai, canon in enumerate(alts[:2]):
                grid[gi][ai] = canon

        price_now = price_was = cost_sum = 0.0
        builds = []                                          # (pair stock, [bag names])
        for pair in grid:
            slotbags = [bag(x) for x in pair if x and x != "Zero"]
            if not slotbags:
                continue
            now = max((b.get("valueNow") or 0) for b in slotbags)
            was = max((b.get("valueWas") or 0) for b in slotbags)
            top = max(slotbags, key=lambda b: (b.get("valueNow") or 0))
            price_now += now
            price_was += was
            cost_sum += (top.get("cost") or 0)
            builds.append((sum(int(b.get("stock") or 0) for b in slotbags),
                           [b["name"] for b in slotbags]))
        buildable = min((s for s, _ in builds), default=0)
        scarce = min(builds, key=lambda x: x[0])[1] if builds else []   # bags of the scarcest pair
        profit = price_now - cost_sum
        cands.append({
            "combo": combo, "grid": grid, "buildable": buildable, "scarce": scarce,
            "priceNow": round(price_now), "priceWas": round(price_was),
            "cost": round(cost_sum), "profit": round(profit),
            "margin": (round(profit / price_now * 100, 1) if price_now else None),
        })
    cands.sort(key=lambda x: -x["profit"])
    return {"ready": True, "refMonth": ref_month, "candidates": cands, "catalog": catalog}


def _region_of(shop_up, SR):
    if shop_up in SR:
        return SR[shop_up]
    for suf in (" SHOP", " SALES", " POS", " STORE"):
        if shop_up.endswith(suf) and shop_up[:-len(suf)] in SR:
            return SR[shop_up[:-len(suf)]]
    return "Other"


def _seasonality(cost, prices, catalog):
    """Per combo in the 2025 monthly calendar: planned months, actual sales by CALENDAR
    month (POS combo '+' lines, Jul 2025 onward — the only window combos were rung as
    products), region split, recurrence, and the formula price. monthTotals lets the page
    de-trend (index a month vs its total) since combo volume is on a growth curve."""
    from lib import db
    from self_made_combos import _combo_sheet_slots, _combo_odoo_slots
    try:
        from self_made_combos import _SHOP_REGION_DEFAULT as SR
    except Exception:                                        # noqa: BLE001
        SR = {}
    bomkeys = sorted(cost.keys(), key=len, reverse=True)
    catval = {c["name"]: c for c in catalog}

    uniq, order = {}, []
    for mi, mn in enumerate(MONTH_NAMES):
        for c in MONTHLY_COMBOS_2025[mn]:
            if c not in uniq:
                uniq[c] = {"slots": _combo_sheet_slots(c), "months": []}
                order.append(c)
            uniq[c]["months"].append(mi + 1)
    sheet_slots = [(c, uniq[c]["slots"]) for c in order]

    def best_match(name):
        """Most-specific match: same slot count, every slot overlaps, and among those the
        combo whose alternatives overlap the sold product most tightly (so 'Safiri +
        Standard/Antitheft' wins over the looser 'Safiri + Antitheft')."""
        o = _combo_odoo_slots(name)
        best, best_score = None, -1.0
        for lbl, s in sheet_slots:
            if len(s) != len(o) or not all((o[i] & s[i]) for i in range(len(s))):
                continue
            overlap = sum(len(o[i] & s[i]) for i in range(len(s)))
            looseness = sum(len(x) for x in s)               # fewer spare alternatives = tighter
            score = overlap - 0.01 * looseness
            if score > best_score:
                best_score, best = score, lbl
        return best

    def price_of(slots):
        tot = 0.0
        for slot in slots:
            best = 0
            for tok in slot:
                canon, _, _ = _resolve_bag(tok, cost, bomkeys)
                b = catval.get(canon)
                if b and b.get("value") is not None and b["value"] > best:
                    best = b["value"]
            tot += best
        return round(tot)

    agg = {c: {"monthly": [0] * 12, "total": 0, "regions": {}} for c in order}
    month_totals = [0] * 12
    sql = """
    SELECT pt."name" AS product, UPPER(COALESCE(pc."name",'?')) AS shop,
           EXTRACT(MONTH FROM p.date_order)::int AS mo, SUM(pl.qty)::int AS units
    FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
    LEFT JOIN pos_session ps ON p.session_id=ps.id
    LEFT JOIN pos_config pc ON ps.config_id=pc.id
    LEFT JOIN product_product pp ON pl.product_id=pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
    WHERE p.state IN ('done','paid') AND pl.qty>0 AND pl.price_subtotal>0
      AND pt."name" LIKE '%+%' AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
      AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
      AND p.date_order >= '2025-07-01'
    GROUP BY pt."name", shop, mo
    """
    df = db.run_query(sql, {})
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            mo, u = int(r["mo"]), int(r["units"])
            month_totals[mo - 1] += u
            lbl = best_match(r["product"])
            if not lbl:
                continue
            a = agg[lbl]
            a["monthly"][mo - 1] += u
            a["total"] += u
            reg = _region_of(str(r["shop"]).strip().upper(), SR)
            a["regions"][reg] = a["regions"].get(reg, 0) + u

    combos = []
    for c in order:
        a = agg[c]
        top = max(a["regions"].items(), key=lambda kv: kv[1])[0] if a["regions"] else None
        combos.append({"combo": c, "months": uniq[c]["months"], "monthly": a["monthly"],
                       "total": a["total"], "price": price_of(uniq[c]["slots"]),
                       "topRegion": top, "regions": a["regions"], "recur": len(uniq[c]["months"])})
    combos.sort(key=lambda x: -x["total"])
    return {"monthNames": MONTH_NAMES, "monthTotals": month_totals, "combos": combos,
            "salesFrom": "Jul 2025",
            "note": "Combos are rung as POS products only from Jul 2025; earlier months show the plan, sales de-trend via month totals."}


def build():
    smc = _read_smc_payload()
    cost = _read_bom_costs()
    cards = smc.get("runningCards", []) or []
    mi = {r["combo"]: r for r in (smc.get("monetaryImplication", {}) or {}).get("running", [])}

    offers, missing = [], set()
    for c in cards:
        lbl = c.get("sheetLabel") or c.get("name")
        name = c.get("name", "")
        pc, miss = _combo_cost(name, cost)
        missing.update(miss)
        m = mi.get(lbl, {})
        units = m.get("units") or c.get("total") or 0
        price = round(m["actual"] / units) if (m.get("actual") and units) else 0
        profit = price - pc
        # buildable from current Odoo stock: min over slots of the slot's combined stock
        stock_by = {str(b.get("name", "")).upper(): int(b.get("stock") or 0) for b in c.get("bags", [])}
        slot_stock = []
        for alts in _combo_slots(name):
            s = 0
            for a in alts:
                _, key = _alt_cost(a, cost)
                # match the alt to one of this combo's bag names for its live stock
                for bn, bs in stock_by.items():
                    if key and (bn == key or bn.startswith(key) or key.startswith(bn)):
                        s += bs
                        break
            slot_stock.append(s)
        buildable = min(slot_stock) if slot_stock else 0

        offers.append({
            "combo": lbl,
            "category": c.get("category", "") or "",
            "price": price,
            "cost": round(pc),
            "profit": round(profit),
            "margin": round(profit / price * 100, 1) if price else 0.0,
            "units": units,
            "totalProfit": round(profit * units),
            "revenue": m.get("actual", 0) or 0,
            "buildable": buildable,
            "bags": [{"name": b.get("name"), "stock": int(b.get("stock") or 0), "star": bool(b.get("star"))}
                     for b in c.get("bags", [])],
        })

    offers.sort(key=lambda x: -x["totalProfit"])

    offer_prices, offers_source = _read_offers()
    try:
        next_month = _next_month(cost, offer_prices)
    except Exception as ex:                                   # noqa: BLE001
        next_month = {"ready": False, "refMonth": None, "candidates": [], "error": str(ex)[:200]}

    # Power-deal candidates: single bags to run as a discounted deal, priced WAS (full,
    # col D) vs NOW (offer, col F). Margin on the offer price; stock = inventory to clear.
    catalog = next_month.get("catalog", []) if isinstance(next_month, dict) else []
    power = []
    for b in catalog:
        now, was, c = b.get("valueNow"), b.get("valueWas"), b.get("cost")
        if now and c is not None and b.get("stock", 0) > 0:
            profit = now - c
            power.append({"bag": b["name"], "priceWas": was or now, "priceNow": now, "cost": c,
                          "profit": round(profit), "margin": round(profit / now * 100, 1),
                          "stock": b["stock"]})
    power.sort(key=lambda x: -x["margin"])

    try:
        seasonality = _seasonality(cost, offer_prices, catalog)
    except Exception as ex:                                   # noqa: BLE001
        seasonality = {"monthNames": MONTH_NAMES, "monthTotals": [0] * 12, "combos": [], "error": str(ex)[:200]}

    # Forecast the NEXT calendar month for each picked combo: its historical share of that
    # month's combo sales, whether its offer price sits in the target band, and a
    # recommendation. Best October picks (in-band + selling that month) sort to the top.
    import datetime as _dt
    _fm = (_dt.date.today().month % 12) + 1                    # next month (Sep → Oct)
    _sea = {c["combo"]: c for c in seasonality.get("combos", [])}
    _mt = (seasonality.get("monthTotals") or [0] * 12)[_fm - 1] or 1
    PMIN, PMAX = 3399, 6199
    STOCK_MIN = 100                                            # bags above 100 are "doable" now
    _bk = sorted(cost.keys(), key=len, reverse=True)

    # Client demand from THIS month's self-made combos (CBR) — what clients are requesting
    # now, per bag, weighted by units. A leading demand signal for next month's offers.
    sm_demand = {}
    for r in (smc.get("selfMade") or []):
        q = int(r.get("qty") or 0)
        seen = set()
        for slot in _combo_slots(r.get("name", "")):
            for a in slot:
                canon, _, _ = _resolve_bag(a, cost, _bk)
                if canon in seen:
                    continue
                seen.add(canon)
                sm_demand[canon] = sm_demand.get(canon, 0) + q

    if isinstance(next_month, dict) and next_month.get("candidates"):
        for cand in next_month["candidates"]:
            sc = _sea.get(cand["combo"], {})
            units = (sc.get("monthly") or [0] * 12)[_fm - 1]
            cand["forecastUnits"] = units
            cand["forecastPct"] = round(units / _mt * 100, 1)
            bags = set(x for pair in cand.get("grid", []) for x in pair if x and x != "Zero")
            cand["clientDemand"] = sum(sm_demand.get(b, 0) for b in bags)   # self-made requests for its bags
            cand["inRange"] = bool(PMIN <= (cand.get("priceNow") or 0) <= PMAX)
            cand["stockReady"] = bool((cand.get("buildable") or 0) >= STOCK_MIN)
            # demand = it sold that month last year OR clients are self-making its bags now
            good = cand["inRange"] and (units > 0 or cand["clientDemand"] > 0)
            cand["recommended"] = bool(good and cand["stockReady"])
            cand["needsProduction"] = bool(good and not cand["stockReady"])
        # picks first, then produce, then rest; within each by forecast units + client demand
        next_month["candidates"].sort(key=lambda x: (
            0 if x.get("recommended") else (1 if x.get("needsProduction") else 2),
            -(x.get("forecastUnits") or 0), -(x.get("clientDemand") or 0), -(x.get("profit") or 0)))
        next_month["forecastMonth"] = MONTH_NAMES[_fm - 1]
        next_month["priceMin"], next_month["priceMax"], next_month["stockMin"] = PMIN, PMAX, STOCK_MIN
        next_month["smMonth"] = smc.get("month", "")

    payload = {
        "month": smc.get("month", ""),
        "priceSource": "WAS = full price (col D), NOW = offer price (col F) · " + offers_source,
        "offers": offers,
        "bomBags": len(cost),
        "unmatched": sorted(missing),
        "nextMonth": next_month,
        "powerDeals": power,
        "seasonality": seasonality,
    }

    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- OP_DATA_START -->\n<script>const OP = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
             + ";</script>\n<!-- OP_DATA_END -->")
    html = re.sub(r"<!-- OP_DATA_START -->.*?<!-- OP_DATA_END -->", lambda _: block, html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return payload


if __name__ == "__main__":
    p = build()
    print("offer_picking.html updated.")
    print(f"  Price source    : {p.get('priceSource', '')}")
    if os.path.exists(OFFERS_CACHE):
        print(f"  Downloaded copy : {OFFERS_CACHE}")
    print(f"  Offers ranked   : {len(p['offers'])}  (BOM bags: {p['bomBags']})")
    for o in p["offers"][:5]:
        print(f"    {o['combo'][:34]:<34} price {o['price']:>5}  cost {o['cost']:>5}  "
              f"margin {o['margin']:>5}%  units {o['units']:>3}  profit {o['totalProfit']:>8}  build {o['buildable']}")
    if p["unmatched"]:
        print(f"  Unmatched bags  : {p['unmatched']}")
