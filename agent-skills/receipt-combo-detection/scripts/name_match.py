"""name_match.py — match a till's combo product name to a combo on the offer list by its slots: exact overlap
(any order) first, then the closest names (skill: receipt-combo-detection). Pure Python.

    slots = [(label, combo_list_slots(label)) for label in offer_list]   # "A/B+C" = slot {A,B} + slot {C}
    match_offer("Standard Travel Black + Code 3 Black Combo", slots)     # -> label or None
"""
import difflib
import itertools
import re

# Words that describe a product's category or colour, not its identity — dropped before matching names.
# Replace with your own catalogue's vocabulary.
_COMBO_CATEGORY = {"HANDBAG", "TRAVEL", "BACKPACK", "BAG", "SLING", "SLINGBAG", "MESSENGER", "LUNCH", "LUNCHSET",
                   "LUNCHBAG", "CHEST", "BP", "HB", "COMBO"}
_COMBO_COLOURS = {"BLACK", "GREY", "GREEN", "BROWN", "NUDE", "RED", "BLUE", "MAROON", "SPICE", "BEIGE", "CHOCOLATE",
                  "YELLOW", "DOTTED", "CRACKED", "DARK", "TT", "PURPLE", "PINK", "ORANGE", "WHITE", "GOLD", "SILVER", "NAVY"}
# Promo wording on the offer list -> catalogue wording, e.g. {"LAPTOP BACKPACK": "CODE 3"}. Add yours.
_COMBO_PHRASE_ALIAS = {}
# A bare word that names several products ("MINI" = Mini X / Mini Y) never stands in for one of them.
_OPT_TOO_VAGUE = {"MINI", "BIG", "SMALL", "BABY", "NEO", "SAMPLE"}
# A slot that is ONLY a category word names one product, e.g. {"TRAVEL": "STANDARD"} (a bare "Travel" on the
# list = the Standard Travel bag). Add yours.
_BARE_CATEGORY_ALIAS = {}


def _combo_norm_option(opt):
    """One combo slot-option → its distinctive bag token(s), colours/category words
    and promo aliases stripped so the offer list and till names line up."""
    s = " " + str(opt).upper().strip() + " "
    for a, b in _COMBO_PHRASE_ALIAS.items():
        s = s.replace(" " + a + " ", " " + b + " ")
    words = [w for w in re.split(r"[^A-Z0-9]+", s) if w]
    kept = [w for w in words if w not in _COMBO_CATEGORY and w not in _COMBO_COLOURS]
    if not kept:                                   # only a category word, e.g. a bare "Travel"
        for w in words:
            if w in _BARE_CATEGORY_ALIAS:
                return _BARE_CATEGORY_ALIAS[w]
    return " ".join(kept).strip()


def combo_list_slots(label):
    """Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]."""
    return [set(filter(None, (_combo_norm_option(o) for o in slot.split("/"))))
            for slot in str(label).split("+")]


def combo_till_slots(name):
    """Till name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same shape."""
    return [set(filter(None, (_combo_norm_option(o) for o in re.split(r"\bor\b", slot, flags=re.I))))
            for slot in str(name).split("+")]


def opt_close(a, b):
    """Two normalised slot options name the same bag, loosely: equal ignoring spaces
    ("ANTI THEFT" = "ANTITHEFT"), one a word-prefix of the other ("CODE" = "CODE 3"), or
    ≥ 85 % similar spelling."""
    if a == b:
        return True
    ca, cb = a.replace(" ", ""), b.replace(" ", "")
    if ca == cb:
        return True
    # Word-prefix only when the short name is a bag of its own — a bare "MINI" could be Mini
    # Umbra, Mini Maya or Mini Manbag, so it never stands in for one of them.
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    if long_.startswith(short + " ") and short not in _OPT_TOO_VAGUE:
        return True
    return len(ca) >= 4 and len(cb) >= 4 and difflib.SequenceMatcher(None, ca, cb).ratio() >= 0.85


def slots_fit(o, s, close=False):
    """Same slot count and every slot overlaps under SOME pairing (any order: the list's
    "Code 3+Travel" is rung "Standard Travel + Code 3"). close=True compares options loosely."""
    if len(o) != len(s):
        return False
    hit = (lambda x, y: any(opt_close(a, b) for a in x for b in y)) if close else (lambda x, y: bool(x & y))
    return any(all(hit(o[i], s[j]) for i, j in enumerate(perm)) for perm in itertools.permutations(range(len(s))))


def match_offer(name, list_slots):
    """The offer-list label this till combo maps to, or None if it is not on the list. Exact slot
    overlap first (list order, then any order); failing that, the CLOSEST listed combo by
    name (opt_close per slot) — so short or misspelt till names ("Standard + Code Combo")
    still find their running combo."""
    o = combo_till_slots(name)
    for label, s in list_slots:
        if len(s) == len(o) and all((o[i] & s[i]) for i in range(len(s))):
            return label
    for close in (False, True):
        for label, s in list_slots:
            if slots_fit(o, s, close):
                return label
    return None
