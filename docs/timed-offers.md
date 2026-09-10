# Timed Offers Analytics

- **Generator:** `timed_offers.py`
- **HTML:** `timed_offers.html`
- **Data marker:** `<!-- TIMED_DATA_START -->…<!-- TIMED_DATA_END -->` — injects
  `const TO_DATA = {"month", "offers":[…]}`, then `const TO_LIST = TO_DATA.offers` and
  `const TO = TO_LIST[0]` (back-compat).
- **Config:** `timed_offers_config.json`

## What the page shows

**Every** timed-offer **campaign** running in the month, **stacked** on one page (Kenya):
each shows per-bag sales over that campaign's exact date window, alongside the marketing
posting that ran with it. One `<template id="to-offer-tpl">` is cloned per offer and filled
by `renderOffer(TO, root)` (data hooks are `data-el="…"`, scoped to each offer's clone, so
several offers coexist without id clashes).

## Multiple offers & month rollover

- **Add an offer:** append an item to the `offers` list in the config (below). All offers
  in the list run live and stack on the page — you don't remove the old ones by hand.
- **Rollover (automatic, at month end):** `month_end.py` archives the closing month's
  offers to Supabase (via `monthly_report.py._read_timed_offers()` → `timedOffers` in
  `monthly_report_history.json` → `push_to_supabase.py` → `denri_mkt_timed_offer*` tables),
  then **clears** the config (`offers: []`, `month` bumped to the new month) so the timed
  offers start free. The clear only fires on a real unpinned 1st-of-month run and only after
  every archive step succeeds — `timed_offers.py` itself never archives or clears (it runs
  on every refresh/snapshot and must not race the archive).

## Data sources

- **Sales:** LIVE from Odoo POS for the **exact** `startDate…endDate` (end-of-day
  inclusive), Kenya market (every till except Sinza/Dar/Uganda), per bag type. Excludes
  combo wrappers / delivery / customisation / straps / samples / POS-category lines (same
  rules as the Total Sales figure).
- **Posting:** last week's Kenya marketing posting (WEEKLY_MARKETING_POST col E) per bag
  type, borrowed alongside the sales.
- **Config** (`timed_offers_config.json`): `{"month": "YYYY-MM", "offers": [offer, …]}`.
  Each **offer**: `name`, `market`, `shops[]` (limit sales to those POS tills — e.g. Nairobi
  CBD = Hazina/Hilton/Starmall/KTDA Shop; empty = whole market), `startDate`, `endDate`,
  `bags[]` (default Kai, Pioneer, Double Press, Antitheft, Code 3, School bag), `prices{}`
  (`{BAG: {was, now}}` — config prices win over Odoo's pricelist for a manual cut like "300
  off"). A legacy single-offer file (top-level `name`/`bags`/`startDate`) is still read and
  auto-wrapped into a one-item `offers` list.

## Editing a campaign

Edit `timed_offers_config.json` — add/adjust items in `offers[]` (dates + shops + bag list +
prices) — then regenerate. Each window is literal: set `startDate`/`endDate` to the
campaign's real span. (The inline page control edits **offer[0]**'s shops/window only;
multi-offer editing is done in the file.)

## Regenerate

```
python timed_offers.py            # DENRI_LAUNCHER=1 to skip the browser tab
```
`main.py` also re-runs this daily so it records that day's shop-scoped snapshot.
