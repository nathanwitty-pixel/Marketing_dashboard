"""Run the sticky-controls checks on every wired page and print the markdown results table.
    python notes/sticky_test/run_all.py
Also node --check every <script> block of each page. Exit 1 if any row fails."""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGES = [  # page, bar selector (what the checks measure), extra args (scroll target / redraw action)
    ("product_performance.html", ".controls", ["--set", "#pp-period=lastmonth", "--click", "#pp-mkt button[data-v=KE]", "--read", ".sh-head span:last-child"]),
    ("bags_on_offer.html", "#boo-ctl", ["--set", "#boo-period=weekly", "--read", "#boo-trend-title"]),
    ("self_made_combos.html", "#smc-oos-bar", ["--click", "#smc-view-seg button[data-view=deals]", "--read", "#smc-view-seg .is-active"]),
    ("new_products.html", "div:has(> #pt-title)", ["--at", "#pt-title", "--set", "#pt-period=weekly", "--read", "#pt-title"]),
    ("posting_yields.html", "[data-sticky-controls]:has(#py-k-period)", ["--at", "[data-sticky-controls]:has(#py-k-period)", "--set", "#py-k-period=lastweek", "--read", "#py-k-period"]),
    ("shops_efficiency.html", ".filter-bar", ["--at", ".filter-bar", "--click", ".filter-bar .reset", "--read", ".filter-bar select"]),
    ("timed_offers.html", ".to-ctl", ["--at", ".to-ctl", "--set", "[data-el=why-sort]=sold-asc", "--read", "[data-el=why-sort]"]),
    ("offer_picking.html", ".se-ctl", ["--at", "#se-table"]),
    ("monthly_report.html", "[data-sticky-controls]:has(#np-sort)", ["--at", "[data-sticky-controls]:has(#np-sort)", "--set", "#np-sort=sold-asc", "--read", "#np-sort"]),
    ("history.html", ".sortbar", ["--at", ".sortbar", "--set", "#np-sort=sold-asc", "--read", "#np-sort"]),
]


def node_check(page):
    s = open(os.path.join(ROOT, "html", page), encoding="utf-8").read()
    bad = 0
    for i, b in enumerate(re.findall(r"<script>(.*?)</script>", s, re.S)):
        f = os.path.join(tempfile.gettempdir(), "sc_chk_%d.js" % i)
        open(f, "w", encoding="utf-8").write(b)
        if subprocess.run(["node", "--check", f], capture_output=True).returncode:
            bad += 1
    return bad


def main():
    rows, ok = [], True
    for page, sel, extra in PAGES:
        out = subprocess.run([sys.executable, os.path.join(HERE, "run.py"), page, sel] + extra, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", cwd=ROOT).stdout.strip().splitlines()
        res = {}
        for ln in out:
            try:
                r = json.loads(ln)
                res[r["mode"]] = r
            except ValueError:
                pass
        sa, em = res.get("standalone", {}), res.get("embedded", {})
        nc = node_check(page)
        redraw = "n/a (search box)" if "--set" not in extra and "--click" not in extra else (
            "ok" if sa.get("pass") and em.get("pass") and sa.get("read") else "FAIL")
        errs = len(sa.get("errors") or []) + len(em.get("errors") or [])
        good = bool(sa.get("pass") and em.get("pass") and nc == 0 and errs == 0)
        ok = ok and good
        rows.append("| %s | `%s` | %s | %s | %s | %s | %s | %s |" % (
            page, sel, sa.get("top"), em.get("top"), redraw, "ok" if nc == 0 else "%d FAIL" % nc, errs, "pass" if good else "FAIL"))
        print(rows[-1], flush=True)
    print("\n| Page | Bar selector | Standalone top (0–8) | Embedded top (56–72) | Redraw while pinned | node --check | JS errors | Result |")
    print("|---|---|---|---|---|---|---|---|")
    print("\n".join(rows))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
