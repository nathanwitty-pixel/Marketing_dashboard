# Agent skills — retail analytics

Reusable Claude skills distilled from the marketing dashboard. Each folder is a self-contained skill: a
`SKILL.md` (when to use it + the method) and `scripts/` (pure-Python code, no dependencies, with tests).
No company data, IDs or credentials — feed them your own sales / stock / receipts.

| Skill | What it does |
|---|---|
| [`bag-signals`](bag-signals/SKILL.md) | Quant signals per product — real trend vs luck, volatility, Sharpe-style reliability, beta, 14-day run-out risk, safe stock, posting beta → Restock / Post more / Clear / … |
| [`sales-share-targets`](sales-share-targets/SKILL.md) | Split a month's target across products by recent sales share, scaled to the days each product was launched and in stock; exact rounding; Excel-with-formulas pattern |
| [`receipt-combo-detection`](receipt-combo-detection/SKILL.md) | Combos from receipts where every item is its own line; running vs self-made vs an offer list; closest-name matching |
| [`stockout-demand`](stockout-demand/SKILL.md) | Distinct people asking for out-of-stock products per shop and colour, with each shop's stock |

## Use in another project

Copy the skill folder(s) into either
- `<project>/.claude/skills/` — that project only, or
- `~/.claude/skills/` (Windows: `C:\Users\<you>\.claude\skills\`) — every project,

then start a new Claude Code session. Claude picks a skill up when a request matches its description; you can
also ask for it by name ("use the bag-signals skill on our sales").

## Test a skill

```
cd agent-skills/<skill>
python -m pytest scripts -q
```

Source of truth for the dashboard's own versions: `lib/bag_quant.py`, `lib/product_targets.py`,
`lib/receipt_combos.py`, `self_made_combos.py` (name matching), `lib/oos_callbacks.py`. Regenerate the skill
scripts from them after changes (`gen_skills.py` pattern: copy the pure functions, drop the data loaders).
