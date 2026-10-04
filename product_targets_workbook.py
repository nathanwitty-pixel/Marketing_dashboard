"""product_targets_workbook.py — the month's bag targets as an Excel workbook with live formulas, for reference.

    python product_targets_workbook.py            # live month
    python product_targets_workbook.py 2026-11    # a given month

Same calculation as lib/product_targets.py (spec: docs/product-targets.md): Method (steps + a worked example),
Inputs (Odoo till + Corporate targets, period, minimum days) and Bag targets (Odoo sales and stocked days in
blue; every other column a formula). Open it in Excel to recalculate.
"""
import os, sys, datetime
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter
from lib import db, report_month, product_targets as pt

MONTH = (datetime.date.fromisoformat(sys.argv[1] + "-01") if len(sys.argv) > 1
         else report_month.live_month_window()[0])
MLABEL = MONTH.strftime("%B %Y")
rows, total, start, end, months = pt.build(MONTH)
sheet_t = pt._sheet_targets()
tills = db.run_query("""SELECT COALESCE(pc."name", 'CORPORATE') AS till, t.target_scope AS scope,
    t.target_qty AS qty, t.target_amount AS amt FROM sales_pos_target t LEFT JOIN pos_config pc ON pc.id = t.config_id
    WHERE t.period = 'month' AND t.start_date = :m AND t.target_scope IN ('pos', 'corporate')
    ORDER BY (t.target_scope = 'corporate'), t.target_qty DESC""", {"m": MONTH.isoformat()})

F = "Arial"
BLUE, BLACK, GREEN = Font(name=F, color="0000FF"), Font(name=F, color="000000"), Font(name=F, color="008000")
BOLD = Font(name=F, bold=True)
HEAD = Font(name=F, bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="1F2937")
KEY = PatternFill("solid", fgColor="FFFF00")
THIN = Border(bottom=Side(style="thin", color="BFBFBF"))
NUM, PCT, KES = "#,##0;(#,##0);-", "0.00%;(0.00%);-", "#,##0;(#,##0);-"

wb = Workbook()

# ── Method ─────────────────────────────────────────────────────────────
m = wb.active; m.title = "Method"
m.column_dimensions["A"].width = 4; m.column_dimensions["B"].width = 118
lines = [
    (MLABEL + " bag targets — how each number is calculated", "title"),
    ("Source data: Odoo (sales_pos_target, POS sales, Corporate invoices, stock). Built by lib/product_targets.py; spec docs/product-targets.md.", ""),
    ("", ""),
    ("1. Total to share out", "h"),
    ("The month's Odoo targets for every shop till (all 19, incl. Dar-es-Salaam and Uganda) plus Corporate, in bags. See the Inputs sheet.", ""),
    ("2. Sales in the base period (the three complete months before the target month)", "h"),
    ("Bags sold on every till + Corporate invoices; combo contents count per bag; refunds netted; delivery, straps, customisation, samples, discounts and gift bags left out. Colours fold into the bag (all Jumbo colours = JUMBO).", ""),
    ("3. Days available — so new bags and stock-outs aren't penalised", "h"),
    ("Days the bag had stock in a shop (any colour; daily stock rebuilt from Odoo's stock moves) or sold, counted from its launch (first sale ever). Days used = at least the minimum (Inputs) and at most the days in the period.", ""),
    ("4. Full-period equivalent", "h"),
    ("Full-period equivalent = period sold ÷ days used × days in the period. A bag in stock all period keeps its actual sales.", ""),
    ("5. Share and target", "h"),
    ("Share = the bag's full-period equivalent ÷ the sum over all bags.  Raw target = share × total.", ""),
    ("Target = whole part of the raw target, plus 1 for the bags with the largest fractions until the targets add up exactly to the total (largest-remainder rounding).", ""),
    ("6. No zero targets", "h"),
    ("Bags that sold nothing in the base period have no row; bags whose target would round to 0 are dropped.", ""),
    ("", ""),
    ("Worked example — the JUMBO row of the Bag targets sheet (live formulas)", "h"),
]
r = 1
for text, kind in lines:
    c = m.cell(row=r, column=2, value=text)
    c.font = Font(name=F, bold=True, size=14) if kind == "title" else (BOLD if kind == "h" else Font(name=F))
    c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
