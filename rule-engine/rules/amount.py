from statistics import median
from .base import Rule


class AmountRule(Rule):
    id, version = "amount.v1", 1

    def evaluate(self, tx, history):
        amts = history.amounts(tx["user_id"], tx["occurred_at"])
        if len(amts) < 5:                                  # cold start: use a global threshold
            if tx["amount"] > 100000:
                return self.hit(0.6, f"Large first-time amount {tx['amount']:g}", {"coldStart": True})
            return self.miss()
        med = median(amts)
        mad = median(abs(a - med) for a in amts) or med * 0.1 or 1
        z = 0.6745 * (tx["amount"] - med) / mad            # robust z-score: past fraud can't distort it
        if z < 3.5:
            return self.miss()
        # capped at 0.6: an odd amount alone is flagged; a second signal is needed to reach high risk
        return self.hit(min(0.6, 0.4 + (z - 3.5) / 20),
                        f"Amount {tx['amount']:g} is {tx['amount'] / med:.1f}x this user's median ({med:g})",
                        {"median": med, "mad": mad, "robustZ": round(z, 2)})


RULE = AmountRule()
