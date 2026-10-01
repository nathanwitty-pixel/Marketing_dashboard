"""Tests for lib/push_rules.py (the Push Planner's pure logic). Run:
    python -m pytest tests/test_push_planner.py -q
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import push_rules as pr   # noqa: E402

END = datetime.date(2026, 9, 30)


def day(n):
    """ISO date n days before END (0 = END)."""
    return (END - datetime.timedelta(days=n)).isoformat()


# ── facts ────────────────────────────────────────────────────
def test_days_cover_is_none_when_nothing_sold():
    f = pr.facts("REO", "kenya", {}, stock=109, end=END)
    assert f["sold28"] == 0 and f["perDay"] == 0
    assert f["daysCover"] is None            # never runs out at this pace
    assert f["momentum"] is None


def test_pace_and_cover():
    daily = {day(i): 2 for i in range(28)}   # 2 a day for 28 days
    f = pr.facts("KAI", "kenya", daily, stock=30, end=END)
    assert f["sold28"] == 56 and f["perDay"] == 2.0
    assert f["daysCover"] == 15.0
    assert f["sold7"] == 14 and f["soldPrev7"] == 14 and f["momentum"] == 0.0


def test_sales_outside_window_ignored():
    f = pr.facts("KAI", "kenya", {day(28): 50, day(40): 50}, stock=5, end=END)
    assert f["sold28"] == 0


def test_momentum_up_down_and_from_zero():
    up = pr.facts("A", "kenya", {day(0): 6, day(8): 3}, stock=1, end=END)
    assert up["momentum"] == 100.0
    down = pr.facts("A", "kenya", {day(0): 1, day(8): 4}, stock=1, end=END)
    assert down["momentum"] == -75.0
    fresh = pr.facts("A", "kenya", {day(1): 3}, stock=1, end=END)
    assert fresh["momentum"] == 100.0


def test_posting_and_flags_carried():
    f = pr.facts("NALA", "sinza", {}, stock=14, end=END, on_offer=True, is_new=True, price=2100,
                 posting={"postsMonth": 60, "postsLastWeek": 9, "yieldPct": 1.5, "clearPct": 3.0})
    assert (f["postsMonth"], f["postsLastWeek"], f["yieldPct"], f["clearPct"]) == (60, 9, 1.5, 3.0)
    assert f["onOffer"] and f["isNew"] and f["price"] == 2100 and f["market"] == "sinza"


def test_negative_stock_floors_at_zero():
    assert pr.facts("A", "kenya", {}, stock=-4, end=END)["stock"] == 0


# ── peers ────────────────────────────────────────────────────
def _row(bag, market, cat, sold_per_day, price):
    return pr.facts(bag, market, {day(i): sold_per_day for i in range(28)}, stock=10, end=END,
                    category=cat, price=price)


def test_peers_same_market_and_category_only_selling_bags():
    rows = pr.add_peers([
        _row("S1", "kenya", "SLING", 1, 2000),
        _row("S2", "kenya", "SLING", 3, 3000),
        _row("S3", "kenya", "SLING", 0, 9000),     # sells nothing → not a peer
        _row("B1", "kenya", "BACKPACK", 5, 4000),  # other category
        _row("S4", "sinza", "SLING", 9, 1000),     # other market
    ])
    s3 = rows[2]
    assert s3["peerCount"] == 2 and s3["peerPerDay"] == 2.0 and s3["peerPrice"] == 2500
    s1 = rows[0]                                   # excludes itself
    assert s1["peerCount"] == 1 and s1["peerPerDay"] == 3.0


def test_no_peers_gives_none():
    rows = pr.add_peers([_row("X", "uganda", "", 1, 100)])
    assert rows[0]["peerCount"] == 0 and rows[0]["peerPerDay"] is None and rows[0]["peerPrice"] is None


# ── actions ──────────────────────────────────────────────────
def F(**kw):
    """A facts row with sensible defaults, overridden by kw."""
    base = {"bag": "X", "market": "kenya", "category": "SLING", "price": 3000, "stock": 50, "sold7": 0,
            "soldPrev7": 0, "sold28": 0, "perDay": 0.0, "daysCover": None, "momentum": None,
            "postsMonth": 0, "postsLastWeek": 0, "yieldPct": None, "clearPct": None, "soldMonth": None,
            "available": None, "onOffer": False, "isNew": False}
    base.update(kw)
    return base


def test_restock_fast_seller_low_cover():
    code, says, units, conf = pr.action(F(perDay=4.0, stock=12, daysCover=3.0, postsLastWeek=5, momentum=10))
    assert code == "RESTOCK" and "3 days" in says and "Pause its posts" in says
    assert units == 28 and conf == 0.9


def test_stop_posts_when_posted_and_nothing_sold():
    code, says, units, _ = pr.action(F(postsMonth=36, soldMonth=0, stock=10))
    assert code == "STOP_POSTS" and "36 times" in says and units == 9


def test_put_on_offer_stuck_stock():
    code, says, units, conf = pr.action(F(stock=109, sold28=2, perDay=0.07, daysCover=1557.0, clearPct=2.0,
                                          postsMonth=6, yieldPct=5))
    assert code == "PUT_ON_OFFER" and "Deal of the Week" in says and "109 in stock" in says
    assert units == 27.25 and conf == 0.95          # all three extra signals agree


def test_no_offer_when_already_on_offer_or_below_floor():
    assert pr.action(F(stock=109, onOffer=True))[0] != "PUT_ON_OFFER"
    assert pr.action(F(stock=15))[0] != "PUT_ON_OFFER"                 # Kenya floor is 20
    assert pr.action(F(stock=15, market="sinza"))[0] == "PUT_ON_OFFER"  # Sinza floor is 5


def test_post_more_when_posts_work_and_underposted():
    f = F(stock=60, perDay=2.0, daysCover=30.0, yieldPct=90, postsMonth=4, clearPct=60)
    code, says, units, _ = pr.action(f, post_median=12)
    assert code == "POST_MORE" and "posted only 4 times" in says and units == 7.0
    assert pr.action(f, post_median=3)[0] == "WATCH"                    # already posted more than typical


def test_watch_when_nothing_fits():
    assert pr.action(F(stock=30, perDay=1.0, daysCover=30.0, clearPct=50, onOffer=True))[0] == "WATCH"


def test_moves_from_dead_shop_to_selling_low_shop():
    stock = {"MERU": {"KAI": 9}, "HILTON": {"KAI": 2}, "THIKA": {"KAI": 40}}
    sales = {"MERU": {}, "HILTON": {"KAI": 28}, "THIKA": {"KAI": 1}}      # Hilton 2/day, 2 left → 1 day
    mv = pr.moves(stock, sales)
    assert len(mv) == 1 and mv[0]["from"] == "MERU" and mv[0]["to"] == "HILTON"
    assert mv[0]["qty"] == 9                                            # needs 26, Meru has 9
    assert "Move 9 from Meru" in mv[0]["says"]


def test_moves_skip_website_and_well_stocked():
    stock = {"MERU": {"KAI": 9}, "WEBSITE": {}, "HILTON": {"KAI": 100}}
    sales = {"WEBSITE": {"KAI": 50}, "HILTON": {"KAI": 14}}
    assert pr.moves(stock, sales) == []


def test_urgency_and_score():
    assert pr.urgency(0, 30) == 1.0 and pr.urgency(30, 30) == 2.0 and pr.urgency(15, 30, 0.5) == 2.25
    assert pr.score(10, 3000, 1.5, 0.8) == 36000 and pr.score(10, None, 1, 1) == 25000


def test_rank_caps_each_action():
    rows = [{"action": "PUT_ON_OFFER", "score": 100 - i} for i in range(10)] + \
           [{"action": "RESTOCK", "score": 5}, {"action": "WATCH", "score": 999}]
    top = pr.rank(rows, n=15, per_action=5)
    assert [r["action"] for r in top].count("PUT_ON_OFFER") == 5 and top[-1]["action"] == "RESTOCK"
    assert all(r["action"] != "WATCH" for r in top)


# ── reasons ──────────────────────────────────────────────────
def codes(f, ctx=None):
    return [r["code"] for r in pr.reasons(f, ctx or {})]


def test_first_sold_days_ago():
    assert pr.facts("A", "kenya", {day(3): 1, day(10): 2}, stock=1, end=END)["firstSoldDaysAgo"] == 10
    assert pr.facts("A", "kenya", {}, stock=1, end=END)["firstSoldDaysAgo"] is None


def test_not_moving_rules():
    assert pr.not_moving(F(stock=50, clearPct=10, daysCover=20.0))
    assert pr.not_moving(F(stock=50, daysCover=None))
    assert not pr.not_moving(F(stock=50, clearPct=60, daysCover=20.0))
    assert not pr.not_moving(F(stock=3, daysCover=None))               # too little stock to matter


def test_not_posted():
    r = pr.reasons(F(postsMonth=0), {})
    assert r[0]["code"] == "NOT_POSTED" and "0 posts" in r[0]["text"]


def test_posted_not_converting():
    r = [x for x in pr.reasons(F(postsMonth=36, yieldPct=5, soldMonth=2), {}) if x["code"] == "POSTED_NOT_CONVERTING"]
    assert r and "Posted 36 times this month, but sales reached only 5%" in r[0]["text"]
    assert "POSTED_NOT_CONVERTING" not in codes(F(postsMonth=36, yieldPct=80))


def test_price_above_peers():
    r = [x for x in pr.reasons(F(postsMonth=1, price=4800, peerPrice=3200), {}) if x["code"] == "PRICE_ABOVE_PEERS"]
    assert r and "KES 4,800 vs KES 3,200 for the sling bags that do sell in Kenya." == r[0]["text"]
    assert "PRICE_ABOVE_PEERS" not in codes(F(postsMonth=1, price=3500, peerPrice=3200))


def test_wrong_shops_kenya_only():
    ctx = pr.context([], shop_stock={"MERU": {"X": 40}, "HILTON": {"X": 10}}, shop_sales={"HILTON": {"X": 5}})
    r = [x for x in pr.reasons(F(postsMonth=1), ctx) if x["code"] == "WRONG_SHOPS"]
    assert r and r[0]["text"].startswith("80% of its shop stock (40 of 50)")
    assert "WRONG_SHOPS" not in codes(F(postsMonth=1, market="sinza"), ctx)


def test_offer_shadow():
    rival = F(bag="KAI", onOffer=True, perDay=3.0)
    ctx = pr.context([rival])
    r = [x for x in pr.reasons(F(postsMonth=1, perDay=0.2), ctx) if x["code"] == "OFFER_SHADOW"]
    assert r and r[0]["text"] == "Similar sling bags on offer (Kai) are taking the buyers."
    assert "OFFER_SHADOW" not in codes(F(postsMonth=1, perDay=0.2, onOffer=True), ctx)


def test_new_untested():
    assert "NEW_UNTESTED" in codes(F(postsMonth=1, isNew=True, firstSoldDaysAgo=5))
    assert "NEW_UNTESTED" in codes(F(postsMonth=1, isNew=True, firstSoldDaysAgo=None))
    assert "NEW_UNTESTED" not in codes(F(postsMonth=1, isNew=True, firstSoldDaysAgo=20))


def test_market_fit_outside_kenya():
    ctx = pr.context([F(bag="X", market="kenya", perDay=5.0)])
    r = [x for x in pr.reasons(F(market="uganda", postsMonth=1, sold28=0), ctx) if x["code"] == "MARKET_FIT"]
    assert r and "Sells 5 a day in Kenya but 0 in 28 days in Uganda" in r[0]["text"]
    assert "MARKET_FIT" not in codes(F(market="kenya", postsMonth=1), ctx)


def test_slowing():
    r = [x for x in pr.reasons(F(postsMonth=1, sold7=3, soldPrev7=10, momentum=-70.0), {}) if x["code"] == "SLOWING"]
    assert r and "Sold 3 this week vs 10" in r[0]["text"]
    assert "SLOWING" not in codes(F(postsMonth=1, sold7=1, soldPrev7=2, momentum=-50.0))   # too small to call


def test_every_reason_code_has_a_label():
    assert set(pr.REASONS) == set(pr.REASON_LABEL)


def test_fallback_slow_seller_or_overstocked():
    slow = pr.reasons(F(postsMonth=8, yieldPct=60, perDay=0.2, peerPerDay=1.0, daysCover=250.0, stock=50), {})
    assert [x["code"] for x in slow] == ["SLOW_SELLER"] and "0.2 a day vs 1 for similar bags in Kenya" in slow[0]["text"]
    over = pr.reasons(F(postsMonth=8, yieldPct=60, perDay=2.0, peerPerDay=1.0, daysCover=90.0, stock=180), {})
    assert [x["code"] for x in over] == ["OVERSTOCKED"] and "180 in stock is 90 days of stock" in over[0]["text"]
    assert "SLOW_SELLER" not in codes(F(postsMonth=0, perDay=0.2, peerPerDay=1.0))   # a real reason already found


def test_kind_wording():
    assert pr._kind("HANDBAG") == "handbags" and pr._kind("SCHOOL BAG") == "school bags"
    assert pr._kind("SPORT") == "sport bags" and pr._kind("") == "bags" and pr._kind("BACKPACK") == "backpacks"


# ── Laya second opinion (fake model) ─────────────────────────
from lib import push_laya as pl   # noqa: E402


class FakeAnswer:
    def __init__(self, probs):
        self.probabilities = probs
        self.best = max(range(len(probs)), key=probs.__getitem__)
        self.confidence = probs[self.best]
        self.yes = probs[1] if len(probs) > 1 else 0.0


def test_verdict_uses_baseline():
    assert pl.verdict(0.8, 0.45) == "agrees"
    assert pl.verdict(0.6, 0.45) == "unsure"          # needs ≥ 0.70
    assert pl.verdict(0.15, 0.45) == "disagrees"
    assert pl.verdict(0.55, 0.1) == "agrees"          # floor of 0.5


def test_state_text_has_the_numbers():
    t = pl.state_text(F(bag="REO TRAVEL", category="TRAVEL", stock=109, sold28=2, perDay=0.07, daysCover=1557.0,
                        postsMonth=0, price=2800, peerPrice=3000))
    assert "Reo Travel (travel)" in t and "Stock 109" in t and "1557 days" in t and "not on any offer" in t
    assert "KES 2,800" in t and "KES 3,000" in t


def test_main_reason_choice_and_single_yes_no():
    two = F(reasons=[{"code": "NOT_POSTED", "label": "Not posted", "text": "0 posts."},
                     {"code": "PRICE_ABOVE_PEERS", "label": "Priced above", "text": "KES 4,800 vs 3,200."}])
    seen = {}
    def choice(q, opts, st):
        seen["opts"] = opts
        return FakeAnswer([0.2, 0.8])
    m = pl.main_reason(two, choice, None, 0.4)
    assert m["code"] == "PRICE_ABOVE_PEERS" and m["verdict"] == "picks" and len(seen["opts"]) == 2
    flat = pl.main_reason(two, lambda q, o, s: FakeAnswer([0.52, 0.48]), None, 0.4)
    assert flat["verdict"] == "unsure"                 # an even split isn't a pick
    one = F(reasons=[{"code": "NOT_POSTED", "label": "Not posted", "text": "0 posts."}])
    m1 = pl.main_reason(one, None, lambda s, st: FakeAnswer([0.1, 0.9]), 0.4)
    assert m1["code"] == "NOT_POSTED" and m1["verdict"] == "agrees"


def test_second_opinion_order_budget_and_none_safe():
    fine = [F(bag=f"OK{i}", action="WATCH", sold28=50, notMoving=False) for i in range(6)]
    offer = F(bag="REO", action="PUT_ON_OFFER", stock=109)
    stuck = F(bag="ZURI", action="WATCH", stock=144, notMoving=True,
              reasons=[{"code": "NOT_POSTED", "label": "Not posted", "text": "0 posts."}])
    rows = fine + [offer, stuck]
    calls = []
    def yn(s, st):
        calls.append(st)
        return FakeAnswer([0.4, 0.6]) if "Reo" not in st else FakeAnswer([0.05, 0.95])
    left = {"n": 100}
    def budget():
        return left["n"]
    out = pl.second_opinion(rows, [offer], None, yn, budget)
    assert out["asked"] == 2 and out["offerBaseline"] == 0.6
    assert offer["laya"]["offer"]["verdict"] == "agrees" and "reason" in stuck["laya"]
    # Laya unavailable → nothing added, nothing raised
    rows2 = [F(bag="A", action="PUT_ON_OFFER", stock=50)]
    out2 = pl.second_opinion(rows2, rows2, lambda *a: None, lambda *a: None)
    assert out2["asked"] == 0 and "laya" not in rows2[0] and out2["offerBaseline"] is None


def test_offer_opinion_hidden_when_laya_cannot_separate():
    fine = [F(bag=f"OK{i}", action="WATCH", sold28=50, notMoving=False) for i in range(5)]
    offers = [F(bag=f"STUCK{i}", action="PUT_ON_OFFER", stock=100) for i in range(3)]
    # Laya says yes MORE for the healthy bags than for the stuck ones → its opinion is noise here.
    yn = lambda s, st: FakeAnswer([0.3, 0.7]) if "Ok" in st else FakeAnswer([0.6, 0.4])
    out = pl.second_opinion(fine + offers, offers, None, yn)
    assert out["offerReliable"] is False and "couldn't tell" in out["offerNote"]
    assert all(r["laya"]["offer"]["verdict"] == "hidden" for r in offers)
    # …and shown when it does separate them
    offers2 = [F(bag=f"STUCK{i}", action="PUT_ON_OFFER", stock=100) for i in range(3)]
    yn2 = lambda s, st: FakeAnswer([0.6, 0.4]) if "Ok" in st else FakeAnswer([0.1, 0.9])
    out2 = pl.second_opinion(fine + offers2, offers2, None, yn2)
    assert out2["offerReliable"] is True and offers2[0]["laya"]["offer"]["verdict"] == "agrees"


# ── weekly history ───────────────────────────────────────────
def test_week_start_is_sunday():
    assert pr.week_start(datetime.date(2026, 10, 1)) == datetime.date(2026, 9, 27)   # Thu → Sun
    assert pr.week_start(datetime.date(2026, 9, 27)) == datetime.date(2026, 9, 27)


def test_record_week_replaces_not_duplicates():
    top = [{"bag": "REO", "market": "kenya", "action": "POST_MORE", "perDay": 1.0, "stock": 100}]
    h = pr.record_week({}, "2026-09-27", top)
    h = pr.record_week(h, "2026-09-27", top + top)          # same week again
    assert list(h) == ["2026-09-27"] and len(h["2026-09-27"]) == 2
    for i in range(14):
        h = pr.record_week(h, f"2026-0{1 + i // 9}-{10 + i:02d}", top)
    assert len(h) == 12


def test_followup_compares_since_week_start():
    hist = {"2026-09-27": [
        {"bag": "REO", "market": "kenya", "action": "POST_MORE", "perDayBefore": 1.0, "stockBefore": 100},
        {"bag": "ANTI", "market": "kenya", "action": "RESTOCK", "perDayBefore": 30, "stockBefore": 20},
        {"bag": "LOLA", "market": "uganda", "action": "STOP_POSTS", "perDayBefore": 0, "stockBefore": 9}]}
    daily = {"kenya": {"REO": {"2026-09-27": 3, "2026-09-28": 3, "2026-10-03": 1, "2026-10-04": 50}}}
    stock = {"kenya": {"ANTI": 200}, "uganda": {"LOLA": 9}}
    wk, rows = pr.followup(hist, daily, stock, datetime.date(2026, 10, 4))   # next Sunday
    assert wk == "2026-09-27"
    reo = rows[0]
    assert reo["days"] == 7 and reo["perDayAfter"] == 1.0 and reo["result"] == "= about the same"   # today excluded
    assert rows[1]["worked"] is True and rows[1]["result"] == "✓ restocked"
    assert rows[2]["worked"] is None


def test_followup_ignores_the_current_week():
    hist = {"2026-10-04": [{"bag": "A", "market": "kenya", "action": "POST_MORE", "perDayBefore": 1}]}
    assert pr.followup(hist, {}, {}, datetime.date(2026, 10, 6)) == (None, [])
