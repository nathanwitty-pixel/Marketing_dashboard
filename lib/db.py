"""lib/db.py — Postgres access for the marketing dashboard.

Deliberately the SAME surface as the Streamlit app's lib.db so the existing
queries and report code port straight in when we migrate the rest of the
dashboard: run_query(sql, params) -> DataFrame, plus check_connection().

Connection comes from the environment (a .env in this folder is loaded):
    DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
  — or the individual pieces —
    PGHOST=... PGPORT=5432 PGDATABASE=... PGUSER=... PGPASSWORD=...

Named params use :name placeholders, e.g.
    run_query("SELECT ... WHERE d BETWEEN :start_date AND :end_date",
              {"start_date": s, "end_date": e})
"""
from __future__ import annotations

import os
from functools import lru_cache

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine

load_dotenv()


def _env(*names: str, default: str | None = None) -> str | None:
    for n in names:
        v = os.getenv(n)
        if v:
            return v
    return default


def _url():
    """Build a SQLAlchemy URL from the environment, or None if unset.
    Accepts DATABASE_URL, or the individual PG*/DB_* pieces (DB_* matches the
    Streamlit app's .env). URL.create handles any special chars in the password."""
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        if dsn.startswith("postgres://"):
            dsn = "postgresql+psycopg2://" + dsn[len("postgres://"):]
        elif dsn.startswith("postgresql://") and "+psycopg2" not in dsn:
            dsn = "postgresql+psycopg2://" + dsn[len("postgresql://"):]
        return dsn
    host = _env("PGHOST", "DB_HOST")
    if not host:
        return None
    return URL.create(
        "postgresql+psycopg2",
        username=_env("PGUSER", "DB_USER", default=""),
        password=_env("PGPASSWORD", "DB_PASSWORD", default=""),
        host=host,
        port=int(_env("PGPORT", "DB_PORT", default="5432")),
        database=_env("PGDATABASE", "DB_NAME", default=""),
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine | None:
    url = _url()
    if url is None:
        return None
    # pool_pre_ping avoids stale-connection errors on a long-lived generator run
    return create_engine(url, pool_pre_ping=True, future=True)


def check_connection() -> tuple[bool, str]:
    """(ok, detail). Never raises — the callers show `detail` in the UI."""
    eng = get_engine()
    if eng is None:
        return False, ("No database configured. Set DATABASE_URL (or PGHOST/…) "
                       "in a .env file — see .env.example.")
    try:
        with eng.connect() as c:
            c.execute(text("SELECT 1"))
        return True, "connected"
    except Exception as e:                                   # noqa: BLE001
        return False, str(e)


def run_query(sql: str, params: dict | None = None) -> pd.DataFrame | None:
    """Run a read query and return a DataFrame, or None if the DB is unreachable.

    Matches lib.db.run_query from the Streamlit app so report code is portable.
    """
    eng = get_engine()
    if eng is None:
        return None
    try:
        with eng.connect() as c:
            return pd.read_sql(text(sql), c, params=params or {})
    except Exception as e:                                   # noqa: BLE001
        print(f"  DB query failed: {e}")
        return None
