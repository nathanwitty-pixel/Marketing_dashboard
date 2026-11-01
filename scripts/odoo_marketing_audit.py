"""scripts/odoo_marketing_audit.py — how complete and up to date each marketing source in Odoo is, and what the
dashboard could use it for (spec: docs/odoo-marketing-audit.md).

    python scripts/odoo_marketing_audit.py   # → notes/ODOO_MARKETING_AUDIT.md + data/odoo_marketing_audit.csv
"""
import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import db, paths   # noqa: E402

NAIROBI = "(%s AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date"
_bag = "EXISTS (SELECT 1 FROM denri_meta_post_product_rel r WHERE r.post_id = t.id)"
_tag = "EXISTS (SELECT 1 FROM denri_meta_post_tag_rel r WHERE r.post_id = t.id)"

# tab = the Marketing OS tab / chip it shows under; gran = day | week | month; group = what it's kept per.
SOURCES = [
    # ── Content / Meta ──
    dict(tab="Content", label="Facebook + Instagram posts", table="denri_meta_post", gran="day", date=NAIROBI % "t.posted_at",
         group="t.platform", need=0, fields=[("tagged with a bag", _bag), ("content tag", _tag), ("reach in", "t.reach IS NOT NULL")],
         use="Posting per bag (replace the posting sheets) + reach/views per bag; needs every post tagged with its bags."),
    dict(tab="Meta / Social reach", label="Account per day (followers, reach)", table="denri_meta_account_day", gran="day",
         date="t.date", group="t.platform", fields=[("reach in", "t.reach IS NOT NULL"), ("followers in", "t.followers IS NOT NULL")],
         use="Follower growth and reach trend next to sales."),
    dict(tab="Meta", label="Comments (brand listening)", table="denri_listening_mention", gran="day", date=NAIROBI % "t.date",
         group="t.platform", fields=[("sentiment", "t.sentiment IS NOT NULL"), ("topic", "t.topic IS NOT NULL")],
         need=0, use="Comment volume per post / bag; sentiment needs the Claude key in Setup."),
    dict(tab="Content", label="Old daily posting log (all platforms)", table="denri_marketing_post", gran="day", date='t."date"',
         group="t.platform_code", fields=[("bags named", "COALESCE(t.products, '') <> ''")],
         use="Was the all-platform log; stopped, so not usable."),
    dict(tab="Content", label="Content calendar", table="denri_marketing_content", gran="week", date='t."date"', group=None,
         fields=[("status", "t.status IS NOT NULL")], use="Content plan vs delivered."),
    dict(tab="Home", label="Weekly activity notes", table="denri_marketing_activity", gran="week", date="t.week_start",
         group="t.department", fields=[], use="Text notes only."),
    # ── Channels (ads) ──
    dict(tab="Channels / Ad spend", label="Meta ads, daily per campaign", table="denri_marketing_ads", gran="day", date='t."date"',
         where="t.source = 'meta_ads' AND t.granularity = 'daily'", group="t.country",
         fields=[("spend", "COALESCE(t.spend, 0) > 0"), ("messages", "t.messages IS NOT NULL"), ("purchases", "t.direct_purchases IS NOT NULL")],
         use="Bring back the Ads impact panel from Odoo: spend, cost per message vs bags sold."),
    dict(tab="Channels / Ad spend", label="Ads, weekly (typed in)", table="denri_marketing_ads", gran="week", date='t."date"',
         where="t.source = 'manual'", group="t.country", fields=[("spend", "COALESCE(t.spend, 0) > 0")],
         use="History before the Meta sync (Jan–early Oct)."),
    dict(tab="Channels", label="Google Ads", table="denri_marketing_ads", gran="day", date='t."date"',
         where="t.source = 'google_ads'", group="t.country", fields=[], use="Syncs hourly but writes nothing yet."),
    dict(tab="TikTok", label="TikTok Ads", table="denri_marketing_ads", gran="day", date='t."date"',
         where="t.source = 'tiktok_ads'", group="t.country", fields=[], use="Needs the TikTok business ID in Setup."),
    # ── Leads ──
    dict(tab="Leads", label="Social DM leads (FB / IG / TikTok)", table="denri_social_dm", gran="day", date='t."date"',
         group="t.channel_id::text", fields=[("bag asked about", "t.product_id IS NOT NULL"), ("shop", "t.shop_id IS NOT NULL"),
                                              ("outcome recorded", "COALESCE(t.shop_outcome_id, t.call1_outcome_id, t.call2_outcome_id) IS NOT NULL"),
                                              ("from an ad (yes/no)", "t.is_ad IS NOT NULL")],
         use="DM → sale conversion by channel and per bag; ad vs organic leads."),
    dict(tab="Leads", label="Leads, daily (typed in)", table="denri_marketing_lead", gran="day", date='t."date"',
         where="t.granularity = 'daily'", group="t.channel", fields=[], use="Old daily lead counts."),
    dict(tab="Leads", label="Influencer leads", table="denri_marketing_influencer_lead", gran="month", date="t.month",
         group="t.country", fields=[], use="Influencer leads per month."),
    dict(tab="Leads", label="WhatsApp engagement (CRM)", table="denri_crm_whatsapp_engagement", gran="day", date='t."date"',
         group="t.branch_id::text", fields=[("sale amount", "t.sale_amount IS NOT NULL")], use="Small; agent follow-ups."),
    # ── Sales / website ──
    dict(tab="Sales / Net revenue, GA4, checkouts", label="Website weekly snapshot", table="denri_marketing_web_snapshot",
         gran="week", date="t.week_start", group="t.country",
         fields=[("GA4 sessions", "t.sessions_ga4 IS NOT NULL"), ("net revenue", "t.net_revenue IS NOT NULL"),
                 ("add to carts", "t.add_to_carts IS NOT NULL"), ("checkouts", "t.checkouts_started IS NOT NULL"),
                 ("abandoned", "t.abandoned_checkouts IS NOT NULL"), ("WhatsApp orders", "t.whatsapp_orders IS NOT NULL"),
                 ("Shopify sessions", "t.sessions_shopify IS NOT NULL")],
         use="Website funnel card + online share of revenue, week on week."),
    dict(tab="Website new users", label="Website new users", table="denri_marketing_web_traffic", gran="month", date="t.month",
         group="t.country", fields=[], use="New users per month."),
    dict(tab="WhatsApp checkouts", label="Website WhatsApp clicks per product", table="denri_marketing_wa_click", gran="day",
         date="t.date", group="t.country", fields=[("product", "t.product_id IS NOT NULL")],
         use="Per-bag online demand (Bag Signals / Product Performance)."),
    dict(tab="Sales", label="Back-in-stock sign-ups", table="denri_marketing_restock_request", gran="day", date="t.date",
         group=None, fields=[("product", "t.product_id IS NOT NULL")], use="Out-of-stock demand per bag (few rows)."),
    dict(tab="Sales", label="Website channel / product / referrer", table="denri_marketing_web_channel", gran="week",
         date="t.week_start", group="t.country", fields=[], use="One week only (8 Jun)."),
    # ── Foot traffic / calls / messages ──
    dict(tab="Foot traffic", label="Foot traffic, daily (POS door counts)", table="denri_marketing_foot_daily", gran="day",
         date="t.date", where="t.from_pos", group="t.branch_id::text",
         fields=[("visitors", "t.visitors IS NOT NULL"), ("purchased", "t.purchased IS NOT NULL")],
         use="ALREADY USED: Footfall & Marketing reads the same door counts (denri_footfall_count)."),
    dict(tab="Calls", label="Calls, weekly per shop", table="denri_marketing_calls", gran="week", date="t.week_start",
         group="t.branch_id::text", fields=[], use="Calls per shop."),
    dict(tab="Home", label="Messages handled, daily per shop", table="denri_marketing_messages_daily", gran="day",
         date="t.date", group="t.branch_id::text", fields=[], use="Online vs shop messages."),
    dict(tab="Home", label="Shop social performance (WhatsApp status)", table="denri_marketing_shop_week", gran="week",
         date="t.week_start", group="t.branch_id::text", fields=[], use="Shop status posts, views, contacts saved."),
    dict(tab="Social reach", label="Social, weekly per platform (typed in)", table="denri_marketing_social", gran="week",
         date="t.week_start", group="t.platform || ' ' || t.country", fields=[("reach", "t.reach IS NOT NULL"),
                                                                             ("followers", "t.followers IS NOT NULL")],
         use="TikTok / YouTube / X / LinkedIn reach (the only place they are)."),
    dict(tab="Setup", label="Marketing expense", table="denri_marketing_expense", gran="month", date="t.month",
         group="t.country", fields=[], use="Monthly spend per market."),
]


