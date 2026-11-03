#!/usr/bin/env python3
"""Self-test: recomputes the scripts' key numbers by a second, independent route
(reading the CSV directly, without leakkit) and checks they agree. Also checks
that bad input is refused with a clear message instead of a silent empty result.

Usage: python3 scripts/selftest.py
"""

from __future__ import annotations

import csv
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import basket_value  # noqa: E402
import discount_leak  # noqa: E402
import repeat_rate  # noqa: E402
import tracking_gap  # noqa: E402
import cross_sell_pairs  # noqa: E402
import daily_pulse  # noqa: E402
import dead_stock  # noqa: E402
import feed_zero_impressions  # noqa: E402
import lapsed_customers  # noqa: E402
import price_change  # noqa: E402
from leakkit import load_orders, load_rows, load_thresholds  # noqa: E402

SAMPLE = ROOT / "examples" / "sample-orders-export.csv"
failures = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global failures
    print(("PASS  " if ok else "FAIL  ") + name + (f"  ({detail})" if detail and not ok else ""))
    failures += 0 if ok else 1


# Independent read: first row per order number, skip cancelled.
raw: dict[str, dict] = {}
units: dict[str, int] = {}
with SAMPLE.open(newline="") as fh:
    for row in csv.DictReader(fh):
        n = row["Name"]
        if n not in raw:
            raw[n] = row
            units[n] = 0
        units[n] += int(row["Lineitem quantity"])
live = {n: r for n, r in raw.items() if not r["Cancelled at"]}

t = load_thresholds()
orders = load_orders(SAMPLE)

check("order count matches an independent read", len(orders) == len(live), f"{len(orders)} vs {len(live)}")
check("revenue matches", abs(sum(o.total for o in orders) - sum(float(r["Total"]) for r in live.values())) < 0.01)
check("units per order counted across line-item rows",
      all(o.units == units[o.name] for o in orders))

# Thresholds are read from the file, not hard-coded.
check("thresholds parsed (15% -> 0.15)", abs(t["tracking.gap_flag"] - 0.15) < 1e-9)
check("thresholds parsed (multiplier)", abs(t["discount.spike_multiple"] - 3) < 1e-9)

# Discount share by a second route.
d = discount_leak.analyse(orders, t, {"SARAH15"})
disc = [r for r in live.values() if float(r["Discount Amount"] or 0) > 0 or r["Discount Code"]]
check("discount share agrees", abs(d["share"] - len(disc) / len(live)) < 1e-9)
check("leaked private code detected", any(code == "SARAH15" for code, *_ in d["leaked"]))
d_public = discount_leak.analyse(orders, t, set())
check("same spike on a public code is not called leaked", not d_public["leaked"])

# Basket near misses by a second route.
b = basket_value.analyse(orders, t, 50.0)
low = 50 * (1 - t["aov.near_threshold_band"])
near = [r for r in live.values() if low <= float(r["Subtotal"]) < 50]
check("near-miss count agrees", len(b["near"]) == len(near), f"{len(b['near'])} vs {len(near)}")
from leakkit import LineItem, Order  # noqa: E402
edge = [Order(f"#E{i}", f"e{i}@x.com", datetime(2026, 10, 1), s, s, "", 0, 0, "web", [LineItem("x", 1, s)])
        for i, s in enumerate([42.49, 42.50, 49.99, 50.00])]
eb = basket_value.analyse(edge, t, 50.0)
check("near-miss band includes 42.50 and 49.99, excludes 42.49 and 50.00",
      sorted(o.subtotal for o in eb["near"]) == [42.50, 49.99])
single = sum(1 for n in live if units[n] == 1) / len(live)
check("single-unit share agrees", abs(b["single_share"] - single) < 1e-9)

# Repeat rate by a second route.
rr = repeat_rate.analyse(orders, t)
by_email: dict[str, list[datetime]] = {}
for r in live.values():
    by_email.setdefault(r["Email"].lower(), []).append(datetime.strptime(r["Created at"][:19], "%Y-%m-%d %H:%M:%S"))
as_of = max(dt for v in by_email.values() for dt in v)
window = timedelta(days=int(t["repeat.window_days"]))
elig = back = 0
for dates in by_email.values():
    dates.sort()
    if dates[0] > as_of - window:
        continue
    elig += 1
    back += any(dates[0] < x <= dates[0] + window for x in dates[1:]) or (len(dates) > 1 and dates[1] == dates[0])
check("repeat eligible customers agree", rr["eligible"] == elig, f"{rr['eligible']} vs {elig}")
check("repeat rate agrees", rr["came_back"] == back, f"{rr['came_back']} vs {back}")

# Tracking gap logic.
v, gap, direction = tracking_gap.gap_verdict(181, 236, t["tracking.gap_flag"], t["tracking.min_orders"])
check("tracking: 181 vs 236 is a 23.3% under-tracking gap -> reconcile",
      v == "reconcile" and direction == "under-tracking" and abs(gap + 0.2330508) < 1e-6)
