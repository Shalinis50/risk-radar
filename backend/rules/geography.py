from math import radians, sin, cos, asin, sqrt
from .base import Rule

MAX_SPEED_KMH = 900     # roughly a commercial flight
MIN_DISTANCE_KM = 50    # ignore GPS noise


def haversine_km(a, b):
    dlat, dlng = radians(b["lat"] - a["lat"]), radians(b["lng"] - a["lng"])
    h = sin(dlat / 2) ** 2 + cos(radians(a["lat"])) * cos(radians(b["lat"])) * sin(dlng / 2) ** 2
    return 2 * 6371 * asin(sqrt(h))


class GeographyRule(Rule):
    id, version = "geo.v1", 1

    def evaluate(self, tx, history):
        if tx.get("lat") is None or tx.get("lng") is None:
            return self.miss()                             # never guess on missing data
        prev = history.last_with_geo(tx["user_id"], tx["occurred_at"])
        if not prev:
            return self.miss()
        dist = haversine_km(prev, tx)
        hours = max((tx["occurred_at"] - prev["occurred_at"]) / 3.6e6, 1 / 60)   # floor at 1 minute
        speed = dist / hours
        if dist < MIN_DISTANCE_KM or speed <= MAX_SPEED_KMH:
            return self.miss()
        return self.hit(min(1, 0.6 + min(speed, 5000) / 12500),
                        f"{round(dist)} km in {hours * 60:.0f} min ({round(speed)} km/h)",
                        {"distanceKm": round(dist), "speedKmh": round(speed),
                         "from": {"lat": prev["lat"], "lng": prev["lng"]}, "to": {"lat": tx["lat"], "lng": tx["lng"]}})


RULE = GeographyRule()
