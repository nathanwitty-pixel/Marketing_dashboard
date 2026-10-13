# Ralph task — "Out of stock — call back" demand per shop

Repo: `c:\Users\jonat\Desktop\Marketing_dashboard` (Denri Marketing dashboard; `streamlit_app.py`
embeds the generated HTML pages). Add the **"Out of stock — call back"** demand from the Odoo
**WhatsApp Monitoring** module, **per shop**, to three menus:

| Menu | Generator | HTML | Data const | Spec |
|---|---|---|---|---|
| New Products | `new_products.py` | `new_products.html` | `NP` | `docs/new-products.md` |
| Self-made vs Running Combos | `self_made_combos.py` | `self_made_combos.html` | `SMC` | `docs/self-made-combos.md` |
| Bags On vs Off Offer | `bags_on_offer.py` | `bags_on_offer.html` | `BOO` | `docs/bags-on-offer.md` |

## Every iteration

1. Read `OOS_PROGRESS.md` and work on the **first unfinished sub-goal**.
2. Orient with `graphify query "<question>"` before reading code (the project hooks require it once per session).
3. Run that sub-goal's VERIFY. If it fails, fix it in the same iteration and don't move on.
4. Update `OOS_PROGRESS.md` (sub-goal status, what you verified, any blocker plus a repeat counter) before you finish.
5. Never `git commit`, never run `publish.bat`, never change existing numbers or logic on these pages beyond adding the call-back data. Match the surrounding code style and comment density.

## Established facts (do not re-investigate)

- **DB:** `lib.db.run_query(sql, params)` → DataFrame, or `None` if unreachable (prints the error, never raises).
  `lib.db.run_query_cached(sql, params, ttl_min)` adds a disk cache and falls back to a **stale** cached copy when offline.
- **Tables:**
  - `denri_monitor_interaction`: id, date, shop_id, phone_key, wa_username_key, reason_id, is_purchased, oos_product_id.
  - `denri_monitor_interaction_oos_product_rel`: interaction_id, product_id. product_id is a `product_product.id`;
    the name comes from `product_template.name` via `product_tmpl_id`, and it's a plain varchar (not jsonb).
  - `denri_monitor_reason`: `is_out_of_stock = true` marks "Out Of Stock" (id 4).
  - `denri_monitor_shop`: id, name, code, kind ('shop' / 'region' = Uganda / 'online' = Website). Junk rows with NULL code are ignored.
- **The query is already written:** `sql/oos_callbacks.sql` returns one row per OOS request × product:
  interaction_id, req_date, shop, shop_kind, person, is_purchased, product. Reuse it and only change it if a check proves it wrong.
- **One person** = phone_key, else wa_username_key, else `'i' || interaction id`. Count **distinct** persons.
  Never add up counts that could include the same person twice. When re-keying (several Odoo names → one page bag), union the person sets.
- Bags have only been recorded since **June 2026**, so Lifetime effectively starts then. The UI note says "Bag recorded from June 2026".
- Non-bag products (DRAWER REPAIR, flour, China Material…) appear. They drop out because each page only shows its own bags.
- Current volumes, for sanity: `sql/oos_callbacks.sql` returns ~486 request×product rows, ~453 distinct people, 213 products (shop_kind: shop 401, online 71, region 14). The top bag is
  **Mini Maya Wooven Black** with ~63 people. The current New Products (LOOP BP, ZULA, LAMORA, TAJI, IMANI, NALA, AMORA,
  VOYAGE, LAFEMME) have **0** OOS requests right now, so their chips are hidden. That's correct, not a bug.
- Colour rule: New Products keeps colour shades separate (its own `_key` / `match_odoo_bags` prefix match).
  The other two pages fold shades into `bag_names.csv` families, exactly as they already do (`lib/colours.family`, `lib/odoo_tabs.base_name`).
- Repo rule: `docs/` is the per-menu spec. Update the doc first, then the code.

## Periods (dates in Africa/Nairobi)

| Key | Meaning |
|---|---|
| `lifetime` | all OOS requests |
| `monthly` | the live report month — `lib.report_month.live_month_window()` |
| `weekly` | current Sun–Sat week to date |
| `lastweek` | previous complete Sun–Sat week |
| `current` | **still waiting** = all-dates OOS requests where is_purchased is not true |

## Sub-goals (in order)

1. **DOCS.** Add a section headed `## Out of stock — call back` to each of the three spec docs. Cover the source tables,
   the person definition, the periods, the June 2026 caveat, the per-shop hover, the matching rule for that page, and offline behaviour.
   VERIFY: `grep -l "Out of stock — call back" docs/*.md` lists all three.

