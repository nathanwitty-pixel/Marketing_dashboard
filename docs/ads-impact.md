# Ads impact — on every page (21 Oct 2026, user's call)

The weekly **Ads Performance Report** (marketing's .pptx on Drive, Sun–Sat weeks, e.g.
*Denri_Weekly_Ads_Report_11-17_Oct_2026*) joined to what the dashboard already knows (Odoo sales,
marketing posts, corporate payments), so every page shows what the ads cost, what moved, and what to do.

- **Data (weekly upload — the user shares the report, Claude transcribes):**
  - `data/ads_weekly.csv` — one row per campaign per week: `week_start` (Sunday), `platform`, `market`
    (KENYA / SINZA / UGANDA), `campaign`, `focus` (offers / new_bags / corporate / website), `currency`
    (KES / USD), `spend`, `results`, `result_type` (messages, conversions, purchases, website users,
    engaged sessions), `impressions`, `clicks`.
  - `data/ads_notes.csv` — the report's takeaways and next steps: `week_start`, `tags`
    (`;`-separated: all / offers / combos / new_bags / corporate / shops / website), `market`,
    `kind` (win / watch / do / event), `text`.
- **Generator:** `generators/ads_impact.py` → `data/ads_impact.json` (one section per page html).
  Runs with Current Performance and Posting Yields (`dashboard_pages.json`); the other pages read the file.
- **Shown by:** `assets/ads_panel.js`, injected on **every page** by `streamlit_app.py` (same place as the
  theme), with that page's section. Collapsible: headline tiles always visible, "Details" opens the table
  and the full list of actions. Missing file / no section → nothing shown.

## Figures

- **Ad spend** = KES campaigns + USD campaigns × `USD_KES` in `lib/ads.py` (an assumed rate, shown with ≈).
- **Messages** = Meta messaging conversations + TikTok conversions (the report's "messages"). Google /
  X website results are listed separately (purchases, website users, engaged sessions).
- **Sales** per market and week from Odoo POS: bags (combo '+' wrapper excluded), orders, revenue
  (combo money included, Sinza ÷25, Uganda ÷29 — same as `sql/bag_revenue.sql`).
- **Ads % of revenue** = ad spend ÷ revenue. **Ad cost per bag** = ad spend ÷ bags sold. These are the fair
  measures across markets — cost per message flatters cheap-message, low-conversion markets (Tanzania).
- **Posts** per market and week from `lib/marketing_posts`.
- **Posts → sales a week later:** per Kenya bag type, the change in posts one week against the change in
  bags sold the next, pooled over the report's weeks. Shown as "bags posted more sold X% more the following
  week" vs "posted less". Measured 21 Oct 2026: +13.0% vs −8.7% (same-week comparison is the opposite,
  because marketing posts more on bags that are already slowing). A pattern across bags, not proof per bag.
- **Corporate:** Corporate offers campaign spend and messages next to corporate bags paid and KES received
  (`sql/corporate_bags.sql`) since the campaign started.
- No ad is linked to a single till sale (except corporate and Google web purchases): comparisons are by
  week and market, and the panel says so.

## Charts (21 Oct 2026, user's call)

Two charts under the tiles, on every page (Chart.js 4.4.0, loaded by the panel when a page has none;
`chartSwitch: false` so the page's chart menu leaves them alone):

- **Week on week** — the report's weeks, by market (Kenya blue, Tanzania orange, Uganda aqua: palette
  slots 1–3). Toggle: Ad spend, Messages, Bags sold, Posts = bars stacked by market (tooltip adds the
  all-markets total); Cost per message, Ad cost per bag, Ads % of revenue = one line per market. On the
  offers / New Bags pages spend and messages cover those campaigns only (the note says so), and the
  two all-ads ratios are left off.
- **Last week by campaign** — one bar per campaign, colour = market, value at the bar end. Toggle: Spend
  (every campaign, USD ones ≈ KES), Messages, Cost per message (chat campaigns only; tooltip shows the
  3-week average and the change). Filtered to the page's campaigns like the table.

Data: `chart` in each section of `data/ads_impact.json` (`weeks`, `markets`, `series` per market:
spend, chatSpend, messages, bags, revenue, posts; `campaigns` for the last week).

## What each page shows

| Page | Section |
|---|---|
| Current Performance, Monthly Report, History, Bag Signals, Reject Sale | Overview: tiles for the last report week (spend, messages, ads % of revenue, ad cost per bag, each week on week) + market table + actions tagged `all` / `corporate` |
| Product Performance, New Products | New Bags campaign weekly + overview tiles; actions `new_bags` |
| Timed Offers, Bags On vs Off Offer, Offer Picking, Self-made vs Running Combos | Offer campaigns (Meta Weekly / Monthly Offers in all markets, TikTok Monthly Offers, Hot Picks) weekly; actions `offers` / `combos` |
| Shop Stock Levels, Shops Efficiency, Push Planner, Shop Launch | Market table + branch cost notes from Weekly Offers; actions `shops` |
| Posting Yields | Posts vs ads vs sales per market and week + the posts → next-week-sales finding |

## Actions ("what we can do")

Computed every run, then the report's own notes:
- A market whose **ads % of revenue > 6%** or **ad cost per bag > KES 150** → *watch*: ads aren't paying
  back at the till; test a cut or redirect.
- **Messages up but orders down** week on week (≥5% each way) → *watch*: the extra chats aren't buying.
- A campaign's **cost per result vs its 3-week average**: ≥ +15% → *do* refresh the creative; ≤ −15% → *win*.
- **Posts → next-week sales** → *do*: plan posts a week before the sales are wanted.
- **Corporate**: KES received per KES spent on the corporate campaign.
- A paused campaign (notes `event`) → before / after sales for that market when the data allows.

## Refresh

```
python generators/ads_impact.py
```