jumbo_row = 3 + next((i for i, x in enumerate(rows) if x["bag"] == "JUMBO"), 0)   # data starts at row 3 on Bag targets
ex = [
    ("Sold Jul–Sep", f"='Bag targets'!G{jumbo_row}"),
    ("Days used", f"='Bag targets'!I{jumbo_row}"),
    ("Full-period equivalent (sold ÷ days used × days in period)", f"='Bag targets'!J{jumbo_row}"),
    ("Share of all bags", f"='Bag targets'!K{jumbo_row}"),
    ("× Total (Inputs)", "=Inputs!$C$4"),
    ("Raw target (share × total)", f"='Bag targets'!L{jumbo_row}"),
    (MONTH.strftime("%B") + " target (after rounding)", f"='Bag targets'!N{jumbo_row}"),
]
m.column_dimensions["C"].width = 16
for label, f in ex:
    m.cell(row=r, column=2, value=label).font = Font(name=F)
    c = m.cell(row=r, column=3, value=f); c.font = GREEN
    c.number_format = PCT if "Share" in label else ("#,##0.0" if "Raw" in label or "equivalent" in label else NUM)
    r += 1

# ── Inputs ─────────────────────────────────────────────────────────────
inp = wb.create_sheet("Inputs")
for col, w in zip("ABCDE", (34, 14, 14, 18, 60)):
    inp.column_dimensions[col].width = w
inp["A1"] = "Inputs — " + MLABEL; inp["A1"].font = Font(name=F, bold=True, size=14)
inp["A3"] = "Item"; inp["C3"] = "Value"; inp["E3"] = "Source / note"
for c in ("A3", "C3", "E3"):
    inp[c].font = HEAD; inp[c].fill = HFILL
inp["A4"] = "Total target (bags)"; inp["C4"] = "=SUM(C15:C40)"; inp["C4"].fill = KEY
inp["E4"] = "Sum of the till + Corporate targets below"
inp["A5"] = "Base period start"; inp["C5"] = start
inp["A6"] = "Base period end"; inp["C6"] = end
inp["A7"] = "Days in base period"; inp["C7"] = "=C6-C5+1"
inp["A8"] = "Minimum days available"; inp["C8"] = pt.MIN_DAYS; inp["C8"].fill = KEY
inp["E8"] = "Stops a bag a few days old from getting an inflated rate (lib/product_targets.MIN_DAYS)"
inp["A9"] = "Total target (KES)"; inp["C9"] = "=SUM(D15:D40)"
for c in ("C5", "C6"):
    inp[c].number_format = "dd mmm yyyy"; inp[c].font = BLUE
inp["C8"].font = BLUE
for c in ("C4", "C7", "C9"):
    inp[c].font = BLACK
inp["C4"].number_format = NUM; inp["C9"].number_format = KES; inp["C7"].number_format = "0"
for a in ("A4", "A5", "A6", "A7", "A8", "A9"):
    inp[a].font = Font(name=F)
inp["E5"] = "The three complete months before " + MONTH.strftime("%B")
for c in ("E4", "E5", "E8"):
    inp[c].font = Font(name=F, italic=True, color="595959")
inp["A13"] = "Odoo monthly targets — " + MLABEL + " (sales_pos_target)"; inp["A13"].font = BOLD
for col, h in zip("ABCD", ("Till", "Scope", "Target (bags)", "Target (KES)")):
    inp[f"{col}14"] = h; inp[f"{col}14"].font = HEAD; inp[f"{col}14"].fill = HFILL
rr = 15
for t in tills.itertuples():
    inp.cell(row=rr, column=1, value=str(t.till)).font = Font(name=F)
    inp.cell(row=rr, column=2, value=str(t.scope)).font = Font(name=F)
    c = inp.cell(row=rr, column=3, value=int(round(float(t.qty)))); c.font = BLUE; c.number_format = NUM
    c = inp.cell(row=rr, column=4, value=int(round(float(t.amt)))); c.font = BLUE; c.number_format = KES
    rr += 1
assert rr <= 41, "more tills than the C15:C40 total range"
inp.cell(row=rr + 1, column=1, value="Source: Odoo sales_pos_target, period = month, start " + MONTH.isoformat() + ", scopes pos + corporate (pulled "
         + datetime.date.today().isoformat() + ").").font = Font(name=F, italic=True, color="595959")

# ── Bag targets ────────────────────────────────────────────────────────
bt = wb.create_sheet("Bag targets")
heads = ["Bag", "Launch (first sale)", "Days with stock or sales", "Jul sold", "Aug sold", "Sep sold",
         "Period sold", "Days in shops (from launch)", "Days used", "Full-period equivalent", "Share",
         "Raw target", "Rounding +1", MONTH.strftime("%B") + " target (bags)", "Sheet target (col C)", "Target − sheet"]
