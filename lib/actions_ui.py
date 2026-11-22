"""lib/actions_ui.py — the "Act on this page" panel shown above Current Performance.

Reads what the page says (its "Do next" lines, the weekly floor, the open corporate
quotes) from the built HTML, and lets people act on it: tasks, this week's minimum,
quote follow-ups. Saves go to Supabase through lib/actions.py.
Spec: docs/current-performance.md › Acting on the page.
"""
from __future__ import annotations

import datetime
import json
import re

import pandas as pd
import streamlit as st

from lib import actions

PAGE = "Current Performance"

# Which card each "Do next" line comes from, in page order.
BEATS = [
    ("summary", "Month outlook"),
    ("weekly", "Weekly performance"),
    ("projections", "Forward projections"),
    ("price", "Price per bag"),
    ("corporate", "Corporate by client"),
]


# ── what the page says ───────────────────────────────────────────────────────

def _field(html: str, name: str):
    """A one-line JSON value from the page's PERF / PROJ blocks (`  name:   <json>,`)."""
    m = re.search(r"^\s*" + re.escape(name) + r":\s*(.+?),?\s*$", html, re.M)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def _recs(html: str) -> dict:
    beats = _field(html, "beats") or {}
    out = {k: (beats.get(k) or {}).get("rec") for k in ("summary", "weekly", "projections", "price")}
    out["corporate"] = (_field(html, "corporateBeat") or {}).get("rec")
    return {k: v for k, v in out.items() if v}


def _open_quotes(html: str) -> list:
    """Quotes this month not invoiced yet (and not declined / cancelled)."""
    rows = []
    for c in _field(html, "corporateClients") or []:
        for q in c.get("quotes") or []:
            if q.get("invoice") or str(q.get("status", "")).lower() in ("cancel", "cancelled", "declined"):
                continue
            rows.append({"client": c.get("client", ""), "no": q.get("no", ""), "status": q.get("status", ""),
                         "on": q.get("on", ""), "until": q.get("until", ""),
                         "bags": int(float(q.get("bags") or 0)), "kes": int(float(q.get("kes") or 0))})
    return rows


def _month_key(html: str) -> str:
    """The month the page reports ('YYYY-MM'), from PROJ.projMonth; this month if missing."""
    name = _field(html, "projMonth")
    today = datetime.date.today()
    try:
        m = datetime.datetime.strptime(str(name), "%B").month
        year = today.year if m <= today.month else today.year - 1     # December viewed in January
        return f"{year}-{m:02d}"
    except ValueError:
        return f"{today.year}-{today.month:02d}"


# ── Supabase reads, cached briefly (the pooler is slow) ─────────────────────

@st.cache_data(ttl=30, show_spinner=False)
def _load(month_key: str):
    return {
        "ok": actions.available(),
        "error": actions.LAST_ERROR,
        "tasks": actions.tasks(PAGE, month_key),
        "carried": actions.carried_over(PAGE, month_key),
        "minimum": actions.get_setting(actions.WEEKLY_MINIMUM),
        "followups": actions.followups(),
    }


def _saved(msg: str):
    _load.clear()
    st.session_state["actions_msg"] = msg


def _plain(v):
    """An edited cell back to plain Python: NaN / NaT → None, Timestamp → date."""
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(v, pd.Timestamp):
        return v.date()
    if isinstance(v, datetime.datetime):
        return v.date()
    return v


def _when(ts) -> str:
    if not ts:
        return ""
    try:
        t = datetime.datetime.fromisoformat(str(ts)).astimezone()
        return t.strftime("%d %b %H:%M")
    except ValueError:
        return str(ts)


# ── the panel ────────────────────────────────────────────────────────────────

