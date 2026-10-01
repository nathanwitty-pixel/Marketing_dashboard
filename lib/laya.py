"""lib/laya.py — Laya, the on-device decision model, for the dashboard (spec: docs/push-planner.md › Laya).

Laya answers multiple-choice and yes/no questions about a short text ("state") with calibrated
probabilities. Python port of the tested Kotlin reference (laya-on-device skill): the HF `tokenizers`
library reads tokenizer.json, `onnxruntime` runs model_int4.onnx (techtheist/laya-onnx, en/).

    from lib import laya
    if laya.available():
        a = laya.ask_choice("Which is the main reason this bag isn't selling?", ["...", "..."], facts)
        a.best, a.confidence, a.probabilities
        y = laya.ask_yes_no("This bag should go on an offer next week.", facts); y.yes

It is a second opinion only: callers keep their own rules and show Laya's answer beside them.
Missing model / libraries / a failed self-test → available() is False and nothing raises.
Answers are cached (question + options + state) in laya_cache.json; `budget` caps model calls per run.

    python -m lib.laya --selftest
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import threading
import time

MODEL_DIR = os.environ.get("LAYA_DIR") or os.path.join(os.path.expanduser("~"), "models", "laya-int4")
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(_BASE, "laya_cache.json")

OPT_TOKENS = 48            # tokens per option
YES_NO = ["false: no, the statement does not hold", "true: yes, the statement holds"]


class Answer:
    def __init__(self, probabilities, cached=False):
        self.probabilities = list(probabilities)
        self.best = max(range(len(self.probabilities)), key=self.probabilities.__getitem__) if self.probabilities else 0
        self.cached = cached

    @property
    def confidence(self):
        return self.probabilities[self.best] if self.probabilities else 0.0

    @property
    def yes(self):
        return self.probabilities[1] if len(self.probabilities) > 1 else 0.0


def _clamp(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return 1.0
    return min(5.0, max(0.5, v)) if math.isfinite(v) else 1.0


def _bucket(qtype, k):
    size = "2" if k <= 2 else "3-5" if k <= 5 else "6-10" if k <= 10 else "11+"
    return f"{['choice', 'score', 'noul'][qtype]}:{size}"


def softmax(z):
    if not z:
        return []
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]


class Laya:
    """One loaded model. Use the module functions below (they share one instance)."""

    def __init__(self, model_dir=MODEL_DIR):
        import numpy as np
        import onnxruntime as ort
        from tokenizers import Tokenizer
        self.np = np
        self.tok = Tokenizer.from_file(os.path.join(model_dir, "tokenizer.json"))
        ids = {t: self.tok.token_to_id(t) for t in ("[CLS]", "[SEP]", "[MASK]", "[PAD]")}
        if any(v is None for v in ids.values()):
            raise ValueError("tokenizer.json is missing [CLS]/[SEP]/[MASK]/[PAD]")
        self.cls, self.sep, self.mask, self.pad = ids["[CLS]"], ids["[SEP]"], ids["[MASK]"], ids["[PAD]"]
        cfg = {}
        try:
            with open(os.path.join(model_dir, "rl_agent_config.json"), encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, ValueError):
            pass
        self.max_len = int(cfg.get("max_len", 512))
        self.head_max = int(cfg.get("head_max_len", 192))
        temps = [_clamp(t) for t in (cfg.get("temperature") or [])]
        self.temps = temps if len(temps) == 3 else [1.0, 1.0, 1.0]
        self.temps_by = {k: _clamp(v) for k, v in (cfg.get("temperature_by_options") or {}).items()}
        so = ort.SessionOptions()
        so.log_severity_level = 3
        self.sess = ort.InferenceSession(os.path.join(model_dir, "model_int4.onnx"), so,
                                         providers=["CPUExecutionProvider"])

    def _enc(self, text):
        return self.tok.encode(str(text).replace("[MASK]", " "), add_special_tokens=False).ids

    def _prefix(self, kind, instructions, options):
        head = self._enc(f"{kind} question: {instructions}")
        opts = [[self.mask] + self._enc(" " + o)[:OPT_TOKENS] for o in options]
        budget = self.head_max - sum(len(o) for o in opts)
        if budget < 16:
            per = max(4, (self.head_max - 16) // max(1, len(opts)))
            opts = [o[:per] for o in opts]
            budget = self.head_max - sum(len(o) for o in opts)
        ids = [self.cls] + head[:max(8, budget)] + [self.sep]
        markers = []
        for o in opts:
            markers.append(len(ids))
            ids += o
        ids.append(self.sep)
        return ids, markers

    def run(self, kind, instructions, options, states):
        """Probabilities over `options` for each state (one batch)."""
        np = self.np
        qtype = 2 if kind == "noul" else 0
        pids, markers = self._prefix(kind, instructions, options)
        rows = []
        for st in states:
            room = max(0, self.max_len - len(pids) - 1)
            rows.append((pids + self._enc(st)[:room] + [self.sep])[:self.max_len])
        markers = [m for m in markers if m < self.max_len]
        n, L, k = len(rows), max(len(r) for r in rows), max(1, len(markers))
        ids = np.full((n, L), self.pad, dtype=np.int64)
        att = np.zeros((n, L), dtype=np.int64)
        for i, r in enumerate(rows):
            ids[i, :len(r)] = r
            att[i, :len(r)] = 1
        pos = np.tile(np.array(markers, dtype=np.int64), (n, 1))
        msk = np.ones((n, k), dtype=bool)
        logits = self.sess.run(["logits"], {"input_ids": ids, "attention_mask": att, "marker_pos": pos,
                                            "marker_mask": msk, "qtype": np.full((n,), qtype, dtype=np.int64)})[0]
        scale = self.temps_by.get(_bucket(qtype, len(markers)), self.temps[qtype])
        return [softmax([float(x) / scale for x in row[:len(markers)]]) for row in logits]


# ── Shared instance, cache, budget ───────────────────────────
_lock = threading.Lock()
_inst = None
_tried = False
_err = None
_cache = None
_cache_dirty = False
stats = {"asked": 0, "cached": 0, "seconds": 0.0, "budget_left": 80}


def _load():
    global _inst, _tried, _err
    with _lock:
        if _tried:
            return _inst
        _tried = True
        try:
            if not os.path.isfile(os.path.join(MODEL_DIR, "model_int4.onnx")):
                raise FileNotFoundError(f"no Laya model in {MODEL_DIR}")
            m = Laya(MODEL_DIR)
            ok, detail = _self_test(m)
            if not ok:
                raise ValueError("Laya self-test failed: " + detail)
            _inst = m
        except Exception as e:                                   # noqa: BLE001 — Laya is optional
            _inst, _err = None, f"{type(e).__name__}: {e}"
        return _inst


def available():
    return _load() is not None


def why_unavailable():
    _load()
    return _err


def set_budget(n):
    stats["budget_left"] = int(n)


def _cache_get(key):
    global _cache
    if _cache is None:
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                _cache = json.load(f)
        except (OSError, ValueError):
            _cache = {}
    return _cache.get(key)


def _cache_put(key, probs):
    global _cache_dirty
    _cache_get(key)
    _cache[key] = [round(p, 5) for p in probs]
    _cache_dirty = True


def save_cache():
    global _cache_dirty
    if _cache is not None and _cache_dirty:
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(_cache, f)
            _cache_dirty = False
        except OSError:
            pass


def _ask(kind, instructions, options, state):
    key = hashlib.sha1(json.dumps([kind, instructions, options, state], ensure_ascii=False).encode("utf-8")).hexdigest()
    hit = _cache_get(key)
    if hit is not None:
        stats["cached"] += 1
        return Answer(hit, cached=True)
    m = _load()
    if m is None or stats["budget_left"] <= 0:
        return None
    t = time.time()
    probs = m.run(kind, instructions, options, [state])[0]
    stats["seconds"] += time.time() - t
    stats["asked"] += 1
    stats["budget_left"] -= 1
    _cache_put(key, probs)
    return Answer(probs)


def ask_choice(instructions, options, state):
    """Answer over `options` (probabilities in the same order), or None when Laya can't answer."""
    return _ask("choice", instructions, list(options), state)