v2, _, _ = tracking_gap.gap_verdict(104, 98, t["tracking.gap_flag"], t["tracking.min_orders"])
check("tracking: 104 vs 98 -> trusted", v2 == "trusted")
v3, _, _ = tracking_gap.gap_verdict(9, 12, t["tracking.gap_flag"], t["tracking.min_orders"])
check("tracking: too few orders -> needs_data", v3 == "needs_data")

# Refusal paths must fail loudly.
for script, args in [("basket_value.py", ["--orders", "missing.csv", "--threshold", "50"]),
                     ("repeat_rate.py", ["--orders", str(ROOT / "README.md")])]:
    p = subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True)
    check(f"{script} refuses bad input with a message", p.returncode != 0 and (p.stderr or p.stdout).strip() != "")

# ---- Scripts added in the 40-skill library ----
from leakkit import LineItem as _LI, Order as _O  # noqa: E402


def mk(n: str, when: datetime, items: list[tuple[str, int, float]], email: str = "") -> _O:
    li = [_LI(a, q, pr) for a, q, pr in items]
    tot = sum(q * pr for _, q, pr in items)
    return _O(n, email or f"{n}@x.com", when, tot, tot, "", 0, 0, "web", li)


# Cross-sell pairs: 400 orders, A+B together 60 times, A alone 40, B alone 40, C 260.
d0 = datetime(2026, 9, 1)
syn = ([mk(f"#P{i}", d0, [("A", 1, 10), ("B", 1, 10)]) for i in range(60)]
       + [mk(f"#A{i}", d0, [("A", 1, 10)]) for i in range(40)]
       + [mk(f"#B{i}", d0, [("B", 1, 10)]) for i in range(40)]
       + [mk(f"#C{i}", d0, [("C", 1, 10)]) for i in range(260)])
cp = cross_sell_pairs.analyse(syn, t)
check("pairs: A+B lift = 60*400/(100*100) = 2.4",
      len(cp["pairs"]) == 1 and abs(cp["pairs"][0]["lift"] - 2.4) < 1e-9 and cp["verdict"] == "found")
check("pairs: an existing bundle is not reported as an opportunity",
      cross_sell_pairs.analyse(syn, t, {frozenset({"A", "B"})})["verdict"] == "none")
check("pairs: 299 orders -> needs_data", cross_sell_pairs.analyse(syn[:299], t)["verdict"] == "needs_data")
sp = cross_sell_pairs.analyse(orders, t)
check("pairs: sample store runs and returns a verdict", sp["verdict"] in ("found", "none"))

# Lapsed customers by a second route, straight from the CSV.
lc = lapsed_customers.analyse(orders, t)
first_two: dict[str, list[datetime]] = {}
for r in live.values():
    first_two.setdefault(r["Email"].lower(), []).append(datetime.strptime(r["Created at"][:19], "%Y-%m-%d %H:%M:%S"))
reps = {e: sorted(v) for e, v in first_two.items() if len(v) >= 2}
gaps = sorted((v[1] - v[0]).days for v in reps.values())
mid = len(gaps) // 2
median = gaps[mid] if len(gaps) % 2 else (gaps[mid - 1] + gaps[mid]) / 2
lapse_days = median * t["lapse.gap_multiple"]
as_of2 = max(max(v) for v in first_two.values())
lapsed_n = sum(1 for v in reps.values() if (as_of2 - v[-1]).days > lapse_days)
check("lapsed: repeat customers agree", lc["repeat_customers"] == len(reps), f"{lc['repeat_customers']} vs {len(reps)}")
check("lapsed: median gap agrees", lc["median_gap"] == median, f"{lc['median_gap']} vs {median}")
check("lapsed: lapsed count agrees", lc["lapsed"] == lapsed_n, f"{lc['lapsed']} vs {lapsed_n}")
few = [mk(f"#L{i}", d0 + timedelta(days=i), [("A", 1, 10)], "same@x.com") for i in range(3)]
check("lapsed: too few repeat customers -> needs_data, default lapse days used",
      lapsed_customers.analyse(few, t)["verdict"] == "needs_data"
      and lapsed_customers.analyse(few, t)["lapse_days"] == t["lapse.default_days"])

# Price change: 3 units/day at 20 for 28 days, then 2 units/day at 24.
pc_orders = []
change = datetime(2026, 9, 29)
for dd in range(-28, 29):
    if dd == 0:
        # A large order on the change day itself, which both windows must exclude.
        pc_orders.append(mk("#C0", change + timedelta(hours=12), [("P", 50, 22.0)]))
        continue
    q, pr = (3, 20.0) if dd < 0 else (2, 24.0)
    pc_orders.append(mk(f"#C{dd}", change + timedelta(days=dd, hours=12), [("P", q, pr)]))
