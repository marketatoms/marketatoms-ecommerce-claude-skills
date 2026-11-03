#!/usr/bin/env python3
"""Arithmetic for lapsed-customer-leak.

Counts repeat customers (2+ orders) whose last order is older than the store's
own lapse point: `lapse.gap_multiple` x the median days between first and
second order (or `lapse.default_days` when there are too few second orders).
Customers are identified by email. Reads lapse.* keys from
references/thresholds.md.

Usage:
  python3 scripts/lapsed_customers.py --orders orders.csv
"""

from __future__ import annotations

import argparse
import statistics
from collections import defaultdict

from leakkit import load_orders, load_thresholds, pct, threshold


def analyse(orders, t):
    multiple = threshold(t, "lapse.gap_multiple")
    default_days = threshold(t, "lapse.default_days")
    share_flag = threshold(t, "lapse.repeat_share_flag")
    min_repeat = threshold(t, "lapse.min_repeat_customers")

    by_email = defaultdict(list)
    for o in orders:
        if o.email:
            by_email[o.email].append(o)
    as_of = orders[-1].created
    repeaters = {e: sorted(os_, key=lambda o: o.created) for e, os_ in by_email.items() if len(os_) >= 2}
    gaps = [(os_[1].created - os_[0].created).days for os_ in repeaters.values()]
    if len(gaps) >= min_repeat:
        median_gap = statistics.median(gaps)
        lapse_days, basis = max(1.0, median_gap * multiple), "store median"
    else:
        median_gap, lapse_days, basis = None, default_days, "default"
    lapsed = [(e, os_) for e, os_ in repeaters.items() if (as_of - os_[-1].created).days > lapse_days]
    result = {
        "as_of": as_of, "customers": len(by_email), "repeat_customers": len(repeaters),
        "median_gap": median_gap, "lapse_days": lapse_days, "basis": basis,
        "lapsed": len(lapsed),
        "lapsed_past_revenue": sum(o.total for _, os_ in lapsed for o in os_),
    }
    if len(repeaters) < min_repeat:
        result["verdict"] = "needs_data"
        return result
    result["share"] = len(lapsed) / len(repeaters)
    result["verdict"] = "leak" if result["share"] >= share_flag else "ok"
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orders", required=True)
    args = ap.parse_args()
    t = load_thresholds()
    r = analyse(load_orders(args.orders), t)
    print(f"As of {r['as_of']:%Y-%m-%d}: {r['customers']} customers, {r['repeat_customers']} with 2+ orders")
    if r["median_gap"] is not None:
        print(f"Median days first -> second order: {r['median_gap']:g}; lapse point = "
              f"{threshold(t, 'lapse.gap_multiple'):g}x = {r['lapse_days']:g} days")
    else:
        print(f"Too few second orders for a store median; using lapse.default_days = {r['lapse_days']:g} days")
    if r["verdict"] == "needs_data":
        print(f"needs_data: fewer than {threshold(t, 'lapse.min_repeat_customers'):g} repeat customers")
        return
    print(f"Lapsed repeat customers: {r['lapsed']} ({pct(r['share'])}, flag {pct(threshold(t, 'lapse.repeat_share_flag'))}) -> {r['verdict']}")
    print(f"What those lapsed customers spent before: {r['lapsed_past_revenue']:,.2f}")


if __name__ == "__main__":
    main()