def ask_yes_no(statement, state):
    """Answer with probabilities [no, yes] (use .yes), or None."""
    return _ask("noul", statement, YES_NO, state)


def _self_test(m):
    """The model-card check from the laya-on-device skill (LayaModelTest): a double charge goes to
    billing (~0.98) and "or we will cancel" reads as a churn threat. Broken exports score every
    option the same, so they fail here and Laya is not used."""
    state = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
    p = m.run("choice", "Which department should handle this?",
              ["billing: invoices, payments, refunds", "technical: bugs, outages, system errors",
               "other: everything else"], [state])[0]
    churn = m.run("noul", "Does the user threaten to cancel or leave?", YES_NO, [state])[0][1]
    return (p[0] > 0.8 and churn > 0.5, f"billing={p[0]:.3f} churn yes={churn:.3f}")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
        t = time.time()
        if not available():
            print("Laya unavailable:", why_unavailable())
            sys.exit(1)
        print(f"loaded + self-test in {time.time() - t:.1f}s")
        ok, detail = _self_test(_inst)
        print("self-test:", "OK" if ok else "FAILED", detail)
        y = ask_yes_no("This bag should go on an offer next week.",
                       "Bag: REO TRAVEL. Market: Kenya. Stock 109. Sold 2 in the last 28 days. "
                       "Days of stock: 1,526. Not on offer. Posted 0 times this month.")
        n = ask_yes_no("This bag should go on an offer next week.",
                       "Bag: ANTITHEFT. Market: Kenya. Stock 74. Sold 564 this month, 20 a day. "
                       "Days of stock: 4. Already a Power Deal. Posted 36 times.")
        print(f"yes/no — slow bag yes={y.yes:.3f} · selling-out bag yes={n.yes:.3f}")
        save_cache()
