"""lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-planner.md › Laya).

The rules decide; Laya only comments. Two questions:
  • main reason — for a not-moving bag with 2+ flagged reasons, a choice among THOSE reasons only;
    with one reason, a yes/no on it.
  • offer check — for each "Put on an offer" row, a yes/no on putting it on an offer.
Yes/no answers only count when clearly above Laya's own baseline (laya-on-device skill): the mean
"yes" it gives the same question for 5 bags that are doing fine. verdict = agrees / unsure / disagrees.

`ask_choice(instructions, options, state)` and `ask_yes_no(statement, state)` are passed in (lib.laya's
functions in production, fakes in tests); each returns an object with .probabilities / .best /
.confidence / .yes, or None when Laya can't answer (no model, budget used up).
"""
from __future__ import annotations

from lib.push_rules import LABEL, MARKET

REASON_Q = "Which is the main reason this bag isn't selling?"
REASON_YN = "This is the main reason the bag isn't selling: {text}"
OFFER_Q = "This bag should go on a price offer next week to clear its stock."


def state_text(f):
    """The bag's facts as short plain sentences — what Laya reads."""
    cover = "it did not sell at all" if f["daysCover"] is None else f"that is {f['daysCover']:g} days of stock"
    parts = [
        f"Bag: {f['bag'].title()} ({(f.get('category') or 'bag').lower()}), market: {MARKET.get(f['market'], f['market'])}.",
        f"Stock {f['stock']}. Sold {f['sold28']} in the last 28 days ({f['perDay']:g} a day); {cover}.",
        f"Sold {f['sold7']} this week and {f['soldPrev7']} the week before.",
        f"Posted {f['postsMonth']} times this month." + (f" Posts reached {f['yieldPct']:g}% of the expected sales."
                                                          if f.get("yieldPct") is not None else ""),
        "It is on an offer." if f["onOffer"] else "It is not on any offer.",
    ]
    if f.get("price"):
        parts.append(f"Price KES {f['price']:,}" + (f"; similar bags that sell cost KES {f['peerPrice']:,}."
                                                    if f.get("peerPrice") else "."))
    if f.get("isNew"):
        parts.append("It is a new product.")
    return " ".join(parts)


def verdict(yes, baseline):
    """agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline - 0.25; else unsure."""
    if yes >= max(0.5, baseline + 0.25):
        return "agrees"
    if yes <= baseline - 0.25:
        return "disagrees"
    return "unsure"


def baseline(ask_yes_no, statement, fine_rows, n=5):
    """Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it can't answer)."""
    ys = []
    for f in fine_rows[:n]:
        a = ask_yes_no(statement, state_text(f))
        if a is not None:
            ys.append(a.yes)
    return sum(ys) / len(ys) if ys else None


def main_reason(f, ask_choice, ask_yes_no, reason_base):
    """{"code", "label", "confidence", "verdict"} or None. Choice among the bag's own reasons."""
    rs = f.get("reasons") or []
    if not rs:
        return None
    st = state_text(f)
    if len(rs) == 1:
        a = ask_yes_no(REASON_YN.format(text=rs[0]["text"]), st)
        if a is None:
            return None
        v = verdict(a.yes, reason_base if reason_base is not None else 0.5)
        return {"code": rs[0]["code"], "label": rs[0]["label"], "confidence": round(a.yes, 3), "verdict": v}
    a = ask_choice(REASON_Q, [f"{r['label']}: {r['text']}" for r in rs], st)
    if a is None:
        return None
    pick = rs[a.best]
    # A choice is only worth showing when Laya clearly prefers one option over an even split.
    clear = a.confidence >= min(0.9, 1.0 / len(rs) + 0.15)
    return {"code": pick["code"], "label": pick["label"], "confidence": round(a.confidence, 3),
            "verdict": "picks" if clear else "unsure"}


def offer_check(f, ask_yes_no, offer_base):
    a = ask_yes_no(OFFER_Q, state_text(f))
    if a is None:
        return None
    return {"confidence": round(a.yes, 3), "verdict": verdict(a.yes, offer_base if offer_base is not None else 0.5)}


def second_opinion(rows, top, ask_choice, ask_yes_no, budget_left=lambda: 1):
    """Adds r["laya"] = {"reason": …, "offer": …} to the rows Laya looked at. Order of asking (so a
    small budget goes where it matters): baselines, the offer rows in `top`, other offer rows, then
    not-moving bags by stock value. Returns {"offerBaseline", "reasonBaseline", "asked"}."""
    fine = [r for r in rows if r.get("action") == "WATCH" and not r.get("notMoving") and r["sold28"] >= 10]
    fine.sort(key=lambda r: -r["sold28"])
    ob = baseline(ask_yes_no, OFFER_Q, fine)
    rb = baseline(ask_yes_no, REASON_YN.format(text="nobody has seen it, 0 posts this month."), fine)
    offers = [r for r in top if r.get("action") == "PUT_ON_OFFER"]
    offers += [r for r in rows if r.get("action") == "PUT_ON_OFFER" and r not in offers]
    stuck = sorted((r for r in rows if r.get("reasons")), key=lambda r: -(r["stock"] * (r.get("price") or 2500)))
    asked = 0
    for r in offers:
        if budget_left() <= 0:
            break
        o = offer_check(r, ask_yes_no, ob)
        if o:
            r.setdefault("laya", {})["offer"] = o
            asked += 1
    # Reliability gate: Laya's offer opinion is only shown when it rates the stuck bags clearly higher
    # than the healthy ones. On real data (1 Oct 2026) it did the opposite (healthy 0.61 vs stuck lower)
    # — it can't read the numbers — and showing "disagrees" on 37 of 43 offers would mislead.
    ys = [r["laya"]["offer"]["confidence"] for r in offers if (r.get("laya") or {}).get("offer")]
    sep = (sum(ys) / len(ys) - ob) if (ys and ob is not None) else None
    offer_ok = sep is not None and sep >= 0.05
    if not offer_ok:
        for r in offers:
            if (r.get("laya") or {}).get("offer"):
                r["laya"]["offer"]["verdict"] = "hidden"
    for r in stuck:
        if budget_left() <= 0:
            break
        m = main_reason(r, ask_choice, ask_yes_no, rb)
        if m:
            r.setdefault("laya", {})["reason"] = m
            asked += 1
    return {"offerReliable": offer_ok, "offerSeparation": None if sep is None else round(sep, 3),
            "offerNote": ("" if offer_ok or sep is None else
                          f"Laya couldn't tell the stuck bags from healthy ones this run (it said yes "
                          f"{sum(ys) / len(ys):.0%} for these vs {ob:.0%} for bags that sell fine), so its offer "
                          "opinion is hidden."),
            "offerBaseline": None if ob is None else round(ob, 3),
            "reasonBaseline": None if rb is None else round(rb, 3), "asked": asked,
            "label": LABEL["PUT_ON_OFFER"]}
