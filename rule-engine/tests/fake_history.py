class FakeHistory:
    """In-memory stand-in for Member 2's database history provider. Same three methods."""
    def __init__(self, txs=None):
        self.txs = list(txs or [])
    def add(self, tx):
        self.txs.append(tx)
    def recent(self, user, sec, at):
        return [t for t in self.txs if t["user_id"] == user and at - sec * 1000 < t["occurred_at"] <= at]
    def amounts(self, user, at):
        return [t["amount"] for t in self.txs if t["user_id"] == user and t["occurred_at"] < at]
    def last_with_geo(self, user, at):
        c = [t for t in self.txs if t["user_id"] == user and t.get("lat") is not None and t["occurred_at"] < at]
        return max(c, key=lambda t: t["occurred_at"], default=None)
