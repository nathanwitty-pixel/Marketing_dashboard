"""Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET, MONTHLY_MARKETING_POST,
WEEKLY_MARKETING_POST — of the main spreadsheet (docs/README.md › Where the data comes from).
Fails if live code (not export/, tests/) reads another tab, a range of another tab, or another sheet.
    python -m pytest tests/test_sheet_reads.py -q
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_TABS = {"MONTHLY_TARGET", "MONTHLY_MARKETING_POST", "WEEKLY_MARKETING_POST"}
MAIN_SHEET = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"
SKIP = ("export", "tests", "graphify-out", ".git", "__pycache__", ".claude")


def _sources():
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for f in files:
            if f.endswith(".py"):
                p = os.path.join(root, f)
                yield os.path.relpath(p, BASE), open(p, encoding="utf-8").read()


def test_only_three_tabs_are_read():
    bad = []
    for rel, src in _sources():
        for tab in re.findall(r"""worksheet\(\s*["']([^"']+)["']""", src):
            if tab not in ALLOWED_TABS:
                bad.append(f"{rel}: worksheet('{tab}')")
        for tab in re.findall(r"""["']([A-Z_]+)!""", src):
            if tab not in ALLOWED_TABS:
                bad.append(f"{rel}: range on '{tab}'")
        if re.search(r"get_worksheet(_by_id)?\(", src):
            bad.append(f"{rel}: worksheet by index/id")
    assert not bad, "sheet reads outside the three tabs:\n" + "\n".join(bad)


def test_only_the_main_spreadsheet():
    ids = set()
    for rel, src in _sources():
        ids |= {(rel, i) for i in re.findall(r"""["'](1[A-Za-z0-9_-]{40,})["']""", src)}
    assert {i for _, i in ids} <= {MAIN_SHEET}, sorted(ids)
