# Product / name matching

How a name on a **sheet** (a deal label, a new-product row, a combo pairing) is matched to
the **Odoo** product(s) it refers to. This is the single most common source of "it shows 0
but I know it sold" bugs, so it has its own reference. When a figure looks wrong, start
here.

## Why matching is hard — the Odoo naming realities

Odoo product names don't line up 1:1 with how the sheets write them:

| Reality | Example | Effect |
|---------|---------|--------|
| **Colour-only** template names | `JAMELA BLACK`, `KAI GREY` | the sheet label adds a category word the name lacks |
| **Category word in the label** | sheet "Jamela **handbag**", "Kai **backpack**" | full-label match fails; need a root fallback |
| **Spelling variant** | sheet "Briefcase" vs Odoo `BRIEF CASE …` | prefix match fails; need an alias |
| **Promo wording ≠ catalogue** | sheet "Laptop Backpack" = `CODE 3 …` | need an alias |
| **Internal-reference prefix** | `full_product_name` = `[S_0] Lamora Sky Blue` | prefix match fails; strip the `[...]` |
| **Combos carry `+` names** | `KAI GREEN + STANDARD BLACK + …` | must be excluded from single-bag sales/stock |
| **Bogus placeholder stock** | `WIP`/`WRKWH`/… ≈ 44,444 per variant | never count as sellable stock |
| **Look-alikes** | `MINI BRIEF CASE`, `KCB BRIEFCASE` vs `BRIEF CASE` | must NOT be swept in |

## Normalisation (applied before any compare)

- **Upper-case** everything (`UPPER(pt."name")` in SQL, `.upper()` in Python).
- **Collapse whitespace:** `re.sub(r"\s+", " ", s).strip()`.
- **Strip the internal-ref prefix:** `re.sub(r"^\[[^\]]*\]\s*", "", p)` — drops a leading
  `[S_0] ` / `[CODE] ` so `[S_0] Lamora Sky Blue` matches "LAMORA".
- **Net returns:** count sales with `pl.qty <> 0` (not `> 0`) so `SUM(pl.qty)` **subtracts
  returns** (return lines are negative qty, same day/state). Filtering `> 0` counts the sale
  but not its refund — e.g. a 777-unit Lola Black sale + a −776 return netted to 51, but
  showed as 826 until this was fixed. Applies to Self-Made Combos (all its SQL), New
  Products' Kenya-vs-outside split, and Current Performance already nets via `lib/queries`
  (no `qty` filter). Stock queries are unaffected (they sum on-hand `quantity`).
- **Exclude combos** from single-bag figures: `name NOT LIKE '%+%'`.
- **Exclude non-sellable stock:** only count shop stock-location codes; never
  `WIP`/`WRKWH`/`PURCH`/`PREWH`/`ASSWH`/`CORP`/`VLD`/`MRKT`/`FINWH`/`RJW`/`SHT`/`STF` etc.
  (see [README](README.md) for the sellable Kenya/Sinza/Uganda codes).

## New Products — `match_odoo_bags` (`new_products.py`)

Sums Odoo bags whose `full_product_name` **starts with** the new-product name:

```python
p = strip_ref_prefix(name.upper())          # drop "[S_0] " etc.
p == b  or  p.startswith(b + " ")  or  p.startswith(b + "-")
```

- **Prefix, not contains** — so "AMORA" catches "AMORA …" but not "**L**AMORA".
- Counts standalone `full_product_name` sales only; combo/reward/strap/gift lines are
  filtered out upstream by `_BAGS_WHERE`.
- **Gotcha fixed:** without the `[...]` strip, `[S_0] Lamora Sky Blue` was dropped
  (Lamora read 10 not 14 this month, and 38 short on lifetime).

## Deals (Power Deals / Deal of the Week) — `_match` (`self_made_combos.py`)

The richest matcher. It builds three predicates, picks **one selector**, and uses it
everywhere so the total, the weekly series and the per-shop split always agree.