pr_ = price_change.analyse(pc_orders, t, "P", change)
check("price change: change day excluded; units/day -33.3%, revenue/day 60 -> 48 (-20%) -> cost_revenue",
      pr_["verdict"] == "cost_revenue" and abs(pr_["units_change"] + 1 / 3) < 1e-9
      and abs(pr_["revenue_change"] + 0.2) < 1e-9)
check("price change: after-window not finished -> needs_data",
      price_change.analyse(pc_orders[:40], t, "P", change)["verdict"] == "needs_data")

# Daily pulse: 30 orders on each of 4 previous Mondays, 18 on the day -> -40% -> down.
day = datetime(2026, 10, 26)  # a Monday
dp_orders = [mk(f"#D{w}-{i}", day - timedelta(weeks=w, hours=-10), [("A", 1, 10)]) for w in range(1, 5) for i in range(30)]
dp_orders += [mk(f"#T{i}", day + timedelta(hours=10), [("A", 1, 10)]) for i in range(18)]
dp_orders.sort(key=lambda o: o.created)
dp = daily_pulse.analyse(dp_orders, t, day.date())
check("pulse: 18 vs 30 baseline = -40% -> down", dp["verdict"] == "down" and abs(dp["orders_dev"] + 0.4) < 1e-9)
sdp = daily_pulse.analyse(orders, t)
base_counts = [sum(1 for r in live.values() if r["Created at"][:10] == (sdp["day"] - timedelta(weeks=w)).isoformat())
               for w in range(1, int(t["pulse.baseline_weeks"]) + 1)]
check("pulse: sample baseline agrees with a raw count and is under the minimum -> needs_data",
      sdp["verdict"] == "needs_data" and abs(sdp["base_orders"] - sum(base_counts) / len(base_counts)) < 1e-9)

# Feed zero impressions by a second route.
FEED = ROOT / "examples" / "sample-google-products.csv"
with FEED.open(newline="") as fh:
    frows = list(csv.DictReader(fh))
elig_f = [r for r in frows if r["Status"] == "Approved" and r["Availability"] == "in stock"]
zero_f = [r for r in elig_f if int(r["Impr."]) == 0]
fz = feed_zero_impressions.analyse(load_rows(FEED, feed_zero_impressions.COLUMNS, ["id", "impressions"]), t, 14)
check("feed: eligible and zero-impression counts agree",
      fz["eligible"] == len(elig_f) and len(fz["invisible"]) == len(zero_f), f"{fz['eligible']}/{len(fz['invisible'])}")
check("feed: share at or above the flag -> feed_problem",
      fz["verdict"] == ("feed_problem" if len(zero_f) / len(elig_f) >= t["feed.zero_share_flag"] else "products"))
check("feed: a 7-day report -> needs_data", feed_zero_impressions.analyse([], t, 7)["verdict"] == "needs_data")

# Dead stock by a second route.
INV, PRODS = ROOT / "examples" / "sample-inventory-export.csv", ROOT / "examples" / "sample-products-export.csv"
as_of3, start3, covered3 = dead_stock.window(orders, t)
sold_raw = set()
with SAMPLE.open(newline="") as fh:
    for r in csv.DictReader(fh):
        if r["Name"] in live and r["Created at"][:10] >= start3.strftime("%Y-%m-%d"):
            sold_raw.add(r["Lineitem sku"])
stock_raw: dict[str, float] = {}
for r in csv.DictReader(INV.open(newline="")):
    stock_raw[r["SKU"]] = stock_raw.get(r["SKU"], 0) + float(r["Available"])
cost_raw = {r["Variant SKU"]: float(r["Cost per item"]) for r in csv.DictReader(PRODS.open(newline=""))}
dead_raw = sum(u * cost_raw[s] for s, u in stock_raw.items() if u > 0 and s not in sold_raw)
ds = dead_stock.analyse(dead_stock.sold_skus(SAMPLE, start3), covered3, as_of3,
                        load_rows(INV, dead_stock.INVENTORY, ["sku", "available"]),
                        load_rows(PRODS, dead_stock.PRODUCTS, ["sku", "cost"]), t)
check("dead stock: value at cost agrees", abs(ds["dead_value"] - dead_raw) < 0.01, f"{ds['dead_value']} vs {dead_raw}")
check("dead stock: short export -> needs_data",
      dead_stock.analyse(set(), False, as_of3, [], [], t)["verdict"] == "needs_data")

for script, args in [("feed_zero_impressions.py", ["--products", str(ROOT / "README.md"), "--days", "14"]),
                     ("dead_stock.py", ["--orders", str(SAMPLE), "--inventory", "missing.csv", "--products", str(PRODS)]),
                     ("cross_sell_pairs.py", ["--orders", "missing.csv"])]:
    p = subprocess.run([sys.executable, str(HERE / script), *args], capture_output=True, text=True)
    check(f"{script} refuses bad input with a message", p.returncode != 0 and (p.stderr or p.stdout).strip() != "")


print("\nAll checks passed" if not failures else f"\n{failures} check(s) failed")
sys.exit(1 if failures else 0)
