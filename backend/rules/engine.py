"""Rule engine: auto-discovers rules in this package, runs them, combines scores.
Add a rule = add a file in rules/ that defines RULE = MyRule(). This file never changes."""
import importlib
import pkgutil

FLAG_THRESHOLD = 0.4          # risk >= this -> FLAGGED (shows in reviewer console)
HIGH_RISK_THRESHOLD = 0.7     # risk >= this -> alert (SNS/SES)
WEIGHTS = {"velocity.v1": 1.0, "amount.v1": 0.9, "geo.v1": 1.0}
SHADOW = []                   # rule ids that run and are reported but don't affect the score
_SKIP = {"base", "engine"}


def load_rules():
    found = []
    for m in pkgutil.iter_modules(importlib.import_module(__package__).__path__):
        if m.name in _SKIP:
            continue
        mod = importlib.import_module(f"{__package__}.{m.name}")
        if hasattr(mod, "RULE"):
            found.append(mod.RULE)
    return found


def evaluate(tx: dict, history):
    """Returns (risk 0..1, flags). Each flag: rule_id, version, score, reason, evidence, shadow."""
    flags, p = [], 1.0
    for rule in load_rules():
        try:
            res = rule.evaluate(tx, history)
        except Exception as e:                       # a crashing rule never breaks the others
            print(f"[rule {rule.id} failed] {e}")
            continue
        if not res or not res.get("triggered"):
            continue
        shadow = rule.id in SHADOW
        flags.append({"rule_id": rule.id, "version": getattr(rule, "version", 1), "score": res["score"],
                      "reason": res["reason"], "evidence": res.get("evidence", {}), "shadow": shadow})
        if not shadow:                               # noisy-OR: weak signals compound, stays within 0..1
            p *= 1 - res["score"] * WEIGHTS.get(rule.id, 1.0)
    return round(1 - p, 3), flags
