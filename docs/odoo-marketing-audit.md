# Odoo marketing data audit

Which marketing data in Odoo (the **Marketing OS** app: Home · Sales · Channels · Content · Meta · TikTok · Setup, and
its metric chips) the dashboard could use, and **how complete and up to date** each one is. Not a menu page: a
script you run when you want to know (user, 1 Nov 2026: "show the percentage of data that is there … is it up to
date?").

    python scripts/odoo_marketing_audit.py   # → notes/ODOO_MARKETING_AUDIT.md + data/odoo_marketing_audit.csv

## What it measures, per source

- **Latest data** and **behind by**: the newest date in the table vs the newest it should have:
  daily → yesterday, weekly → the last complete week (weeks start Monday, as Odoo stores them),
  monthly → last month.
- **Filled %** (is it completely entered?): of the periods it should have in the check window, how many have data,
  for every group the table is kept by (shop, country, platform, channel). Groups = those seen in the 120 days up to
  the table's newest row. Window = the last 8 weeks (daily / weekly) or 6 months (monthly), up to the expected
  latest, never before the table's first row.
- **Field fill**: for the key fields, the % of rows in the window where they're entered (e.g. Meta posts tagged
  with a bag, DM leads with the bag asked about, comments with a sentiment).
- **Required field:** where the dashboard use depends on one field (Meta posts → tagged with a bag; comments →
  sentiment), the source can't be Ready until ≥ 90% of rows have it.
- **Status:** ✅ **Ready** (up to date, ≥ 90% filled, required field ≥ 90%) · 🟡 **Partial** (≤ 1 period behind or 50–90% filled) ·
  ❌ **Stale** (further behind or < 50% filled) · ⛔ **Empty** (no rows).
- **Dashboard use:** what the data could feed, and whether the dashboard already uses that source.

The source list lives at the top of the script; add a row to audit a new table.
