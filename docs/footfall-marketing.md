# Footfall and Marketing (21 Oct 2026, user's call)

Shop by shop and week by week: do posting and ads bring people through the door, and do the shops turn
them into buyers? Footfall (people counted entering each shop) is joined to walk-in till sales, WhatsApp
chats, marketing posts and ad spend.

- **Generator:** `generators/footfall_marketing.py` → `data/footfall_marketing.json` and the
  `<!-- FOOT_DATA_START -->…<!-- FOOT_DATA_END -->` block (const `FOOT`) in `html/footfall_marketing.html`.
- **Library / SQL:** `lib/footfall.py` (`daily`, `weekly`, shop mapping), `sql/footfall_walkins.sql`.
- **Page:** "Footfall and Marketing" in `dashboard_pages.json` (section Shops). The Ads impact panel
  shows its `shops` section here too (`generators/ads_impact.py` PAGES).

## Sources

| What | Where | Fields |
|---|---|---|
| Visitors | `denri_footfall_count` | `date`, `config_id` (= `pos_config.id`, the shop), `manual_count` (visitors counted at close of day), `counted_by`, `note` |
| Walk-in buyers | `pos_order` + `pos_order_line` | `customer_type = 'walkin'` (others: online, activation, employee), `state` in done / invoiced / paid, `amount_total > 0`, shop = `pos_session.config_id`, day = `date_order + 3 hours` (Kenya time) |
| WhatsApp chats | `denri_monitor_interaction` | `date`, `shop_id` → `denri_monitor_shop.name`, `response_time_first` (minutes to the first reply, from Jul 2026), `is_purchased`, `source_id` → `denri_monitor_source.is_paid` (paid ad lead) |
| Posts | `lib/marketing_posts.posts(start, end)` | `{(bag type, colour): {market: posts}}`, markets KENYA / SINZA / UGANDA |
| Ads | `lib/ads.py` over `data/ads_weekly.csv` | spend per campaign per week per market (KES; USD × `USD_KES`) |

Footfall is counted daily from Jan 2026 (16–18 shops, about 15,000 visitors a month). **Today is left
out**: its count is entered at close of day.

### Shop mapping (`lib/footfall.SHOPS`)

Footfall shop = `pos_config.name`. WhatsApp shop and market:

| pos_config | WhatsApp shop | Market |
|---|---|---|
| KTDA Shop | Ktda | KENYA |
| DAR-ES-ALAM | Sinza | SINZA (Tanzania) |
| UGANDA | Uganda | UGANDA |
| every other shop (BUSIA, ELDORET, HAZINA, HILTON, KAKAMEGA, KISII, KISUMU, KITENGELA, MERU, MOMBASA, NAKURU, NANYUKI, RONGAI, STARMALL, THIKA) | same name, title case | KENYA |

## Definitions

- **Visitors** = `manual_count`, summed over the week's **counted days**.
- **Walk-in orders** = walk-in POS orders on counted days. **Conversion** = walk-in orders ÷ visitors.
- **Revenue per visitor** = walk-in KES ÷ visitors, **without bulk orders**. Money is KES-normalised:
  DAR-ES-ALAM (and Sinza) ÷ 25, UGANDA ÷ 29, the same as `sql/bag_revenue.sql`.
- **Bulk order** = a walk-in order with any POS line of **10+ units**. Its KES and units are kept apart:
  shown with ⚠, the reason ("bulk line of N units") and the "without bulk order" figure.
- **WhatsApp** (from Jul 2026): **paid-ad leads only** per shop (source `is_paid`): chats, conversion
  (`is_purchased`), median `response_time_first`. Walk-in and existing-customer chats convert far higher
  and would distort the shop ranking.
- **Posts** and **ad spend** are per **market**, not per shop: a shop shows its market's posts last week
  and this week, and its market's ad spend that week. Posts lead sales by about a week.
- Weeks are **Sunday to Saturday**.

## Data traps (said on the page)

1. **Count looks low:** a shop-week with conversion **> 80%** or more walk-in orders than visitors —
   visitors are under-counted (Eldoret, Nakuru, Meru run 85–93% over Jul–Oct). Fix counting before
   judging the shop.
2. **Hilton:** about 17,000 visitors in 3.5 months — mall or event traffic, not shop visitors. Flagged,
   and its conversion is shown apart from the ranking.
3. **Bulk orders:** large orders (Kakamega, Uganda, Dar-es-Alam) inflate revenue per visitor — taken out
   by the 10+ unit rule and listed.
4. **Not counted:** a day with walk-in orders but no count is listed as "not counted", never as 0 visitors.

## Correlations ("Posts and ads vs visitors")

Per market, over shop-weeks (Pearson r): (a) the market's posts **last week** vs this week's visitors,
(b) the market's ad spend that week vs visitors, and the same two against walk-in orders. Only shop-weeks
with a count and without the "count looks low" flag; Hilton left out. Stated in plain words
("no link", "weak", "moderate", "strong", with the sign) and the number of shop-weeks. Ads cover only the
weeks in `data/ads_weekly.csv`.

## What the page shows

1. **Tiles** (last complete week, each week on week): visitors, walk-in conversion, revenue per visitor,
   WhatsApp ad-lead conversion.
2. **Shop week on week** (shop selector): visitors and walk-in orders per week (bars + line, one axis).
   A separate chart below: that shop's market posts and ad spend per week (each on its own small chart,
   never a second y-axis).
3. **Shop ranking** (last 4 complete weeks): visitors, walk-in orders, conversion, revenue per visitor,
   WhatsApp ad leads, their conversion, median first reply, flags.
4. **Posts and ads vs visitors:** the correlations in plain words.
5. **Data quality:** low-count shop-weeks, Hilton, not-counted days, bulk orders.
6. **What we can do:** the actions below.

## Actions (rules)

- **High traffic, low conversion:** visitors above the median shop and conversion in the bottom third
  (counted shops only) → staff or stock problem at the door.
- **Fast WhatsApp, few walk-ins:** median first reply ≤ 2 min and paid-ad conversion above the median, but
  walk-in orders falling week on week → the online push isn't reaching the shop.
- **Posts or ads didn't lift visitors:** a market whose posts or ad spend rose week on week while its
  visitors next week fell → rethink that spend.
- **Fix counting first:** a shop with 2+ "count looks low" weeks in the last 4 → its conversion can't be
  judged until the count is fixed.
- **Bulk orders:** a shop whose revenue per visitor moves by > 25% when bulk orders are removed.

Each action names the shop or market, the numbers and the week.

## Regenerate

```
python generators/footfall_marketing.py
```
