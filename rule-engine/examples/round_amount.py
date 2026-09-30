"""Proof of extensibility: copy into rules/ and the engine picks it up with NO engine change."""
from .base import Rule


class RoundAmountRule(Rule):
    id, version = "round.v1", 1

    def evaluate(self, tx, history):
        if tx["amount"] >= 10000 and tx["amount"] % 1000 == 0:
            return self.hit(0.3, f"Suspiciously round amount {tx['amount']:g}")
        return self.miss()


RULE = RoundAmountRule()