2. **MODULE.** Create `lib/oos_callbacks.py`:
   - `load_rows()` reads `sql/oos_callbacks.sql` via `run_query_cached` (short TTL) and returns the rows, or `[]` on any failure (log it, never raise).
   - `aggregate(rows, key_fn=None, shop_filter=None)` returns `{period: {key: {shop: people}}}` for the 5 periods.
     key_fn maps a product name to the page's bag key, or None to drop it. People are distinct persons per (key, shop).
   - `totals(agg)` returns `{period: {key: people}}`, with distinct persons across shops (keep the person sets to compute this — not a sum).
   - `oos_by_bag_shop()` = `aggregate(load_rows())` keyed by the raw product name.
   VERIFY: create `tests/test_oos_callbacks.py` and run `python -m pytest tests/test_oos_callbacks.py -q` (it must pass). It asserts:
   (a) the lifetime sum over all products/shops equals a raw SQL `COUNT(*)` of `DISTINCT (person, product, shop)` from the same base query;
   (b) the per-shop lifetime counts for "Mini Maya Wooven Black" equal a raw per-shop SQL count;
   (c) `current <= lifetime` for every product/shop;
   (d) with `run_query` / `run_query_cached` monkeypatched to raise or return None, `oos_by_bag_shop()` returns `{}` without raising;
   (e) the totals for a key never exceed the sum of its shops.

3. **NEW PRODUCTS.** `new_products.py` puts an `oos` block in `NP`: per product card (`productTargets[].name`), matched with
   the page's own prefix rule (`match_odoo_bags` semantics, shades kept). Shape: `{period: {name: {"total": n, "shops": [[shop, n], ...]}}}`,
   with shops sorted high → low. `new_products.html` shows the chip on each product card. The chip follows the page's existing
   Period dropdown (Weekly → weekly, Last week → lastweek, Monthly → monthly, Lifetime → lifetime), plus a small "Waiting now" toggle that shows `current`.
   VERIFY: `python new_products.py` exits 0, and the NP data block in new_products.html contains `oos:` with all 5 period keys.

4. **COMBOS.** `self_made_combos.py` adds `oos` to `SMC`, keyed by the page's existing bag matching (family-folded). The chip goes on
   every component bag in the running-combo cards, every row in the region guidance bag lists, and every "Bags not on offer" row.
   The page has no period dropdown, so add a compact toggle: Lifetime / Monthly / Last week / Waiting now.
   Remember the choice in localStorage, wrapped in try/catch.
   VERIFY: `python self_made_combos.py` exits 0 and the SMC block contains `oos`.

5. **BAGS ON OFFER.** `bags_on_offer.py` adds `oos` into `BOO`, keyed the way `onBags` / `offBags` rows are, for **Kenya shops only**
   (shop_kind = 'shop', excluding Sinza and the junk rows, matching the page scope). Add a sortable **Call-backs** column (the chip)
   to both bag tables. It follows the existing Period dropdown (monthly / weekly / lastweek), plus a "Waiting now" toggle.
   VERIFY: `python bags_on_offer.py` exits 0 and the BOO block contains `oos`.

6. **CHIP UX (all 3 pages).** The chip reads "📞 N asked" ("📞 N waiting" for Waiting now), where N is the distinct people across shops.
   **Hover and tap/click** both open a small popover listing shops high → low (`Hilton 4 · Thika 2 · …`) with the footnote
   "Bag recorded from June 2026". Hide the chip when N = 0. Use each page's existing CSS variables so light and dark both work.
   No horizontal scroll at 375 px; on touch, the popover closes on outside tap.
   VERIFY: grep each HTML for the chip class and the popover handler. Then write a scratch script in the session scratchpad that runs
   `AppTest.from_file("streamlit_app.py", default_timeout=180).run()` and asserts there are no exceptions; it must pass.

7. **OFFLINE.** Run all three generators with the DB unreachable: point `lib.db` at a bad host via env vars or a monkeypatch in a
   scratch script, and set `DENRI_FORCE_FRESH=1` plus an empty cache dir so no stale copy is used. All must exit 0 with an empty `oos` (chips hidden).
   Restore everything afterwards.
   VERIFY: record the three exit codes in `OOS_PROGRESS.md`.

8. **FINISH.** Run `graphify update .`. Re-run, in one go, all three generators (normally, DB online), the pytest file, and the AppTest check;
   all must pass. Write the final summary in `OOS_PROGRESS.md`: files changed, the top 5 most-requested bags (lifetime) with their
   top shops, and the requested bag names that did not match any bag on each page.

## Stopping

- **Done:** only when sub-goals 1–8 have all passed their VERIFY in this iteration, output exactly `<promise>OOS_CALLBACKS_DONE</promise>`.
  Never output it otherwise.
- **Stuck:** if the same blocker survives 3 consecutive iterations (see the counter in `OOS_PROGRESS.md`), write `STUCK: <problem>`
  at the top of `OOS_PROGRESS.md`, then **delete `.claude/ralph-loop.local.md`**. That ends the loop. Then explain the blocker to the user.
