"""lib/sales_date_fix.py — sales keyed in late, moved back to the day they happened (docs/shop-launch.md ›
Sales keyed in late).

The shop launch config (data/shop_launch_config.json) lists `salesDateFix` windows for its till:
{"from": "YYYY-MM-DD HH:MM", "to": "...", "asDate": "YYYY-MM-DD"} in Nairobi time. Every sale keyed in that
window counts on asDate. The Shop Launch page applies it to the exact order time; pages that only have a till's
sales per day (the "Why did we move?" waterfall) use day_for(), which moves whole days from the window's first
day up to the day before it ends (Nyeri: Sat 7 and Sun 8 Nov → Sat 7 Nov; Mon 9 Nov stays Monday).
"""
import datetime
import json

from lib import paths


def load():
    """[{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if none or unreadable."""
    try:
        with open(paths.data("shop_launch_config.json"), encoding="utf-8") as fh:
            cfg = json.load(fh)
    except (OSError, ValueError):
        return []
    out = []
    for f in cfg.get("salesDateFix") or []:
        try:
            out.append({"till": str(cfg.get("till") or "").upper(), "shop": cfg.get("shop") or cfg.get("till"),
                        "from": datetime.datetime.fromisoformat(f["from"]),
                        "to": datetime.datetime.fromisoformat(f["to"]),
                        "asDate": datetime.date.fromisoformat(f["asDate"])})
        except (KeyError, ValueError):
            continue
    return out


def day_for(till, day, fixes=None):
    """The day a till's sales of `day` count on (day granularity)."""
    t = str(till or "").upper()
    for f in (load() if fixes is None else fixes):
        if f["till"] == t and f["from"].date() <= day < f["to"].date():
            return f["asDate"]
    return day