widths = [22, 14, 12, 10, 10, 10, 11, 13, 10, 13, 10, 11, 10, 13, 12, 12]
bt["A1"] = MLABEL + " — bag targets (blue = Odoo inputs, black = formulas; see Method)"; bt["A1"].font = Font(name=F, bold=True, size=12)
for i, (h, w) in enumerate(zip(heads, widths), 1):
    c = bt.cell(row=2, column=i, value=h); c.font = HEAD; c.fill = HFILL
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    bt.column_dimensions[get_column_letter(i)].width = w
bt.row_dimensions[2].height = 44
first, last = 3, 2 + len(rows)
R = f"${first}:$"  # helper
for i, x in enumerate(rows):
    n = first + i
    bt.cell(row=n, column=1, value=x["bag"]).font = Font(name=F)
    c = bt.cell(row=n, column=2, value=x["launch"]); c.font = BLUE; c.number_format = "dd mmm yyyy"
    c = bt.cell(row=n, column=3, value=x["rawDays"]); c.font = BLUE
    for j, mo in enumerate(months):
        c = bt.cell(row=n, column=4 + j, value=x["months"][mo]); c.font = BLUE; c.number_format = NUM
    f = {
        7: f"=SUM(D{n}:F{n})",
        8: f"=C{n}",
        9: f"=MIN(MAX(H{n},Inputs!$C$8),Inputs!$C$7)",
        10: f"=IF(I{n}>0,G{n}/I{n}*Inputs!$C$7,0)",
        11: f"=J{n}/SUM($J${first}:$J${last})",
        12: f"=K{n}*Inputs!$C$4",
        13: (f"=IF(RANK(L{n}-INT(L{n}),$X${first}:$X${last})+COUNTIF($X${first}:X{n},L{n}-INT(L{n}))-1"
             f"<=Inputs!$C$4-SUMPRODUCT(INT($L${first}:$L${last})),1,0)"),
        14: f"=INT(L{n})+M{n}",
        16: f'=IF(O{n}="","",N{n}-O{n})',
    }
    for col, formula in f.items():
        c = bt.cell(row=n, column=col, value=formula); c.font = BLACK
        c.number_format = {11: PCT, 12: "#,##0.0", 10: "#,##0"}.get(col, NUM)
    # helper: fractional part (column X), used by the rounding rank
    bt.cell(row=n, column=24, value=f"=L{n}-INT(L{n})").font = Font(name=F, color="808080")
    sv = sheet_t.get(x["bag"], "")
    try:
        sv = int(float(str(sv).replace(",", ""))) if str(sv).strip() else ""
    except ValueError:
        sv = ""
    c = bt.cell(row=n, column=15, value=sv); c.font = BLUE; c.number_format = NUM
    for col in range(1, 17):
        bt.cell(row=n, column=col).border = THIN
        if bt.cell(row=n, column=col).font.name != F:
            bt.cell(row=n, column=col).font = Font(name=F)
tot = last + 1
bt.cell(row=tot, column=1, value="TOTAL").font = BOLD
for col in (7, 10, 11, 12, 13, 14, 15):
    L = get_column_letter(col)
    c = bt.cell(row=tot, column=col, value=f"=SUM({L}{first}:{L}{last})"); c.font = BOLD
    c.number_format = {11: PCT, 12: "#,##0.0", 10: "#,##0"}.get(col, NUM)
bt.cell(row=tot + 1, column=1, value="Check: target total = Inputs total").font = Font(name=F, italic=True)
c = bt.cell(row=tot + 1, column=14, value=f'=IF(N{tot}=Inputs!$C$4,"OK","MISMATCH")'); c.font = BOLD
bt.cell(row=2, column=24, value="Fraction (helper)").font = Font(name=F, color="808080")
bt.column_dimensions["X"].hidden = True
bt.freeze_panes = "B3"
bt.cell(row=2, column=3).comment = Comment("Days in the base period the bag (any colour) had stock in a shop or sold, "
                                           "counted from its launch. Rebuilt from Odoo stock moves (lib/product_targets).", "Claude")
bt.cell(row=2, column=15).comment = Comment("MONTHLY_TARGET column C on the Google Sheet — for comparison only; "
                                            "no longer the target.", "Claude")

out = "Bag targets %s.xlsx" % MLABEL
wb.save(out)
print(out, len(rows), "bags")
