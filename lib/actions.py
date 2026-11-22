"""lib/actions.py — what people DO on the dashboard, kept in Supabase.

The dashboard pages are read-only reports; this is the write side: tasks made from a
card's "Do next" line, settings typed on a page (the weekly minimum), and follow-ups on
open corporate quotes. Spec: docs/current-performance.md › Acting on the page.

Everything lives in our own tables in Supabase (SUPABASE_DB_URL, beside
denri_mkt_monthly). Odoo is never written to. Every change also lands in
denri_mkt_audit: who, when, what, before → after.

All functions fail soft: no URL / no driver / DB down → reads return empty and
`available()` is False, so the page still renders and the panel says why.
"""
from __future__ import annotations

import datetime
import json
import os

try:
    import psycopg2
    import psycopg2.extras
except ImportError:                                   # pragma: no cover
    psycopg2 = None

from dotenv import load_dotenv

load_dotenv()

STATUSES = ("To do", "Doing", "Done")
OUTCOMES = ("Open", "Chased", "Won", "Lost")

SCHEMA = """
CREATE TABLE IF NOT EXISTS denri_mkt_actions (
    id          BIGSERIAL PRIMARY KEY,
    page        TEXT NOT NULL,
    month_key   TEXT NOT NULL,          -- 'YYYY-MM'
    beat        TEXT NOT NULL,          -- which card: summary, weekly, projections, price, corporate
    rec         TEXT,                   -- the "Do next" text when it was last saved
    owner       TEXT,
    status      TEXT NOT NULL DEFAULT 'To do',
    note        TEXT,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by  TEXT,
    UNIQUE (page, month_key, beat)
);
CREATE TABLE IF NOT EXISTS denri_mkt_settings (
    key         TEXT PRIMARY KEY,
    value       JSONB,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by  TEXT
);
CREATE TABLE IF NOT EXISTS denri_mkt_quote_followups (
    quote_no      TEXT PRIMARY KEY,
    client        TEXT,
    bags          INTEGER,
    kes           NUMERIC,
    valid_until   TEXT,
    outcome       TEXT NOT NULL DEFAULT 'Open',
    last_chased   DATE,
    next_followup DATE,
    note          TEXT,
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by    TEXT
);
CREATE TABLE IF NOT EXISTS denri_mkt_audit (
    id      BIGSERIAL PRIMARY KEY,
    at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    who     TEXT,
    what    TEXT NOT NULL,
    before  JSONB,
    after   JSONB
);
"""

_ready = False
LAST_ERROR: str | None = None


def _url():
    return os.environ.get("SUPABASE_DB_URL")


def _connect():
    """A connection with the tables in place, or None (LAST_ERROR says why)."""
    global _ready, LAST_ERROR
    if psycopg2 is None:
        LAST_ERROR = "The Postgres driver (psycopg2) isn't installed."
        return None
    if not _url():
        LAST_ERROR = "SUPABASE_DB_URL isn't set, so actions can't be saved."
        return None
    try:
        conn = psycopg2.connect(_url(), connect_timeout=10)
        if not _ready:
            with conn, conn.cursor() as cur:
                cur.execute(SCHEMA)
            _ready = True
        LAST_ERROR = None
        return conn
    except Exception as e:                            # noqa: BLE001
        LAST_ERROR = f"Supabase can't be reached: {e.__class__.__name__}"
        return None


def available() -> bool:
    conn = _connect()
    if conn is None:
        return False
    conn.close()
    return True


def _jsonable(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    try:
        import decimal
        if isinstance(v, decimal.Decimal):
            return float(v)
    except ImportError:
        pass
    return v


def _row(d):
    return {k: _jsonable(v) for k, v in d.items()} if d else None


def _audit(cur, who, what, before, after):
    cur.execute("INSERT INTO denri_mkt_audit (who, what, before, after) VALUES (%s, %s, %s, %s)",
                (who, what, json.dumps(_row(before)), json.dumps(_row(after))))


def _rows(sql, params=()):
    conn = _connect()
    if conn is None:
        return []
    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]
    except Exception as e:                            # noqa: BLE001
        global LAST_ERROR
        LAST_ERROR = f"Reading failed: {e}"
        return []
    finally:
        conn.close()


# ── 1. Do-next tasks ─────────────────────────────────────────────────────────

def tasks(page: str, month_key: str) -> dict:
    """{beat: row} for this page and month."""
    return {r["beat"]: r for r in _rows(
        "SELECT * FROM denri_mkt_actions WHERE page = %s AND month_key = %s", (page, month_key))}


def carried_over(page: str, month_key: str) -> list:
    """Tasks from earlier months that aren't Done yet."""
    return _rows("SELECT * FROM denri_mkt_actions WHERE page = %s AND month_key < %s AND status <> 'Done' "
                 "ORDER BY month_key DESC, beat", (page, month_key))


