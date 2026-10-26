"""
negative_fixes_report.py — rank the shops on stock-record accuracy from the NEGATIVE FIX LOG
(spec: docs/shops-efficiency.md › Stock record accuracy).

    python scripts/negative_fixes_report.py                     # Last week (default)
    python scripts/negative_fixes_report.py --period thisweek   # lastweek | thisweek | thismonth | lastmonth | sincelog

Best first = fewest fixes per 1,000 bags sold, big one-offs (a single fix of 10+ units) left out.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
from lib import negative_fixes as nf

KEYS = ("lastweek", "thisweek", "thismonth", "lastmonth", "sincelog")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rank shops by negative-stock fixes per 1,000 bags sold.")
    ap.add_argument("--period", choices=KEYS, default="lastweek")
    a = ap.parse_args(argv)
    try:
        data = nf.block()
    except Exception as e:                                  # noqa: BLE001
        print(f"Could not read the NEGATIVE FIX LOG: {e}")
        return 1
    p = data["periods"][a.period]
    before = f" (compared with {p['prevStart']} to {p['prevEnd']})" if p["prevStart"] else ""
    print(f"\nStock record accuracy: {p['label']}, {p['start']} to {p['end']}{before}")
    print(f"Log runs from {data['logStart']} to {data['lastLogDate']}. Ranking = fixes per 1,000 bags sold, "
          f"big one-offs ({data['big']}+ units in one fix) left out.\n")
    head = f"{'#':>3}  {'Shop':<11}{'Fixes':>6}{'Units':>7}{'Bags sold':>11}{'Per 1,000':>11}{'Days':>6}{'Repeats':>9}  Change"
    print(head)
    print("-" * len(head))
    for i, r in enumerate(p["shops"], 1):
        rate = f"{r['rate']:.1f}" if r["rate"] is not None else "no sales"
        if r.get("prevFixes") is None:
            chg = ""
        else:
            d = r["fixesNoBig"] - r["prevFixes"]
            chg = f"{d:+d} fixes (was {r['prevFixes']})" if d else f"same ({r['prevFixes']})"
        big = f"  ⚠ +{len(r['big'])} big" if r["big"] else ""
        print(f"{i:>3}  {r['label']:<11}{r['fixes']:>6}{r['units']:>7}{r['bags']:>11,}{rate:>11}{r['days']:>6}{r['repeatItems']:>9}  {chg}{big}")
    if p["repeats"]:
        print("\nRepeat items (went negative again after an earlier fix):")
        for shop, item, n in p["repeats"][:15]:
            print(f"   {shop:<11} {item:<24} {n} {'time' if n == 1 else 'times'} again")
    if p["big"]:
        print(f"\n⚠ Big one-offs (a single fix of {data['big']}+ units, left out of the ranking):")
        for b in p["big"]:
            print(f"   {b['shop']:<11} {b['date']}  {b['item']:<24} {b['units']} units (sheet row {b['row']})")
    if not p["shops"] or not p["totalFixes"]:
        print("\nNo fixes logged in this period.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
