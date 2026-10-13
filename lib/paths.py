"""
lib/paths.py — where every kind of file lives. Use these instead of building paths from __file__.

    ROOT/
      generators/   the page builders (dashboard_pages.json "scripts" names live here)
      html/         the built pages (dashboard_pages.json "html" names live here)
      assets/       shared .js / .css loaded by the pages
      data/         inputs, configs, snapshots and history files (.json / .csv / .txt / .xlsx)
      sql/  docs/   queries and specs

    from lib import paths
    paths.data("weekly_sales_db.json")      # → ROOT/data/weekly_sales_db.json
    paths.html("current_performance.html")  # → ROOT/html/current_performance.html
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATORS = os.path.join(ROOT, "generators")
HTML = os.path.join(ROOT, "html")
ASSETS = os.path.join(ROOT, "assets")
DATA = os.path.join(ROOT, "data")
SQL = os.path.join(ROOT, "sql")
DOCS = os.path.join(ROOT, "docs")
SCRIPTS = os.path.join(ROOT, "scripts")


def root(*parts):
    return os.path.join(ROOT, *parts)


def generator(*parts):
    return os.path.join(GENERATORS, *parts)


def html(*parts):
    return os.path.join(HTML, *parts)


def asset(*parts):
    return os.path.join(ASSETS, *parts)


def data(*parts):
    return os.path.join(DATA, *parts)


def sql(*parts):
    return os.path.join(SQL, *parts)


def doc(*parts):
    return os.path.join(DOCS, *parts)


def script(*parts):
    return os.path.join(SCRIPTS, *parts)