**Inputs**
- `p` = the sheet label, upper-cased (e.g. `KAI BACKPACK`, `BRIEFCASE`).
- `pa` = `DEAL_ALIASES.get(p, p)` — the aliased catalogue key.
- `root` = `p` minus its trailing word **iff** that word is in `_CATEGORY_WORDS`
  (`HANDBAG, BACKPACK, TRAVEL, SLING, SLINGBAG, MESSENGER, BAG, LUNCHBAG, LUNCHSET, HB,
  BP`). So `KAI BACKPACK` → root `KAI`; `BRIEFCASE` (one word) → root `None`.

**Predicates**
- `_full(nm)` — full-label prefix match against **both** `p` and `pa` (either direction).
- `_rooted(nm)` — prefix match on the category-stripped `root`.
- `_stock_match(bt)` — bag-type/alias/first-word rule, for sheet-level stock keys.

**The selector** (`_sel`) — decided once per deal:
> `_sel = _full` if any full match exists in sales/weekly (or there's no root);
> otherwise `_sel = _rooted`.

`_sel` is then applied to: the **total** sold/revenue, the **weekly** series, and the
**per-shop** `soldByLoc`. Stock uses `_sel(nm) or _stock_match(nm)` (the per-shop stock
map holds colour-level names like `BRIEF CASE GREY`, so the colour-level selector is what
catches them).

### `DEAL_ALIASES` (label → catalogue key)

| Sheet label | Odoo key | Why |
|-------------|----------|-----|
| STANDARD TRAVEL / STANDARD | TRAVEL | promo wording |
| CAIRO BACKPACK | CAIRO BP | catalogue abbreviation |
| LAPTOP BACKPACK | CODE 3 | different catalogue name |
| NEO MAN BAG | NEO MAN | trailing word |
| BRIEFCASE | BRIEF CASE | sheet one word, Odoo two words |

> **If a deal shows 0 sold/stock but you know it sells:** the label almost certainly
> differs from the Odoo name. Confirm with a quick `LIKE '%…%'` probe, then add a
> `DEAL_ALIASES` entry (label → the Odoo prefix). One entry fixes sales, weekly **and**
> stock because they share `_sel`.

## Bag-type matching for combo components (`_match_bag`)

`_match_bag` (used by `_combo_bags` for the card's component list AND by the component
attribution below) resolves a bag name to a catalogue bag type. `BAG_ALIASES` (Standard /
Standard Travel → TRAVEL, Laptop Backpack → CODE 3, Neo Man Bag → NEO MAN, Gym Bag) is
applied to the **whole token and to its leading word(s)** — so a printed component carrying
a colour suffix (`"STANDARD TRAVEL BLACK"`) still aliases to TRAVEL. Without the
leading-word alias the print was orphaned under `STANDARD` while `_combo_bags` (aliasing the
bare `"Standard"`) showed the bag as TRAVEL, so a running card's per-bag `· N sold` chips
did **not** sum to `combos × slots` (Jumbo+Standard, Baby). Both sides now agree.

## Combo component attribution (`self_made_combos.py`)

To count how many of a bag went out **inside** combos (vs standalone), the printed
component is read from `pos_order_line.combo_product_attribute_values` — a Python-literal
string — via `ast.literal_eval`, mapped to the full product, then to a bag type with
`_match_bag`. This is what powers a running-combo card's per-bag `· N sold`. Combo lines
are the `%+%`-named products; standalone sales are separate POS lines.

## Market & shop mapping (deals)

- **Market split:** Kenya = every till except `sinza` / `dar-es-alam` / `uganda`.
- **POS till → sheet location label:** `_SHOP_TO_LOC` (e.g. `KTDA SHOP`→`KTDA`,
  `WEBSITE SALES`→`Website`, `NAIROBI TOWN`→`Starmall` via the sheet alias).
- **Stock code → sheet location label:** `_STOCK_CODE_TO_LOC` (e.g. `STAR`→`Starmall`,
  `HTN`→`Hilton`). Website has no stock code — it's judged on sales alone.

## Quick probe recipe

When unsure what Odoo calls something, run a throwaway query (scratchpad):

```sql
SELECT UPPER(pt."name"), SUM(pl.qty)
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','paid') AND pl.qty>0
  AND UPPER(pt."name") LIKE '%<TERM>%'
GROUP BY 1 ORDER BY 2 DESC;
```

Then reconcile the real name with the sheet label — add an alias (deals) or rely on the
`[...]`-strip + prefix rule (new products).
</content>
</invoke>