def save_task(page, month_key, beat, rec, owner, status, note, who) -> bool:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}")
    conn = _connect()
    if conn is None:
        return False
    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM denri_mkt_actions WHERE page=%s AND month_key=%s AND beat=%s",
                        (page, month_key, beat))
            before = cur.fetchone()
            cur.execute("""
                INSERT INTO denri_mkt_actions (page, month_key, beat, rec, owner, status, note, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, now(), %s)
                ON CONFLICT (page, month_key, beat) DO UPDATE SET
                    rec = EXCLUDED.rec, owner = EXCLUDED.owner, status = EXCLUDED.status, note = EXCLUDED.note,
                    updated_at = now(), updated_by = EXCLUDED.updated_by
                RETURNING *""", (page, month_key, beat, rec, owner or None, status, note or None, who))
            after = cur.fetchone()
            _audit(cur, who, f"task {page}/{month_key}/{beat}", before, after)
        return True
    finally:
        conn.close()


def set_task_status(task_id: int, status: str, who: str) -> bool:
    """For carried-over rows: change only the status."""
    conn = _connect()
    if conn is None:
        return False
    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM denri_mkt_actions WHERE id=%s", (task_id,))
            before = cur.fetchone()
            cur.execute("UPDATE denri_mkt_actions SET status=%s, updated_at=now(), updated_by=%s WHERE id=%s RETURNING *",
                        (status, who, task_id))
            _audit(cur, who, f"task #{task_id} status", before, cur.fetchone())
        return True
    finally:
        conn.close()


# ── 2. Settings: the weekly minimum ──────────────────────────────────────────

WEEKLY_MINIMUM = "cp.weekly_minimum"


def week_start(day: datetime.date | None = None) -> datetime.date:
    """The Sunday that starts `day`'s Sun–Sat week (the dashboard's weeks)."""
    day = day or datetime.date.today()
    return day - datetime.timedelta(days=(day.weekday() + 1) % 7)


def get_setting(key: str):
    rows = _rows("SELECT value FROM denri_mkt_settings WHERE key = %s", (key,))
    return rows[0]["value"] if rows else None


def set_setting(key: str, value, who: str) -> bool:
    conn = _connect()
    if conn is None:
        return False
    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM denri_mkt_settings WHERE key=%s", (key,))
            before = cur.fetchone()
            if value is None:
                cur.execute("DELETE FROM denri_mkt_settings WHERE key=%s", (key,))
                after = None
            else:
                cur.execute("""
                    INSERT INTO denri_mkt_settings (key, value, updated_at, updated_by) VALUES (%s, %s, now(), %s)
                    ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now(), updated_by = EXCLUDED.updated_by
                    RETURNING *""", (key, json.dumps(value), who))
                after = cur.fetchone()
            _audit(cur, who, f"setting {key}", before, after)
        return True
    finally:
        conn.close()


def weekly_minimum_override(day: datetime.date | None = None) -> int | None:
    """The weekly minimum someone set for `day`'s week, or None (use the worked-out one)."""
    v = get_setting(WEEKLY_MINIMUM)
    if not isinstance(v, dict):
        return None
    if v.get("week_start") != week_start(day).isoformat():
        return None                                    # set for another week: doesn't apply
    try:
        bags = int(v.get("bags"))
        return bags if bags > 0 else None
    except (TypeError, ValueError):
        return None


# ── 4. Corporate quote follow-ups ────────────────────────────────────────────

def followups() -> dict:
    """{quote_no: row}."""
    return {r["quote_no"]: r for r in _rows("SELECT * FROM denri_mkt_quote_followups")}


def save_followup(quote_no, client, bags, kes, valid_until, outcome, last_chased, next_followup, note, who) -> bool:
    if outcome not in OUTCOMES:
        raise ValueError(f"outcome must be one of {OUTCOMES}")
    conn = _connect()
    if conn is None:
        return False
    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM denri_mkt_quote_followups WHERE quote_no=%s", (quote_no,))
            before = cur.fetchone()
            cur.execute("""
                INSERT INTO denri_mkt_quote_followups
                    (quote_no, client, bags, kes, valid_until, outcome, last_chased, next_followup, note, updated_at, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s)
                ON CONFLICT (quote_no) DO UPDATE SET
                    client = EXCLUDED.client, bags = EXCLUDED.bags, kes = EXCLUDED.kes, valid_until = EXCLUDED.valid_until,
                    outcome = EXCLUDED.outcome, last_chased = EXCLUDED.last_chased, next_followup = EXCLUDED.next_followup,
                    note = EXCLUDED.note, updated_at = now(), updated_by = EXCLUDED.updated_by
                RETURNING *""", (quote_no, client, bags, kes, valid_until, outcome, last_chased, next_followup, note or None, who))
            _audit(cur, who, f"quote {quote_no}", before, cur.fetchone())
        return True
    finally:
        conn.close()
