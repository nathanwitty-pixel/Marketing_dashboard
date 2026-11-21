# Menu 1 Current Performance in the 3-beat layout (preview)

**Status:** preview only. Nothing on the page has changed yet. Once you approve this, the rules go into
`docs/current-performance.md` first, then the code.

**The idea, from the "Never tell your VP" video:** no card opens with "this chart shows…". Every card hits three beats:

| Beat | What it is | Where it sits on a card |
| --- | --- | --- |
| **1. Headline** | The takeaway, as a full sentence with the number in it | Replaces the card title as the first line |
| **2. Evidence** | The chart or figures we already have, unchanged | Same place as today |
| **3. Recommendation** | What to do about it, as one line starting with a verb | New line under the chart, in an amber box |

Each card keeps its current name as a small grey label above the headline, so you can still find it.
Headlines and recommendations are **written by the generator from the data** each build. They are
not typed by hand, so they stay true when the numbers move.

Example figures are from today's build (18 Nov 2026, day 18 of 30).

---

## 0. New: an executive summary strip at the top of the page

This is new. It goes above the Sales, Weekly Sales and Remaining cards.

| Beat | Example today |
| --- | --- |
| **Headline** | **November is on course for about 17,800 bags, 54% of the 33,313 target.** |
| **Evidence** | 10,235 sold so far (31%) with 60% of the month gone. 23,078 bags still to sell in 13 days. |
| **Recommendation** | **Reset the month's expectation and push the weekend: we need about 1,775 bags a day against the current ~600.** |

---

## 1. Sales, Weekly Sales and Remaining Target cards

| | Today | After |
| --- | --- | --- |
| Headline | "Sales" / "Weekly Sales" / "Remaining Target" | **"10,235 bags sold: 31% of target with 60% of the month gone"** |
| Evidence | The three cards | Same three cards, same breakdown line (POS, corporate, rejects, gift bags) |
| Recommendation | none | Rule: behind pace → "**Close the gap of X bags a day**". On pace → "**Hold the pace: X a day lands the target**" |

## 2. Followers & Reach

| | Today | After |
| --- | --- | --- |
| Headline | "Followers & Reach — Week on Week" | **"Instagram added +N followers this week (±X% on last week)"**, naming the biggest mover of the four metrics |
| Evidence | Waterfall chart and the three cards | Same |
| Recommendation | none | Rule: biggest day up → "**Repeat what was posted on [day]**". Reach down → "**Post more on [platform]; reach fell X%**" |

## 3. Weekly Performance — Week 1 to Latest

| | Today | After |
| --- | --- | --- |
| Headline | "Weekly Performance — Week 1 to Latest" | **"Last week sold 4,486 bags, X% of target, against Y% in the same week of October"** |
| Evidence | Area / Line / Bar / Radar chart, pills, short-week labels | Same |
| Recommendation | none | Rule: behind October → "**Find what October's week N had that this one doesn't (offers, posts, bulk orders)**". Ahead → "**Keep it going; this week sets the bar**" |

## 4. Why Did We Move?

The amber "The reason" box is already Beat 3 in spirit. It moves to the headline, and a real action is added below.

| | Today | After |
| --- | --- | --- |
| Headline | "Why Did We Move? — Week on Week & Month on Month" | **"Sales fell 251 bags week on week, mostly Nairobi CBD (−700)"**, which is today's reason sentence promoted |
| Evidence | Waterfall, best-week lines, tooltip | Same |
| Recommendation | The reason box (explains, doesn't advise) | Rule: biggest drag region → "**Check [top 2 shops] in [region]: stock, staff, offers**". Bulk-driven → "**Ignore the drop: it's the 500-bag bulk order last week; without bulk we're +274**" |

## 5. Sales vs Monthly Target, Week-over-Week, Bare Minimum

| | Today | After |
| --- | --- | --- |
| Headline | Three card names | **"Week on week: +X% (4,486 → N bags)"** |
| Evidence | Same cards | Same |
| Recommendation | none | Rule: under bare minimum → "**Below the week's minimum by X bags: escalate to shop managers**". Bare minimum unset → no line |

## 6. Forward Projections (Standard and Forecasted)

| | Today | After |
| --- | --- | --- |
| Headline | "Standard Projection" / "Forecasted Projection" | **"Month end: about 17,800 bags (54%) and 54% of revenue target"** |
| Evidence | The two cards with bags, revenue and % | Same |
| Recommendation | none | Rule: projected < 90% → "**Target is out of reach at this pace; decide now on a push (offer, corporate follow-ups)**". 90–100% → "**Within reach: X more bags a day closes it**". ≥100% → "**On track; protect stock on the top sellers**" |

## 7. Price per Bag, and On offer vs not on offer

| | Today | After |
| --- | --- | --- |
| Headline | "Price per Bag — Why the revenue % and the bags % differ" | **"Bags sell at +X% above the target price, so revenue runs ahead of bags"** |
| Evidence | Target vs actual price, the On offer table | Same |
| Recommendation | The verdict line (biggest lift and drag) | Rule: from the biggest drag row → "**[Row] is pulling the price down by KES X; review its discount**" |

## 8. Corporate by Client

| | Today | After |
| --- | --- | --- |
| Headline | "Corporate by Client" | **"Corporate: 105 bags sold, X% of its 1,163 target, with N bags quoted and not yet invoiced"** |
| Evidence | Target strip, charts, client table | Same |
| Recommendation | none | Rule: open quotes → "**Chase [biggest open quote client] (QUO-…, N bags, valid until …)**". Part-paid → "**Collect KES X from [client]**" |

---

## What does not change

- No numbers, SQL or calculations change. Only titles and one new line per card.
- Charts, toggles, tooltips, remembered choices and the Kenya / Sinza / Uganda buttons stay as they are.
- No dot separators: headlines use words and commas.

## Decisions for you

1. **The summary strip at the top (section 0):** add it, or put headlines on the cards only?
2. **The recommendation rules:** are the thresholds right (for example, under 90% projected = "out of reach")?
   Add or remove any action wording.
3. **Old card names:** keep them as a small grey label above the headline, or drop them?
