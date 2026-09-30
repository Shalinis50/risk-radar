"""Base class every fraud rule extends. Rules never touch the database: they only call `history`."""
from abc import ABC, abstractmethod


class Rule(ABC):
    id: str = ""        # e.g. "velocity.v1" (stored with every flag)
    version: int = 1    # bump when the logic changes, so old flags stay auditable

    @abstractmethod
    def evaluate(self, tx: dict, history) -> dict:
        """Return self.hit(...) if suspicious, otherwise self.miss()."""

    @staticmethod
    def hit(score: float, reason: str, evidence: dict | None = None) -> dict:
        return {"triggered": True, "score": score, "reason": reason, "evidence": evidence or {}}

    @staticmethod
    def miss() -> dict:
        return {"triggered": False}
