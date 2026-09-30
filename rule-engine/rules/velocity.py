from .base import Rule

WINDOWS = [(60, 5), (3600, 20)]     # (window seconds, max transactions allowed)


class VelocityRule(Rule):
    id, version = "velocity.v1", 1

    def evaluate(self, tx, history):
        worst = None
        for sec, limit in WINDOWS:
            count = len(history.recent(tx["user_id"], sec, tx["occurred_at"])) + 1   # +1 = this transaction
            if count > limit and (worst is None or count / limit > worst[3]):
                worst = (sec, limit, count, count / limit)
        if not worst:
            return self.miss()
        sec, limit, count, ratio = worst
        return self.hit(min(1, 0.5 + (ratio - 1) * 0.5), f"{count} transactions in {sec}s (limit {limit})",
                        {"count": count, "windowSec": sec, "limit": limit})


RULE = VelocityRule()
