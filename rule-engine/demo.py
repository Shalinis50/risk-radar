"""Story demo:  python demo.py"""
from rules import engine
from rules.engine import evaluate
from tests.fake_history import FakeHistory
M, NOW = 60000, 10**12
def mk(u, a, at, lat=None, lng=None): return {"id": "x", "user_id": u, "amount": a, "currency": "INR", "merchant": "", "lat": lat, "lng": lng, "occurred_at": at}
h = FakeHistory([mk("asha", 1000 + i * 20, NOW - (600 - i * 20) * M, 19.07, 72.87) for i in range(8)] + [mk("asha", 1050, NOW - 20 * M, 19.07, 72.87)]
                
                + [mk("ravi", 250, NOW - i * 4000) for i in range(1, 9)])
cases = {"Normal purchase": mk("asha", 1100, NOW, 19.07, 72.87),
         "Unusual amount": mk("asha", 48000, NOW, 19.07, 72.87),
         "Impossible travel (Mumbai -> London in 20 min)": mk("asha", 1200, NOW, 51.5, -0.12),
         "Rapid-fire (velocity)": mk("ravi", 250, NOW)}
for name, t in cases.items():
    risk, flags = evaluate(t, h)
    band = "HIGH RISK -> alert" if risk >= engine.HIGH_RISK_THRESHOLD else "FLAGGED" if risk >= engine.FLAG_THRESHOLD else "clean"
    print(f"\n{name}: risk={risk} [{band}]")
    for f in flags: print(f"   - {f['rule_id']}: {f['reason']}")