def render(html: str, rebuild):
    """Draw the panel. `rebuild()` rebuilds the page in the background (after a settings change)."""
    month_key = _month_key(html)
    recs = _recs(html)
    quotes = _open_quotes(html)
    data = _load(month_key)
    today = datetime.date.today()

    todo = sum(1 for k in recs if (data["tasks"].get(k) or {}).get("status", "To do") != "Done")
    due = sum(1 for q in quotes
              if (f := data["followups"].get(q["no"])) and f.get("next_followup")
              and str(f["next_followup"]) <= today.isoformat() and f.get("outcome") not in ("Won", "Lost"))
    title = f"Act on this page: {todo} to do" + (f", {due} follow-up{'s' if due != 1 else ''} due" if due else "")

    with st.expander(title, expanded=False, icon=":material/task_alt:"):
        msg = st.session_state.pop("actions_msg", None)
        if msg:
            st.success(msg)
        if not data["ok"]:
            st.warning(f"Actions can't be saved right now. {data['error'] or ''} The page below still works.")
            return

        who = st.text_input("Your name (saved with every change)", key="actions_who",
                            placeholder="e.g. Jonathan").strip()
        if not who:
            st.caption("Type your name first. Each change records who made it.")

        t_do, t_min, t_quotes = st.tabs(["Do next", "Weekly minimum", f"Corporate follow-ups ({len(quotes)})"])

        # ── 1. Do next → tasks ──
        with t_do:
            if not recs:
                st.caption("No “Do next” lines on the page right now.")
            for beat, label in BEATS:
                rec = recs.get(beat)
                if not rec:
                    continue
                row = data["tasks"].get(beat) or {}
                with st.form(f"task_{beat}", border=True):
                    st.markdown(f"**{label}**  \n{rec}")
                    if row.get("rec") and row["rec"] != rec:
                        st.caption(f"Saved against the earlier advice: “{row['rec']}”")
                    c1, c2 = st.columns([0.45, 0.55])
                    owner = c1.text_input("Owner", value=row.get("owner") or "", key=f"own_{beat}")
                    status = c2.segmented_control("Status", actions.STATUSES, key=f"st_{beat}",
                                                  default=row.get("status") or "To do") or "To do"
                    note = st.text_area("Note", value=row.get("note") or "", key=f"note_{beat}", height=68)
                    if row.get("updated_by"):
                        st.caption(f"Last saved by {row['updated_by']}, {_when(row.get('updated_at'))}")
                    if st.form_submit_button("Save", type="primary", disabled=not who):
                        if actions.save_task(PAGE, month_key, beat, rec, owner.strip(), status, note.strip(), who):
                            _saved(f"Saved “{label}” as {status}.")
                            st.rerun()
                        else:
                            st.error(f"Couldn't save: {actions.LAST_ERROR}")
            if data["carried"]:
                st.markdown("**Carried over** (earlier months, not Done)")
                for r in data["carried"]:
                    c1, c2 = st.columns([0.75, 0.25])
                    c1.markdown(f"{r['month_key']} · **{dict(BEATS).get(r['beat'], r['beat'])}**: {r.get('rec') or ''}"
                                f"  \n<small>{r.get('owner') or 'no owner'}, {r['status']}"
                                f"{', ' + r['note'] if r.get('note') else ''}</small>", unsafe_allow_html=True)
                    if c2.button("Mark done", key=f"done_{r['id']}", disabled=not who):
                        actions.set_task_status(r["id"], "Done", who)
                        _saved("Marked done.")
                        st.rerun()

        # ── 2. Weekly minimum ──
        with t_min:
            auto = _field(html, "bareMinimumAuto")
            current = _field(html, "bareMinimumSet")
            week = actions.week_start(today)
            saved = data["minimum"] if isinstance(data["minimum"], dict) else None
            saved_here = saved if saved and saved.get("week_start") == week.isoformat() else None
            st.markdown(f"Week of **{week:%a %d %b}** to **{week + datetime.timedelta(days=6):%a %d %b}**")
            st.caption(f"Worked out: {auto:,} bags (the month's target ÷ its full weeks)." if auto else
                       "The worked-out minimum isn't on the page yet.")
            if saved_here:
                st.info(f"Set to **{int(saved_here['bags']):,}** bags for this week"
                        + (" (the page below is still rebuilding with it)" if current != saved_here.get("bags") else ""))
            with st.form("weekly_min", border=False):
                bags = st.number_input("This week's minimum (bags)", min_value=0, step=50,
                                       value=int(saved_here["bags"]) if saved_here else int(auto or 0))
                c1, c2 = st.columns(2)
                go = c1.form_submit_button("Save for this week", type="primary", disabled=not who)
                clear = c2.form_submit_button("Use the worked-out figure", disabled=not (who and saved_here))
            if go and bags > 0:
                if actions.set_setting(actions.WEEKLY_MINIMUM, {"week_start": week.isoformat(), "bags": int(bags)}, who):
                    rebuild()
                    _saved(f"This week's minimum is now {int(bags):,} bags. The page is rebuilding with it.")
                    st.rerun()
                st.error(f"Couldn't save: {actions.LAST_ERROR}")
            if clear:
                if actions.set_setting(actions.WEEKLY_MINIMUM, None, who):
                    rebuild()
                    _saved("Back to the worked-out minimum. The page is rebuilding.")
                    st.rerun()

        # ── 4. Corporate quote follow-ups ──
        with t_quotes:
            if not quotes:
                st.caption("No open corporate quotes this month.")
            else:
                st.caption("Quotes from this month not invoiced yet. Outcome is our own note; Odoo isn't changed.")
                rows = []
                for q in quotes:
                    f = data["followups"].get(q["no"]) or {}
                    nxt = f.get("next_followup")
                    nxt_d = datetime.date.fromisoformat(str(nxt)) if nxt else None
                    last = f.get("last_chased")
                    rows.append({
                        "Due": "⚠ due" if nxt_d and nxt_d <= today and f.get("outcome") not in ("Won", "Lost") else "",
                        "Client": q["client"], "Quote": q["no"], "Bags": q["bags"], "KES": q["kes"],
                        "Valid until": q["until"],
                        "Outcome": f.get("outcome") or "Open",
                        "Last chased": datetime.date.fromisoformat(str(last)) if last else None,
                        "Next follow-up": nxt_d,
                        "Note": f.get("note") or "",
                    })
                rows.sort(key=lambda r: (r["Due"] == "", r["Next follow-up"] or datetime.date.max, -r["KES"]))
                table = pd.DataFrame(rows)
                for col in ("Last chased", "Next follow-up"):      # the date editor wants real dates, None = empty
                    table[col] = table[col].astype("object")
                edited_df = st.data_editor(
                    table, key="quote_editor", hide_index=True, width="stretch",
                    disabled=["Due", "Client", "Quote", "Bags", "KES", "Valid until"],
                    column_config={
                        "KES": st.column_config.NumberColumn(format="%,d"),
                        "Outcome": st.column_config.SelectboxColumn(options=list(actions.OUTCOMES), required=True),
                        "Last chased": st.column_config.DateColumn(format="DD MMM YYYY"),
                        "Next follow-up": st.column_config.DateColumn(format="DD MMM YYYY"),
                        "Note": st.column_config.TextColumn(width="large"),
                    })
                edited = [{k: _plain(v) for k, v in r.items()} for r in edited_df.to_dict("records")]
                if st.button("Save follow-ups", type="primary", disabled=not who, key="save_quotes"):
                    changed = 0
                    for before, after in zip(rows, edited):
                        keys = ("Outcome", "Last chased", "Next follow-up", "Note")
                        if all(before[k] == after[k] for k in keys):
                            continue
                        q = next(x for x in quotes if x["no"] == after["Quote"])
                        ok = actions.save_followup(q["no"], q["client"], q["bags"], q["kes"], q["until"],
                                                   after["Outcome"], after["Last chased"], after["Next follow-up"],
                                                   (after["Note"] or "").strip(), who)
                        if not ok:
                            st.error(f"Couldn't save {q['no']}: {actions.LAST_ERROR}")
                            break
                        changed += 1
                    else:
                        _saved(f"Saved {changed} follow-up{'s' if changed != 1 else ''}." if changed else "Nothing changed.")
                        st.rerun()
