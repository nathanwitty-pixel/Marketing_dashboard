"""lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB till snapshot).

One pull from the replica — the last WINDOW_DAYS of pos_order and their lines (through POS_LINES, so
refunded combos are already fixed) plus the small lookup tables — written as versioned Parquet under
.snapshots/<stamp>/ with .snapshots/current.json pointing at the live set (swapped with os.replace, so a
reader never sees half a snapshot). query() runs a page's own Postgres SQL in an in-memory DuckDB over
those files and returns None whenever it can't answer faithfully, so the caller falls back to Postgres.
"""

import datetime as _dt
import json
import os
import re
import shutil
import time

import pandas as pd

from lib import paths

DIR = paths.root(".snapshots")
CURRENT = os.path.join(DIR, "current.json")
LOCK = os.path.join(DIR, "refresh.lock")
WINDOW_DAYS = 150
MAX_AGE_MIN = 30          # older → refresh before use
FORCE_MAX_AGE_MIN = 5     # a manual Refresh (DENRI_FORCE_FRESH=1) wants it newer than this
KEEP = 3

# table → Postgres SQL that fills it (:start = first day held). Numbers cast to float8 so Parquet gets
# plain doubles (psycopg2 hands back Decimal objects otherwise).
_PULL = {
    "pos_order": """
        SELECT p.id, p."name", p.date_order, p.state, p.session_id, p.partner_id, p.amount_total::float8 AS amount_total
        FROM pos_order p WHERE p.date_order >= CAST(:start AS date)""",
    "pos_order_line": """
        SELECT pl.id, pl.order_id, pl.product_id, pl.qty::float8 AS qty, pl.price_unit::float8 AS price_unit,
               pl.price_subtotal::float8 AS price_subtotal, pl.price_subtotal_incl::float8 AS price_subtotal_incl,
               pl.discount::float8 AS discount, pl.full_product_name::text AS full_product_name,
               pl.is_combo_line, pl.is_program_reward, pl.combo_product_attribute_values::text AS combo_product_attribute_values,
               pl.refunded_orderline_id, pl.sub_product_line, pl.parent_id
        FROM pos_order p JOIN POS_LINES(p) pl ON pl.order_id = p.id
        WHERE p.date_order >= CAST(:start AS date)""",
    "pos_session": "SELECT id, config_id FROM pos_session",
    "pos_config": 'SELECT id, "name" FROM pos_config',
    "product_product": "SELECT id, product_tmpl_id FROM product_product",
    "product_template": 'SELECT id, "name"::text AS "name", categ_id, list_price::float8 AS list_price, active FROM product_template',
    "product_category": 'SELECT id, "name"::text AS "name" FROM product_category',
}
TABLES = tuple(_PULL)
_FROM = re.compile(r"\b(?:FROM|JOIN)\s+(?:LATERAL\s+)?([A-Za-z_][\w]*)", re.I)
_POS_LINES = re.compile(r"\bPOS_LINES\(\s*\w+\s*\)")
_PARAM = re.compile(r"(?<![:\w]):([A-Za-z_]\w*)")
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _meta():
    try:
        with open(CURRENT, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _age_min(meta):
    return (time.time() - meta.get("refreshed_ts", 0)) / 60


def refresh():
    """Pull a new snapshot and point current.json at it. Returns the new meta, or None (old one kept)."""
    import duckdb
    from lib import db
    os.makedirs(DIR, exist_ok=True)
    try:                                                     # one refresher at a time across generators
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        if time.time() - os.path.getmtime(LOCK) < 600:
            return None                                      # someone else is refreshing — use what's there
        os.remove(LOCK)
        return refresh()
    try:
        t0 = time.time()
        start = (_dt.date.today() - _dt.timedelta(days=WINDOW_DAYS)).isoformat()
        stamp = _dt.datetime.now().strftime("%Y%m%dT%H%M%S")
        out = os.path.join(DIR, stamp)
        os.makedirs(out, exist_ok=True)
        rows = {}
        con = duckdb.connect()
        for t, sql in _PULL.items():
            df = db.run_query(sql, {"start": start})
            if df is None:
                raise RuntimeError(f"{t}: Odoo unreachable")
            con.register("df", df)
            con.execute(f"COPY (SELECT * FROM df) TO '{_p(os.path.join(out, t + '.parquet'))}' (FORMAT parquet)")
            con.unregister("df")
            rows[t] = len(df)
        con.close()
        meta = {"dir": stamp, "start": start, "refreshed_ts": time.time(),
                "refreshed_at": _dt.datetime.now().strftime("%d %b %Y %H:%M"), "rows": rows,
                "seconds": round(time.time() - t0, 1)}
        tmp = CURRENT + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=1)
        os.replace(tmp, CURRENT)
        print(f"  Till snapshot    : refreshed in {meta['seconds']}s "
              f"({rows['pos_order_line']:,} lines since {start})")
        _cleanup(stamp)
        return meta
    except Exception as e:                                   # noqa: BLE001 — keep the old snapshot
        print(f"  Till snapshot    : refresh failed ({e}) — kept the previous one")
        return None
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass


