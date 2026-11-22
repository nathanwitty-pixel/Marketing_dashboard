# Weekly Report

- **Generator:** `weekly_report.py`
- **HTML:** `weekly_report.html`
- **Data markers:** `<!-- WR_DATA_START -->…<!-- WR_DATA_END -->` (const `WR`)
- **Reads:** the built `current_performance.html` (its `PERF` / `PROJ` blocks, so the figures match the page) and
  Odoo (daily till bags, Kenya's Meta account sync, WhatsApp chats, footfall)
- **Menu:** Performance › Weekly Report (`dashboard_pages.json`)

## Two reports in one page: Marketing and Sales (23 Nov 2026, user's call)

A toggle at the top of the page, **Marketing report | Sales report**, switches between two decks built from the same
slides. Each deck has its own cover ("Weekly Marketing Report" / "Weekly Sales Report", the report week, the owner,
its own contents list) and its own slide numbers; **Print / Save as PDF prints the deck on screen**. The choice is
remembered per browser (`localStorage`, key `wr-deck`) and can be opened directly with `#sales` / `#marketing`.
`WR.decks = {marketing: [slide ids], sales: [slide ids]}` (built by `generators/weekly_report.py`); a slide in both
decks is drawn once and moved into place.

**Marketing deck:** as before (Sales this month, followers slides, follower test, Product Performance, New Products,
combos, offer types).

**Sales deck**, in order (`lib/weekly_sales.py` builds the sales-only slides from the built Current Performance page,
`PERF` / `PROJ`, so the figures match it; no extra Odoo query):
1. **Current Performance: Sales (Odoo, this month) and Sales vs Monthly Target**: the shared Sales slide.
2. **Weekly Performance, Week 1 to latest** (`PROJ.weeklyHistory`, this month's weeks to the report week): bars of
   each week's bags (shop tills + corporate, stacked) against the weekly floor (`PROJ.bareMinimum`, line); table:
   week, bags, corporate, % of the target that week, cumulative %, vs the floor, last month's same week
   (`PERF.cpPrevWeekly`, % of last month's target). Headline / Do next: `PROJ.beats.weekly`.
3. **Why Did We Move? Week on week vs month on month** (`PROJ.whyMoved`): two charts side by side, the change in bags
   per region (green up, red down): **week on week** = the report week vs the week before (`weeks[]`, shop rows summed
   to regions; a selling-days bar when the weeks differ in length), **month on month** = the same days last month vs this
   month (`mom.with`: then, now, days effect, regions). Insight: the shops behind the biggest moves. Do next: the
   page's rule (a region fell → check stock, staff and offers at its top two falling shops; a region rose → copy what
   its top shops did).
4. **What if…** (the page's What-if card as fixed scenarios): the month end at the current pace (`PROJ` forecast) and
   with **+100, +200, +300, +500 bags a day** for the days left, each with its % of the bag target and the revenue at
   this month's price per bag (`priceMix.actualPpb`), plus **what 100% takes** (bags a day on top of the pace).
   Graph: one bar per scenario against the target line.
5. **Price per Bag: operating above the target price** (`PROJ.priceMix`): target price (revenue target ÷ bag target),
   actual price (single bags and combos, after discounts), the gap, bags still to sell for the revenue target at the
   actual price, bags % vs revenue % of target. Graph: price per bag per offer type (`priceMix.offerMix.rows`) against
   the target price (green above, red below), labelled with the price and its gap; gift bags and samples left out (not
   sold at the target price). Insight: the biggest lift and drag
   (`effectKes` by month end). Do next: `PROJ.beats.price.rec`.
6. **Corporate by Client** (`PERF.corporateClients`, `corporateTarget`, `corporateBeat`): totals strip (bags sold,
   KES received, % of the corporate KES target, bags quoted and not invoiced); graph: the top clients by bags sold this
   month plus open quotes (bar = sold, light = quoted, not invoiced); Insight: biggest clients, open quotes, balances owed (agreed −
   received). Headline / Do next: `PERF.corporateBeat`.
7. Then the shared slides, the marketing way: **Product Performance** (Kenya, Uganda, Tanzania), **New Products**,
   **Combos and offers** (power deals included) and **Offer types, all of Denri** (the Bags On vs Off Offer list).

**Sales deck refinements (23 Nov 2026, user's call):**
- **Why Did We Move?:** the week-on-week side shows **every week of the month** (Wk 1, Wk 2, Wk 3, Wk 4 when it has
  days): bags per region per week (grouped bars), each bar labelled with its bags and its growth on the week before
  (Wk 1 against the last week of the month before), green up / red down. The month-on-month side is unchanged.
- **What if…:** says what the extra is added to: the forecast's own pace for the days left (forecast bags − bags so
  far, ÷ days left; the weekday pattern), e.g. "+100 a day (580 → 680 a day)", next to the pace so far (bags so far ÷
  days done).
- **Price per Bag:** **offers working** = the offer types the committee runs (Power deals, Combos, Deal of wk,
  Mid-month offers) selling at or above the target price, "2 of 4 (50%)", and the individual offers inside them
  (`offerMix.rows[].items`, each with its own gap) at or above the target price, "35 of 58 (60%)". Each offer type's
  bar ends with its "n of m working". Do next: review the offer types below the target price.
- **Corporate by Client:** two panels, **Corporate app** (as before) and **paid at the shops** (`PERF.shopCorporate`:
  Corporate-team clients paying at a shop till, their bags paid and quoted, the shop, balances), each with its own
  totals strip; Insight adds the shop side and its balances owed.
- **Male vs female bags (both decks):** the headline counts **every bag by who bought it**, unisex included ("Women
  bought 68% of Kenya's bags last week: 2,825 vs 1,312 by men"), then the bag-type comparison.

## What it is (22 Nov 2026, user's call)

The marketing report handed in every week, built as slides. Every slide hits three beats, the business-strategy
"drum beat": **B1 Headline** (the takeaway as one sentence with its number), **B2 Evidence** (the graph),
**B3 Business recommendation** (the action, starting with a verb). Never "this graph shows…".

Each slide has the same layout:

```
┌──────────────── Headline ────────────────┐
│                      │      Insight      │
│        Graph         ├───────────────────┤
│                      │      Biz Rec      │
└──────────────────────┴───────────────────┘
```

- **Headline** across the top. **Graph** on the left, about 60% of the width. **Insight** on the right, top: two to four
  short facts behind the headline, with their numbers. **Biz Rec** on the right, bottom: one to three actions.
- **Print / Save as PDF** prints one slide per landscape A4 page, so the PDF is the report to submit. Light paper colours
  in print whatever the screen theme.
- A cover slide comes first: "Weekly Marketing Report", the report week, the build time and the page owner
  (`dashboard_pages.json › owner`).

**The report week** is the last complete Sun–Sat week (built on Sun 22 Nov 2026 → Sun 15 to Sat 21 Nov).
Month-to-date slides say "as of" the build date, the same moment as Current Performance.

The report grows one menu at a time. It starts with Performance › Current Performance.

## Slide 1: Sales this month (the Sales card and its hover)

The Sales card ("Sales, Odoo, this month") and what its hover shows (sales vs the month's target, this week's growth %,
the previous % achieved, corporate by client).

- **Headline:** where the month lands in **bags and revenue** (23 Nov 2026, user's call): "November is on course for
  about 18,300 bags (55% of the 33,313 target) and KES 36.8M (55% of the KES 66.6M revenue target)." Bags from
  `PROJ.beats.summary`, revenue from `PROJ.forecastedRevenue` / `forecastedRevenuePct` / `revenueTarget` (the Forward
  Projections revenue card). Red when either is under 90%.
- **Graph:** bags sold to date, day by day, cumulative: **this month** (solid), **last month** to the same day (dashed),
  and the **target pace** (a straight line from 0 to the month's target on the last day). **Projection** (23 Nov 2026,
  user's call): a dashed blue line from this month's last day to month end, ending at Forward Projections' till figure
  (`PROJ.pace.soFar.bags + restBags` = `projBags`); each remaining day adds its share of `restBags` by the weekday
  pattern (`pace.weekdays`), so it bends like a real month. It is the tills only: the headline's figure adds corporate. Till bags from
  `BAGS_SOLD_DAILY` (all shops, refunds netted, the Sales card's rules); corporate bags are added on top in the Insight,
  not drawn, because corporate is booked on the payment date.
- **Insight:**
  - Sold so far: `PERF.sales` bags (`salesPos` at the tills + `corporateBags` corporate) = `salesPctAchieved` of the
    target, with the share of the month gone.
  - Last complete week: its bags and the points of the target it added (`PROJ.weeklyHistory`, the week ending on the
    report week's Saturday: `salesPct` − `prevSalesPct`).
  - Last month at the same day: its cumulative bags vs this month's, as a %.
  - Revenue so far: `PROJ.pace.soFar` till KES + corporate KES, as % of the revenue target, and the price per bag
    (`PROJ.beats.price.headline`).
  - Corporate: `PERF.corporateBeat.headline`.
- **Biz Rec:** `PROJ.beats.summary.rec`, then `PROJ.beats.projections.rec` (bags vs revenue: volume, or discounts and
  the offer mix), then `PERF.corporateBeat.rec`.

## Slide 2: Did new followers sell bags? (Kenya)

Answers "when follows go up, do we sell more, or is it awareness?" with Kenya only (Kenya's Facebook page and Instagram
account, market `KE`, against Kenya's shop tills, Sinza and Uganda left out).

- **Days compared:** from the first day both platforms report new follows (20 Oct 2026) to the report week's Saturday.
- **Weeks drawn:** Sun–Sat weeks where both platforms have all 7 days (from 25 Oct 2026).
- **Graph:** per week, Kenya till bags (bars, left axis) with new follows (Instagram + Facebook) and WhatsApp chats
  (lines, right axis).
- **Match score (day level):** each day's figure is divided by the average for that weekday (so Saturdays aren't
  compared with Mondays), then a rank correlation (Spearman) is taken between that and the same day's till bags.
  From 0 (no link) to 1 (move together). Worked out for new follows, WhatsApp chats and shop visitors
  (footfall, Kenya, Hilton left out).
- **Top follow days:** the quarter of days with the most new follows (weekday-adjusted): their bags vs a normal day for
  that weekday, the same day and the day after.
- **Headline (rule):** follows' match score under **0.3** → "New follows rose/fell X% last week while Kenya shop sales
  rose/fell Y%: follows are building awareness, not this week's sales." **0.3 or more** → "Days with more new follows
  sold more: …". `LINK` in `generators/weekly_report.py`.
- **Insight:** last week vs the week before (follows, bags, WhatsApp chats); the top-follow-days result; the three match
  scores in words; "a match isn't proof: a launch or an offer can lift both".
- **Biz Rec (rule):** no link → judge Meta posts and ads by WhatsApp chats and cost per chat, not follows; keep follows
  as the brand-growth figure. A platform whose follows fell more than 30% → find out why. Fewer than 12 weeks of
  history → check again on the date it reaches 12 weeks. Link found → repeat what went out on the top follow days.

### Slide 2b: Followers vs sales, Sinza and Uganda (23 Nov 2026, user's call)

Right after the Kenya slide, the same question for Sinza (market `TZ`, the `sinza` + `dar-es-alam` tills) and Uganda
(`UG`, the `uganda` till). Their pages joined Odoo's Meta sync on 10–11 Nov 2026, so the slide works **day by day**
from the first day both platforms report new follows for that market.

- **Graph:** two panels, one per market: bags at its till each day (bars), shop visitors counted (dashed line, left
  axis; a gap = not counted) and new follows, Instagram + Facebook (line, right axis).
- **Visitors (22 Nov 2026, user's call):** footfall for the market's shop (`DAR-ES-ALAM` for Sinza, `UGANDA`), from
  `lib/footfall.daily`, the Kenya slide's source. A 0 count on a day with walk-in sales is "not counted", the Denri
  dashboard's Foot Traffic rule. The insight gives last week's visitors with the days counted, and a second day-level
  match score, visitors vs bags.
- **Insight, per market:** followers now (Instagram, Facebook); last week's new follows, Instagram reach and views
  (vs the week before only when the market has all 7 days before); its till's bags last week (vs the week before);
  its WhatsApp chats (`denri_monitor_interaction`, shop Sinza / Uganda); the day-level match score between new follows
  and bags (rank correlation, no weekday adjustment: too few days), always with the number of days.
- **Headline (rule):** fewer than **28 days** → "too early to link follows to sales"; else Kenya's rule (`LINK`).
- **Biz Rec:** judge by WhatsApp chats; check again on the date the market reaches 12 weeks of history.

### Foot traffic band (22 Nov 2026, user's call)

On both Followers vs sales slides, a band under the headline: last week's figures from the Denri dashboard's Foot
Traffic page, per market (Kenya; Sinza and Uganda side by side), with the page's own labels. Data:
`lib/foot_traffic.py` (ported from Denri-dashboard `lib/footfall.py`, `queries.FOOTFALL_COUNTS / FOOTFALL_SALES /
WA_SHOP_KPIS`; keep them in step).

- **Walk-ins** (the people who came into the shops): walk-ins counted, purchased walk-ins, didn't buy, walk-in
  conversion, revenue per walk-in. Counted days only; a 0 beside walk-in sales is "not counted".
- **Not walk-ins** (orders that are not part of the conversion): online orders, activation & employee, refunds, days
  not counted, undercounted days.
- **WhatsApp** (chats handled by every shop of the market, from the WhatsApp Monitor): performance, ads, avg response.
- Market: Sinza (Dar-Es-Alam) → Sinza, Uganda → Uganda, every other shop → Kenya. Hilton is left out of Kenya's
  walk-ins (mall traffic), as on the chart.

### Kenya: insight and recommendation read the band with the chart (23 Nov 2026, user's call)

The Kenya slide's headline, insight and recommendation follow **one path from a follow to a sale**, using the chart
(new follows, WhatsApp chats, bags) and the Foot traffic band (walk-ins, conversion, WhatsApp buyers) for last week
and the week before (`foot_traffic.summary` for both weeks):

- **Online path:** new follows → WhatsApp chats (from ads) → WhatsApp buyers (performance %).
- **Shop path:** walk-ins counted → walk-in buyers (conversion %) and the walk-ins who didn't buy.
- **Headline:** the bags and their change, then the two paths' buyer changes, bigger one first, then follows:
  "Kenya sold 4,196 bags last week (-3%): the shops gained 147 walk-in buyers while WhatsApp lost 197; new follows
  fell 55% and didn't move sales."
- **Insight:** (1) online path with each step's change; (2) shop path with each step's change and the walk-ins who
  left without buying; (3) day by day, sales follow shop visitors and WhatsApp chats, not follows (match scores);
  (4) what 5 more points of walk-in conversion are worth: counted walk-ins × 5% buyers × the average walk-in sale
  (revenue per walk-in × counted ÷ purchased).
- **Biz Rec (rules, three at most):** WhatsApp buyers down 10% or more, or performance down 2 points or more →
  follow up the chats that didn't buy and check the ad chats (count, % bought); walk-ins who didn't buy → work on
  them shop by shop (Footfall and Marketing ranks the shops), with the 5-point value; follows → judge posts and ads
  by the WhatsApp chats and buyers they bring, with the check-again date while history is short.

### WhatsApp buyers by source (23 Nov 2026, user's call)

Answers "did the new followers become WhatsApp chats that bought?". Meta gives follower counts, not who followed, so
the link is read from where each chat came from (`denri_monitor_interaction.source_id` → `denri_monitor_source`):
the **social pages** (Social DMs, Direct IG: people who messaged from the Instagram / Facebook page) are the follower
path. Per market (Kenya = every shop but Sinza and Uganda; Sinza; Uganda), last week vs the week before.

| Source in the monitor | Shown as |
|---|---|
| Existing Direct | Returning customers |
| New Direct | New customers |
| Social DMs, Direct IG | Social pages (follower path) |
| Meta Ad - Facebook / Instagram / Twitter, Status Ads | Facebook ads, Instagram ads, X ads, WhatsApp Status ads |
| Web Check Out, Walk-in, Shop Transfer | Website checkout, Walk-in, Shop transfer |

- **Table under the chart:** Kenya: Source, Chats, Bought, Bought the week before, Change (most buyers first).
  Sinza and Uganda: one table, Source, then Bought (change) for each market.
- **Insight:** the follower path's buyers and their share of the market's WhatsApp buyers; the source with the
  biggest change in buyers.
- **Biz Rec (replaces the general WhatsApp line):** the source that lost the most buyers (5 or more) → returning
  customers: re-contact last month's buyers (broadcast, new arrivals, offers); new customers: check the reply and
  follow-up of first-time chats; an ad source: check that ad's budget and creatives; social pages: answer page DMs
  faster and point posts to WhatsApp. No source lost 5 → keep what is working.

### Follower test: does a new follower become a sale? (23 Nov 2026, user's call)

One slide after the two Followers vs sales slides, Kenya, Sinza and Uganda, that pins the three metrics together:
**new follows** (Instagram + Facebook), **WhatsApp chats** (every source, the market's shops) and **bags** (the market's
tills). `lib/follower_test.py`, pure function, no DB.

- **Days:** from the first day both platforms report new follows for the market to the report Saturday. Each figure is
  divided by its weekday's average (so a busy Saturday isn't read as a follower effect).
- **Three links**, each a rank correlation (Spearman) at the best of a few day lags:
  1. **Follows → Chats:** follows on a day vs chats the same day up to 3 days later.
  2. **Chats → Bags:** chats vs bags the same day up to 2 days later.
  3. **Follows → Bags (awareness):** follows vs bags the same day up to 7 days later.
- **Passed** = score **0.3 or more** and a **chance test** under 5%: the follows (or chats) are shuffled 2,000 times and
  the best score over the same lags is worked out each time; p = the share of shuffles that score as high. Picking the
  best lag is part of the shuffle, so it isn't an unfair advantage. `LINK`, `P_MAX`, `MIN_DAYS = 28`.
- **Verdict (the gate):**

| Links passed | Verdict |
|---|---|
| fewer than 28 days | Too early: the test runs from the date the market reaches 28 days |
| 1 and 2 | Followers buy through WhatsApp: follows bring chats and the chats sell |
| 3 (not 1) | Awareness: follows lift sales N days later, but not through WhatsApp chats |
| 1, not 2 | Follows bring chats that don't buy: fix the chat follow-up |
| none | Not yet: follows are brand growth only, judge Meta by chats and buyers |

- **Graph:** per market, three boxes (Follows, WhatsApp chats, Bags) joined by arrows: Follows → Chats → Bags along
  the top and the awareness arrow Follows → Bags underneath. Each arrow shows pass (green) / fail (grey), the score,
  the lag and the chance. The verdict sits beside the market's name.
- **Headline:** Kenya's verdict. **Insight:** each link in words, per market. **Biz Rec:** from the verdict.

### What it found first (22 Nov 2026)

Over 33 days (20 Oct to 21 Nov) Kenya's new follows had no day-level link with Kenya's till sales; sales moved with shop
visitors and, partly, WhatsApp chats. The one day with a big jump in both (Sun 8 Nov: 515 follows, sales twice a normal
Sunday) was Nyeri's opening, which lifted both. The 26–29 Oct Facebook burst (up to 303 follows a day) came with
sales below a normal day. Reading: follows are awareness for now.

## Product Performance slides (23 Nov 2026, user's call)

After the Performance slides: three slides per market, **Kenya first, then Uganda, then Tanzania (Sinza)**
(markets `KE`, `UG`, `TZ`, the Product Performance page's split: Sinza = `sinza` + `dar-es-alam` tills, Uganda =
`uganda`, Kenya = every other till, Website included). Units are bags, combos' bags included, gift bags and samples
counted, refunds netted: the page's own rules, from `product_performance.load_lines()` (one Odoo pull from the first
day of the same days last month to the report Saturday). Stock now, category, offers and posts come from the built
`product_performance.html` (`PP.info`), the "why it moved" lines from `PP.why`.

### A. Bag of the Month: week by week vs the whole month

- **Period:** the 1st of the report Saturday's month to that Saturday (Sun 1 to Sat 21 Nov), split into its Sun–Sat
  weeks (Wk 1 = the 1st to the first Saturday, so it can be short), vs the same days last month.
- **Bags:** the **top seller** (most units in the month so far) and the **biggest mover** (biggest rise in units vs the
  same days last month, bulk orders aside: POS lines of 10+ units left out; at least 10 units a week of the period in Kenya, **3** in Sinza and Uganda (23 Nov 2026, user's call: their
  shops sell about 50 to 130 bags a week, so 10 left them with no mover; `MOVER_MIN_WEEK`);
  not the top seller).
- **Graph:** one bar per week for each of the two bags, with a dotted line at each bag's **month average a week**, so
  each week reads against the whole month.
- **Each week's own leaders (23 Nov 2026, user's call):** the month's bags may not have led every week, so each week
  gets its own **top seller** (most units that week) and **biggest mover** (biggest rise vs the 7 days before, bulk
  orders aside, at least the market's minimum a week (10 Kenya, 3 Sinza and Uganda) scaled to the week's length, not that week's top seller), plus the month's pair as
  the last row. A table under the chart: Week, Top seller (units), Biggest mover (before → after). A week whose
  leader isn't the month's is marked, and the Insight says which bag led which week ("the lead changed hands").
  **On the chart too (23 Nov 2026, user's call):** a third bar per week, amber, *That week's biggest mover*, named on the
  bar ("Sarai 109"); hover gives the week before → that week. When a week was led by a bag other than the month's top
  seller (common in Sinza and Uganda), a teal bar *That week's top seller* is added for that week, named the same way,
  so every market's chart compares the month's pair with each week's own leaders.
- **Headline:** "JUMBO is Kenya's Bag of the Month: 1,068 bags from 1 to 21 Nov (8.4% of units), +49% on the same
  days of October."
- **Insight:** each week's units (Wk 1, Wk 2, Wk 3) against the month average; the whole month (units, share,
  revenue, vs last month); why it moved (`PP.why.monthly[mkt][bag].head` and its support verdict); stock now and
  weeks of cover at last week's pace. The same for the mover, shorter.
- **Biz Rec (rules):** cover under **2 weeks** → "Restock X: N in the shops is about W weeks at last week's pace."
  Last week more than **20%** under the month average → "X is slowing: …, check stock by shop and its posts." Verdict
  *Demand problem* → check price / design; *Support pulled* → put back its offer and posts; *Working* → keep its offer
  and posts running; *Selling on its own* → give it more posts. `COVER_WEEKS`, `SLOWING` in the generator.

### B. Top-selling bags: the top 10 moving and the 5 stuck

- **Period:** the report week (last week), vs the week before.
- **Top 10:** the 10 bags with the most units, each with its % share of the market's units and the change in share
  (pp). **Stuck 5:** bags with at least **30** (Kenya) or **10** (Uganda, Tanzania) in the market's shops now (`PP.info[bag].stock`) ranked by weeks of cover
  (stock ÷ units sold last week, a bag that sold none counts as selling 1), top 5, top-10 bags left out.
- **Graph:** two horizontal bar charts: top 10 by units (share on the bar), and the stuck 5 as shop stock with the units
  sold last week beside it.
- **Headline:** "The top 10 bags carried X% of Kenya's units last week, led by JUMBO (N, s%); 5 bags hold S bags in
  the shops but sold only U."
- **Insight:** biggest share gain and loss in the top 10; any top-10 bag under 2 weeks of cover; the stuck 5's stock and
  weeks of cover.
- **Biz Rec:** restock the top-10 bags under 2 weeks of cover; for the stuck 5, the page's bottom-bag rule: not posted
  this month → *post it first*; not on offer → *put it on an offer or in a combo with its category's top seller*; on
  offer and still slow → *check price or design, or clear it*.

### C. Top 5 categories: best and weakest bags

- **Period:** the report week. Category = `PP.info[bag].cat` (the page's catalogue category), else OTHER.
- **Graph:** the top 5 categories by units, last week vs the week before (grouped bars), share on the bar.
- **Insight:** per category: its share and bags (change on the week before), its **best bag** (most units last week)
  and its **weakest bag** in the same light as the stuck 5: the category's bag with at least 30 (Kenya) / 10 (Uganda,
  Tanzania) in the shops and the most weeks of cover (it can have sold none); when none has that much stock, its
  lowest seller. Both with stock now.
- **3 to 5 weakest bags (23 Nov 2026, user's call):** each category lists up to **5** weakest bags: its bags with the
  stuck-stock minimum in the shops and at least **6 weeks of cover** at last week's pace (`WEAK_COVER`, the Product Performance page's overstock rule; so a big
  seller holding big stock isn't called weak), not its best bag, most weeks of cover first; when fewer than **3** have that much
  stock, the lowest sellers (sold at least 1) fill it to 3. They sit in a **table under the chart**: Category, Best bag
  (sold, in shops), Weakest bags (sold / in shops each). The Insight keeps one short line per category: share, change,
  best bag, and what the weakest hold in the shops against what they sold. `WEAK_MIN = 3`, `WEAK_MAX = 5`.
- **Headline:** "BACKPACK is Kenya's biggest category last week (X% of units); its weakest bag, Y, sold N with S in
  the shops."
- **Biz Rec:** the page's suggestions (docs/product-performance.md › Top 5 categories): best bags with stock below what
  they sold → *restock*; weakest bags with the most stock → the bottom-bag rule above. Two or three lines at most.

### D. Male vs female bags (23 Nov 2026, user's call)

Which side tops: bags for men vs bags for women, per market.

- **Who a bag is for:** `data/bag_gender.csv` (editable, no code change): a **category** row sets the default for its
  category, a **bag** row overrides it for one bag type. `Male`, `Female` or `Unisex`; a category not in the file is
  Unisex; gift bags are left out. First version (23 Nov 2026, Claude's starting list, **to be checked by the user**):
  Male = Man Bag, Briefcase; Female = Handbag, Sling, Messenger, Baby Bag, Make Up, Thigh Bag; the rest Unisex
  (Travel, Backpack, School Bag, Chest Bag, Sport, Waist Bag, Lunch Bag, Washbag…). Read by `lib/bag_gender.py`.
- **Graph:** units per Sun–Sat week of the month (Wk 1, Wk 2, Wk 3) for Male, Female and Unisex, side by side, with
  each week's share on the bar.
- **Who bought them (23 Nov 2026, user's call):** each bag type's bar is **split by the buyer's gender in Odoo**
  (`res_partner.gender` of the order's customer, the Who buys slide's lines: female = pink, male = blue, corporate and
  blank left out, so the stacks can be a little under the bag totals). "Unisex" describes the bag, not the buyer: Odoo
  knows who bought every unisex bag (Kenya, November 2026: 63% women). Each part carries its own % **inside** it
  (women's % in the pink part, men's % in the blue part; left out when the part is too small to hold it), and the
  bar's total bags sit on top. Insight adds one line per bag type: bought by women vs men, last week and month to date.
  Biz Rec: male bags bought 50%+ by women → show them to women as gifts; female bags bought 40%+ by men → show them
  to men too.
- **Headline:** last week, "Female bags outsold male bags in Kenya last week: 1,520 vs 610 (36% vs 15% of units)"
  (or the other way round), with the change in each side's share vs the week before.
- **Insight:** each side's units and share last week vs the week before; its top 3 bags last week (units); the month
  so far.
- **Biz Rec:** a side whose share fell **2 points or more** vs the week before → "Push the male / female range: …,
  feature its top bag"; each side's top bag under 2 weeks of stock → restock. Otherwise keep the mix.

### E. Who buys: women vs men (23 Nov 2026, user's call)

The buyer's gender as Odoo records it: every till order has a customer (`pos_order.partner_id`), and the customer's
`res_partner.gender` is `female`, `male` or `corporate` (November 2026: 6,940 female orders, 3,580 male, 15 corporate).
Corporate and blank are left out. Only counts leave Odoo: no customer name goes into the report.

- **Lines:** the Product Performance sales lines (`product_performance.LINES_SQL`, its bag rules: combo bags counted,
  the combo wrapper not, refunds netted) with the order's customer gender added; bag type = the page's fold.
- **Period:** the month to the report Saturday (enough sales for a stable top 10), and each Sun–Sat week for the split.
- **Graph:** two bar charts, **bags women lean to** and **bags men lean to**: the 10 bags with the highest share of women
  (men) among their buyers, judged only with at least 30 bags with a buyer's gender in the month (Kenya; 4 in Sinza
  and Uganda); units that side bought and its share at the end. (First version showed the top 10 by units for each
  side: both lists were Jumbo, Code 3, Antitheft, because women buy two thirds of everything.) The three best sellers
  overall are one Insight line with their % women, against the market's overall % women.
- **Headline:** "Women bought 67% of Kenya's bags this month (8,343 vs 4,076 by men); women lean most to X (n% women),
  men to Y (n% men)."
- **Insight:** the women's share week by week (Wk 1, Wk 2, Wk 3); **crossovers**: bags the male / female list in
  `bag_gender.csv` gives to one side that the other side buys most (e.g. a "male" bag bought 60% by women = bought
  as a gift); the bags closest to 50/50.
- **Biz Rec:** aim each top bag's posts and ads at the side that buys it; for crossovers, show them to that side
  ("Show Man Bag to women as a gift"); a side whose share fell 3 points or more week on week → check what changed.

Uganda and Tanzania sell far fewer bags, so a week can hold a single sale per bag: the slides say so when the market
sold under 100 bags in the week.

## Combos and offers slides (23 Nov 2026, user's call)

After the New Products slides. Built by `lib/weekly_combos.py`. Weeks = Sun–Sat weeks of the month (Wk 1 starts on the
1st, as on the combos and offer pages); **week on week** = the report week vs the week before; **month to date** = the
1st to the report Saturday. KES everywhere (Sinza ÷ 25, Uganda ÷ 29).

**One slide per market, Kenya, then Sinza, then Uganda: running combos vs self-made combos vs power deals.**
- **Kenya combos:** every combo line on the Kenya tills (`product_performance.LINES_SQL`, wrapper lines = the combo
  product, one per combo sold; refunds netted). **Self-made** = the product is in the Self-made Combos page's list for
  the month (`SMC.selfMade`, the page's offer-list matching), else **running**. Checked 23 Nov 2026: running per week
  = the page's running cards (188, 193, 142), running + self-made = `combosGoal.weeklyDetail.cur` (238, 231, 166).
- **Kenya power deals:** the Bags On vs Off Offer page's **Power deals** row per week (`BOO.periods.monthly
  .offerTypesByWeek`, Kenya single sales counted as Power Deal), bags and KES.
- **Sinza and Uganda:** combos counted from receipts (`lib/receipt_combos.market_summary`, the combos page's method:
  bags sharing one unit price on a receipt = a combo; on the month's list = running, else self-made). They have **no
  power deals**, so the third measure is their **listed single offers** (`singlesOffer`).
- **Graph:** per week, running and self-made combos (bars, left axis) and power deals / listed singles (line, right
  axis), with a table under it: measure, Wk 1, Wk 2, Wk 3, month to date, KES month to date, week on week.
- **Headline:** combos last week and the change, running vs self-made, then power deals (or listed singles).
- **Insight:** self-made share of combos; top running and top self-made combo last week; power deals' top deal last
  week (Kenya); revenue month to date.
- **Biz Rec:** running down 15% or more week on week → push the running list (the one that fell most); a self-made pairing
  sold 5+ times this month (Kenya; 3+ Sinza / Uganda) → consider making it an official combo; power deals down 15% or
  more → check their stock and display.

**Then one slide for the whole of Denri (Kenya + Sinza + Uganda): offer types.** The Bags On vs Off Offer page's offer
type rows (Not on offer, Power deals, Combos, Deal of wk, Corporate, Mid-month offers, Samples, Gift bags, Total) per
week of the month (`offerTypesByWeek`, all three countries). Graph (23 Nov 2026, user's call: was one stacked revenue bar per week, hard to compare): **two charts side by side, money (KES) and bags sold**, one row per offer type with one bar per week (Wk 1 lightest, the report week darkest); **every** week's bar is labelled with its value and its growth on the week before ("3.1M +2%", "2.5M -12%"; green up, red down; Wk 1 has no growth). Shares and month totals are in the headline and Insight. No table under them (the charts need the room); shares are in the Insight. Table:
offer type, Wk 1…, month to date bags and KES, share of revenue, week on week (KES). Headline: what share of revenue
came on offer vs not on offer month to date, and last week's change. Insight: biggest rise and fall last week; the
on-offer share week by week. Biz Rec: the offer type that fell most → check it; not on offer under 40% of revenue →
watch the discount cost.

## New Products slides (23 Nov 2026, user's call)

After the Product Performance slides, five slides from the New Products Analytics menu (docs/new-products.md), all
markets together as on that page. **The products** = `NP.productNames` (`data/new_products.txt`); **targets** =
`NP.productTargets`; **stock** = the page's per-colour stock (`NP.monthlyCombined`: Kenya shops + Sinza and Uganda).
Sales per week and per shop come from `product_performance.load_lines()` (the dashboard's bag rules, combo bags
included) up to the report Saturday; the Corporate app's bags (CORP) come from `NP.shopSales`. Built by
`lib/weekly_newproducts.py`.

1. **Month to date and week by week.** Graph: new-product bags per Sun–Sat week of the month (bars) against the
   weekly target (`NP.weeklyTarget`, line), with a table under it: product, Wk 1, Wk 2, Wk 3, month to date, target,
   % of target, **highest % of target first** (23 Nov 2026, user's call; ties by bags sold), Total last. Headline: sold vs target with the share of the month gone, and last week vs the week before.
   Insight: best and worst product by % of target, the biggest rise and fall last week, last week's posts
   (`NP.weeklyPostsHistory`). Biz Rec: bags a day needed for the target; push the product with the most still needed
   that has stock; post more when posts fell.
2. **Runway Bags Sold: last month's runway styles (23 Nov 2026, user's call).** Not the page's last-30-days list:
   styles created days ago aren't checked and in the shops yet, so the report follows the styles **first created in
   Odoo in the previous calendar month** (October for a November report), via `lib/runway_bags.runway_bags()`
   (same fold, same exclusions, New Products left out) with that month as the window. For each style: sold **this month**
   (to the report Saturday), **last week**, **the week before**, **since created**, created date and stock now (Kenya
   shops, Sinza + Uganda), from `runway_bags.sold_by_type()` / `stock_by_type()`. Graph: this month per style (bars),
   last week vs the week before at the end. Headline: what last month's styles sold this month and the leader.
   **Stock check (23 Nov 2026, user's call):** each style is one of
   - **Cleared**: sold, and no stock left in the shops: marketing and sales did a good job; decide whether to reorder.
   - **In stock, selling**: still in the shops and sold this month.
   - **In stock, not selling**: in the shops, nothing sold this month.
   The bar is coloured by it (green cleared, blue selling, amber not selling) and the end label says "cleared" or the
   stock. Biz Rec: name the cleared styles (good job, reorder?); for **every** style still in stock, marketing shoots at
   least a short video and shows it online in a **Runway** segment (a regular "new on the runway" slot), so the one
   buyer who wants it sees it; the ones not selling first.
3. **Sales by Shop, week to week and month to date.** Graph: new-product bags per shop, last week vs the week before
   (grouped bars), month to date at the bar end; shop codes as on the page (STR, MSA, HTN…, SNZ = Sinza, UGD = Uganda,
   CORP = Corporate app). Insight: top 3 shops month to date, the biggest rise and fall, shops with no new-bag sale
   last week. Biz Rec: the shops with none → dispatch and post there; copy the top shop.
4. **Sold vs Monthly Target.** Graph: per product, sold (bar) and still needed (light), % of target at the end, and
   where it should be by now (target × share of the month gone). On pace = sold ≥ that. Headline: how many products
   are on pace. Biz Rec: behind with stock → push and post it; behind without stock → restock first.
5. **In stock: could move well vs least performers.** Colour level (product + colour), stock ≥ 5:
   **could move well** = the 5 that sold most this month and still hold at least 2 weeks of last week's pace;
   **least performers** = the 5 with the most weeks of cover (stock ÷ this month's sales, none sold counts as 1).
   Graph: two bar charts (stock vs sold). Biz Rec: push and post the movers; for the least, the page's rule (< 3 posts
   this month → post it; else offer or combo with its bag's best colour).

## Colours for up and down, totals strips (23 Nov 2026, user's call)

Everywhere in the report: **green = up / sold better, red = down**. Chart labels that carry a change ("(+24%)",
"-12%", "9 (was 14)") are drawn green or red; changes written inside bars use the same colours (light shades on dark
bars); in the week-by-week tables (combos, new products) each week's figure is green when it beat the week before and
red when it fell. Charts that compare items (runway styles, shops) carry a **totals strip** above them: the label,
this month, last week, the week before and the week-on-week % (green / red chip), plus since created and stock for the
runway styles.

## Data sources

| Figure | Source |
|---|---|
| Month figures, beats | `html/current_performance.html` (`PERF`, `PROJ`) |
| Daily till bags | `sql/bags_sold_daily.sql`, split by shop for Kenya |
| New follows, reach, views | `denri_meta_account_day`, market `KE` (`lib/odoo_marketing.followers_daily`) |
| WhatsApp chats | `denri_monitor_interaction` (all sources), Sinza and Uganda shops left out |
| Shop visitors | `lib/footfall.daily`, Kenya shops, Hilton left out |

## Regenerate

`python generators/weekly_report.py` (after `current_performance.py` and `forward_projections.py`).