def _period(d, gran):
    if gran == "week":
        return d - datetime.timedelta(days=d.weekday())
    if gran == "month":
        return d.replace(day=1)
    return d


def _step(p, gran):
    if gran == "week":
        return p + datetime.timedelta(days=7)
    if gran == "month":
        return (p.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    return p + datetime.timedelta(days=1)


def _expected(today, gran):
    if gran == "week":
        return _period(today, "week") - datetime.timedelta(days=7)        # last complete week
    if gran == "month":
        return _period(_period(today, "month") - datetime.timedelta(days=1), "month")   # last month
    return today - datetime.timedelta(days=1)                               # yesterday


def audit(src, today):
    fields = src.get("fields") or []
    cols = ", ".join(f"CASE WHEN {expr} THEN 1 ELSE 0 END AS f{i}" for i, (_, expr) in enumerate(fields))
    sql = (f"SELECT {src['date']} AS d, {src.get('group') or repr('all')} AS g{', ' + cols if cols else ''} "
           f"FROM {src['table']} t WHERE {src.get('where') or 'TRUE'}")
    df = db.run_query(sql, {})
    gran = src["gran"]
    exp = _expected(today, gran)
    out = {"tab": src["tab"], "source": src["label"], "table": src["table"], "every": gran, "use": src["use"],
           "rows": 0, "first": "", "latest": "", "behind": "", "filled": None, "fields": "", "status": "⛔ Empty"}
    if df is None or df.empty:
        return out
    df = df[df["d"].notna()]
    df["d"] = [x if isinstance(x, datetime.date) else x.date() for x in df["d"]]
    df["p"] = [_period(x, gran) for x in df["d"]]
    df["g"] = df["g"].fillna("—").astype(str)
    first, last = min(df["d"]), max(df["d"])
    behind = max(len(_range(_period(last, gran), _period(exp, gran), gran)) - 1, 0)
    # check window: last 8 weeks / 6 months up to the expected latest, not before the first row
    span = {"day": 55, "week": 49, "month": 150}[gran]
    w_start = max(_period(exp - datetime.timedelta(days=span), gran), _period(first, gran))
    periods = _range(w_start, _period(exp, gran), gran)
    recent = df[df["d"] >= last - datetime.timedelta(days=120)]
    groups = sorted(set(recent["g"]))
    have = set(zip(df["g"], df["p"]))
    want = [(g, p) for g in groups for p in periods]
    filled = round(100 * sum(1 for k in want if k in have) / len(want)) if want else 0
    win = df[df["p"] >= w_start]
    win = win if not win.empty else df
    fill = ", ".join(f"{name} {round(100 * win[f'f{i}'].mean())}%" for i, (name, _) in enumerate(fields))
    unit = {"day": "day", "week": "week", "month": "month"}[gran]
    need = src.get("need")
    need_pct = round(100 * win[f"f{need}"].mean()) if need is not None else 100
    if behind == 0 and filled >= 90 and need_pct >= 90:
        status = "✅ Ready"
    elif behind <= 1 and filled >= 50:
        status = "🟡 Partial" + (f" (only {need_pct}% {fields[need][0]})" if need_pct < 90 else "")
    else:
        status = "❌ Stale"
    out.update(rows=len(df), first=first.isoformat(), latest=last.isoformat(),
               behind="up to date" if behind == 0 else f"{behind} {unit}{'s' if behind != 1 else ''}",
               filled=filled, fields=fill, status=status, groups=len(groups))
    return out


def _range(a, b, gran):
    out, p = [], a
    while p <= b:
        out.append(p)
        p = _step(p, gran)
    return out


def main():
    today = datetime.date.today()
    rows = []
    for src in SOURCES:
        try:
            rows.append(audit(src, today))
        except Exception as ex:                              # noqa: BLE001
            print(f"  {src['label']}: failed ({ex})")
    order = {"✅": 0, "🟡": 1, "❌": 2, "⛔": 3}
    rows.sort(key=lambda r: (order[r["status"][0]], -(r["filled"] or 0)))
    keys = ["status", "tab", "source", "table", "every", "rows", "first", "latest", "behind", "filled", "fields", "use"]
    with open(paths.data("odoo_marketing_audit.csv"), "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    md = [f"# Odoo marketing data audit — {today:%d %b %Y}", "",
          "Generated by `scripts/odoo_marketing_audit.py` (spec: docs/odoo-marketing-audit.md). **Filled** = of the "
          "periods the source should have over the last 8 weeks (6 months for monthly), for every shop / country / "
          "platform it's kept by, how many have data. **Behind** = newest data vs yesterday / last complete week / "
          "last month.", "",
          "| Status | Marketing OS | Source | Every | Rows | Latest | Behind | Filled | Key fields entered | Dashboard use |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['status']} | {r['tab']} | {r['source']} (`{r['table']}`) | {r['every']} | {r['rows']:,} | "
                  f"{r['latest'] or '—'} | {r['behind'] or '—'} | {'' if r['filled'] is None else str(r['filled']) + '%'} | "
                  f"{r['fields'] or '—'} | {r['use']} |")
    with open(paths.root("notes", "ODOO_MARKETING_AUDIT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    for r in rows:
        print(f"{r['status']:10} {r['source'][:42]:42} {r['latest'] or '—':10} {r['behind'] or '—':12} "
              f"{'' if r['filled'] is None else str(r['filled']) + '%':5} {r['fields']}")


if __name__ == "__main__":
    main()
