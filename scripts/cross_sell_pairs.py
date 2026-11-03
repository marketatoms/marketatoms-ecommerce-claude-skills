#!/usr/bin/env python3
"""Arithmetic for cross-sell-pair-leak.

Finds pairs of products bought together more often than chance would predict
(lift), from a Shopify Orders export. Reads pairs.* keys from
references/thresholds.md.

  lift(A, B) = orders with A and B * all orders / (orders with A * orders with B)

Usage:
  python3 scripts/cross_sell_pairs.py --orders orders.csv [--bundled "A+B" ...]
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations

from leakkit import load_orders, load_thresholds, table, threshold


def analyse(orders, t, bundled: set[frozenset] | None = None):
    bundled = bundled or set()
    min_orders = threshold(t, "pairs.min_orders")
    min_pair = threshold(t, "pairs.min_pair_orders")
    lift_flag = threshold(t, "pairs.lift_flag")
    n = len(orders)
    if n < min_orders:
        return {"verdict": "needs_data", "orders": n, "pairs": []}
    single = Counter()
    pair = Counter()
    for o in orders:
        names = sorted({i.name for i in o.items})
        single.update(names)
        pair.update(frozenset(p) for p in combinations(names, 2))
    rows = []
    for p, both in pair.items():
        if both < min_pair:
            continue
        a, b = sorted(p)
        lift = both * n / (single[a] * single[b])
        if lift >= lift_flag:
            rows.append({"a": a, "b": b, "both": both, "lift": lift,
                         "share_of_a": both / single[a], "bundled": p in bundled})
    rows.sort(key=lambda r: (-r["lift"], -r["both"]))
    multi = sum(1 for o in orders if len({i.name for i in o.items}) > 1)
    return {"verdict": "found" if any(not r["bundled"] for r in rows) else "none",
            "orders": n, "multi_item_orders": multi, "pairs": rows}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orders", required=True)
    ap.add_argument("--bundled", action="append", default=[], help='An existing bundle, e.g. "Product A+Product B"')
    args = ap.parse_args()
    t = load_thresholds()
    bundled = {frozenset(s.strip() for s in b.split("+")) for b in args.bundled}
    r = analyse(load_orders(args.orders), t, bundled)
    print(f"Orders: {r['orders']}; rule: lift >= {threshold(t, 'pairs.lift_flag'):g} and >= "
          f"{threshold(t, 'pairs.min_pair_orders'):g} orders together; fewer than {threshold(t, 'pairs.min_orders'):g} orders -> needs_data")
    if r["verdict"] == "needs_data":
        print("needs_data: not enough orders to look for pairs")
        return
    print(f"Multi-product orders: {r['multi_item_orders']} ({r['multi_item_orders'] / r['orders'] * 100:.1f}%)")
    if not r["pairs"]:
        print("No pair meets the rule. No cross-sell finding.")
        return
    print(table(["Product A", "Product B", "Orders with both", "Lift", "Share of A orders", "Already bundled"],
                [[p["a"], p["b"], p["both"], f"{p['lift']:.2f}", f"{p['share_of_a'] * 100:.1f}%",
                  "yes" if p["bundled"] else "no"] for p in r["pairs"]]))


if __name__ == "__main__":
    main()