def _cleanup(keep_stamp):
    dirs = sorted(d for d in os.listdir(DIR) if os.path.isdir(os.path.join(DIR, d)))
    for d in dirs[:-KEEP]:
        if d != keep_stamp:
            shutil.rmtree(os.path.join(DIR, d), ignore_errors=True)   # a locked file is retried next run


def _p(path):
    return path.replace("\\", "/").replace("'", "''")


def fresh_meta():
    """The snapshot to read, refreshing it first when it's too old; None if there's none usable."""
    meta = _meta()
    limit = FORCE_MAX_AGE_MIN if os.getenv("DENRI_FORCE_FRESH") == "1" else MAX_AGE_MIN
    if meta is None or _age_min(meta) > limit:
        meta = refresh() or meta
    if meta is None or _age_min(meta) > MAX_AGE_MIN * 4:     # refresh failed and the old one is too stale
        return None
    return meta


def query(sql: str, params: dict | None = None):
    """The SQL's result from the snapshot as a DataFrame, or None when the snapshot can't answer it
    (stale / missing, dates before its window, or a table it doesn't hold) — the caller then goes live."""
    params = dict(params or {})
    names = {m.group(1).lower() for m in _FROM.finditer(sql)} - {"pos_lines"}
    if not names or not names <= set(TABLES):
        return None
    meta = fresh_meta()
    if meta is None:
        return None
    first = _dt.date.fromisoformat(meta["start"]) + _dt.timedelta(days=1)   # a day's margin for UTC dates
    for v in params.values():
        d = v if isinstance(v, _dt.date) else (_dt.date.fromisoformat(v) if isinstance(v, str) and _ISO.match(v) else None)
        if d is not None and d < first:
            return None
    sql = _POS_LINES.sub("pos_order_line", sql)
    used = set()

    def _sub(m):
        if m.group(1) in params:
            used.add(m.group(1))
            return "$" + m.group(1)
        return m.group(0)
    sql = _PARAM.sub(_sub, sql)
    try:
        import duckdb
        with duckdb.connect() as con:
            for t in TABLES:
                con.execute(f"CREATE VIEW {t} AS SELECT * FROM read_parquet('{_p(os.path.join(DIR, meta['dir'], t + '.parquet'))}')")
            res = con.execute(sql, {k: params[k] for k in used})
            types = [str(d[1]) for d in res.description]
            df = res.df()
        # DuckDB hands DATE back as datetime64; Postgres gives datetime.date, which pages str() into keys.
        for col, t in zip(df.columns, types):
            if t == "DATE":
                df[col] = pd.to_datetime(df[col]).dt.date
        return df
    except Exception as e:                                   # noqa: BLE001 — anything odd → live query
        print(f"  Till snapshot    : query not answerable here ({str(e).splitlines()[0][:120]}) — live instead")
        return None
