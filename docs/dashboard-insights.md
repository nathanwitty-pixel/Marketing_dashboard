# Dashboard Insights

- **Generator:** `generate_insights.py`
- **HTML:** `insights.html`

## What the page shows

An auto-written narrative that pulls the numbers **already injected** into the other
dashboard pages and turns them into cross-page insights. **No Google Sheets / Odoo calls
of its own** — it must run **after** every data page.

## Data sources

Reads the injected data blocks out of the other pages' HTML with `read_block(file, start,
end)` and small regex getters:

- `gstr(block, key)` — string fields. The key regex allows an optional `"?` so it matches
  **both** bare JS identifiers (`wkMktPct: "65.8%"`) and quoted json.dumps keys
  (`"szWkMktPct": "15.0%"`) — nested Sinza/Uganda lookups fail silently without it.
- `graw(block, key)` — bare numerics.

Pages read include Current Performance (`PERF`/`PROJ`), New Products (`NEW_PROD`), Self
Made Combos (`OFFER_DATA`), and Posting (`POST_DATA`).

## Gotcha

If Insights shows blanks or zeros for a metric, the usual cause is a **key rename** in a
source page's data block, or running Insights **before** that page was regenerated. Re-run
the source generator, then `generate_insights.py`.

## Regenerate

```
python generate_insights.py       # run AFTER the data pages
```
</content>
</invoke>
