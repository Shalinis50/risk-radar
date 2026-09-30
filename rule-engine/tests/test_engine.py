import os, unittest, importlib
from rules import engine
from tests.fake_history import FakeHistory

M, NOW = 60000, 10**12
def tx(user="u", amount=100, at=NOW, lat=None, lng=None):
    return {"id": f"{user}-{at}-{amount}", "user_id": user, "amount": amount, "currency": "INR", "merchant": "", "lat": lat, "lng": lng, "occurred_at": at}
def ids(flags): return sorted(f["rule_id"] for f in flags)

class VelocityTests(unittest.TestCase):
    def test_burst_triggers(self):
        h = FakeHistory([tx(at=NOW - i * 1000) for i in range(1, 7)])
        r, f = engine.evaluate(tx(at=NOW), h)
        self.assertIn("velocity.v1", ids(f)); self.assertEqual(f[0]["evidence"]["count"], 7)
    def test_normal_pace_silent(self):
        h = FakeHistory([tx(at=NOW - i * 10 * M) for i in range(1, 4)])
        self.assertEqual(engine.evaluate(tx(), h)[1], [])
    def test_other_users_ignored(self):
        h = FakeHistory([tx(user="other", at=NOW - i * 1000) for i in range(1, 9)])
        self.assertEqual(engine.evaluate(tx(), h)[1], [])

class AmountTests(unittest.TestCase):
    def hist(self): return FakeHistory([tx(amount=1000 + i * 20, at=NOW - (100 - i) * M) for i in range(8)])
    def test_outlier_triggers(self):
        r, f = engine.evaluate(tx(amount=60000), self.hist()); self.assertEqual(ids(f), ["amount.v1"])
    def test_normal_amount_silent(self):
        self.assertEqual(engine.evaluate(tx(amount=1100), self.hist())[1], [])
    def test_cold_start_small_ok(self):
        self.assertEqual(engine.evaluate(tx(amount=500), FakeHistory())[1], [])
    def test_cold_start_huge_flagged(self):
        r, f = engine.evaluate(tx(amount=500000), FakeHistory()); self.assertTrue(f[0]["evidence"]["coldStart"])
    def test_identical_history_mad_zero(self):
        h = FakeHistory([tx(amount=500, at=NOW - i * M) for i in range(1, 9)])
        self.assertEqual(ids(engine.evaluate(tx(amount=5000), h)[1]), ["amount.v1"])   # no divide-by-zero
        self.assertEqual(engine.evaluate(tx(amount=510), h)[1], [])

class GeoTests(unittest.TestCase):
    MUM, LON = (19.07, 72.87), (51.5, -0.12)
    def prev(self, mins_ago=30): return FakeHistory([tx(at=NOW - mins_ago * M, lat=self.MUM[0], lng=self.MUM[1])])
    def test_impossible_travel(self):
        r, f = engine.evaluate(tx(lat=self.LON[0], lng=self.LON[1]), self.prev())
        self.assertEqual(ids(f), ["geo.v1"]); self.assertGreater(f[0]["evidence"]["speedKmh"], 900); self.assertGreater(r, 0.7)
    def test_plausible_flight_silent(self):
        self.assertEqual(engine.evaluate(tx(lat=self.LON[0], lng=self.LON[1]), self.prev(mins_ago=60 * 12))[1], [])
    def test_missing_coordinates_skipped(self):
        self.assertEqual(engine.evaluate(tx(), self.prev())[1], [])
    def test_no_previous_location(self):
        self.assertEqual(engine.evaluate(tx(lat=1, lng=1), FakeHistory())[1], [])
    def test_short_distance_ignored(self):
        self.assertEqual(engine.evaluate(tx(lat=19.08, lng=72.88), self.prev(mins_ago=1))[1], [])
    def test_identical_timestamp_no_crash(self):
        r, f = engine.evaluate(tx(at=NOW, lat=self.LON[0], lng=self.LON[1]), FakeHistory([tx(at=NOW - 1, lat=19.07, lng=72.87)]))
        self.assertEqual(ids(f), ["geo.v1"])

class EngineTests(unittest.TestCase):
    def test_first_ever_transaction_clean(self):
        self.assertEqual(engine.evaluate(tx(), FakeHistory()), (0.0, []))
    def test_crashing_rule_is_isolated(self):
        class Boom: id = "boom.v1"; evaluate = lambda self, t, h: 1 / 0
        real = engine.load_rules
        engine.load_rules = lambda: real() + [Boom()]
        try:
            h = FakeHistory([tx(at=NOW - i * 1000) for i in range(1, 7)])
            r, f = engine.evaluate(tx(), h)
        finally: engine.load_rules = real
        self.assertEqual(ids(f), ["velocity.v1"])        # others still ran
    def test_noisy_or_math(self):
        class A: id, evaluate = "a", lambda s, t, h: {"triggered": True, "score": 0.5, "reason": "a"}
        class B: id, evaluate = "b", lambda s, t, h: {"triggered": True, "score": 0.5, "reason": "b"}
        real = engine.load_rules; engine.load_rules = lambda: [A(), B()]
        try: r, f = engine.evaluate(tx(), FakeHistory())
        finally: engine.load_rules = real
        self.assertEqual(r, 0.75)                        # 1 - 0.5*0.5
    def test_shadow_rule_reported_but_not_scored(self):
        h = FakeHistory([tx(at=NOW - i * 1000) for i in range(1, 7)])
        engine.SHADOW.append("velocity.v1")
        try: r, f = engine.evaluate(tx(), h)
        finally: engine.SHADOW.remove("velocity.v1")
        self.assertEqual(r, 0.0); self.assertTrue(f[0]["shadow"])
    def test_output_contract(self):
        h = FakeHistory([tx(at=NOW - i * 1000) for i in range(1, 7)])
        r, f = engine.evaluate(tx(), h)
        self.assertEqual(set(f[0]), {"rule_id", "version", "score", "reason", "evidence", "shadow"})
        self.assertTrue(0 <= r <= 1)
    def test_new_rule_file_is_auto_discovered(self):
        src = os.path.join(os.path.dirname(__file__), "..", "examples", "round_amount.py")
        dst = os.path.join(os.path.dirname(engine.__file__), "round_amount.py")
        with open(src) as a, open(dst, "w") as b: b.write(a.read())
        importlib.invalidate_caches()
        try: r, f = engine.evaluate(tx(amount=20000), FakeHistory([tx(amount=20000, at=NOW - i * M) for i in range(1, 8)]))
        finally: os.remove(dst)
        self.assertIn("round.v1", ids(f))

if __name__ == "__main__":
    unittest.main()
