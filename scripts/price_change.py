#!/usr/bin/env python3
"""Arithmetic for price-change-leak.

Compares one product's units and revenue per day for `pricing.compare_days`
before and after a price change, from a Shopify Orders export. The change day
itself is excluded. Reads pricing.* keys from references/thresholds.md.

Usage:
  python3 scripts/price_change.py --orders orders.csv --product "Product name" --changed 2026-09-15
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta

from leakkit import load_orders, load_thresholds, pct, table, threshold


def window(orders, product: str, start: datetime, end: datetime):
    units, revenue = 0, 0.0
    for o in orders:
        if start <= o.created < end:
            for i in o.items:
                if i.name == product:
                    units += i.quantity
                    revenue += i.quantity * i.price
    return units, revenue


def analyse(orders, t, product: str, changed: datetime):
    days = int(threshold(t, "pricing.compare_days"))
    drop_flag = threshold(t, "pricing.units_drop_flag")
    min_units = threshold(t, "pricing.min_units")
    day = changed.replace(hour=0, minute=0, second=0, microsecond=0)
    before = window(orders, product, day - timedelta(days=days), day)
    after = window(orders, product, day + timedelta(days=1), day + timedelta(days=1 + days))
    last = orders[-1].created
    r = {"days": days, "before": before, "after": after,
         "after_complete": last >= day + timedelta(days=days)}
    if not r["after_complete"] or before[0] < min_units or after[0] < min_units:
        r["verdict"] = "needs_data"
        return r
    upd = (after[0] - before[0]) / before[0]
    rpd = (after[1] - before[1]) / before[1]
    r["units_change"], r["revenue_change"] = upd, rpd
    if upd <= -drop_flag and rpd < 0:
        r["verdict"] = "cost_revenue"
    elif rpd > 0:
        r["verdict"] = "gained_revenue"
    else:
        r["verdict"] = "no_clear_change"
    return r


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orders", required=True)
    ap.add_argument("--product", required=True, help="Exact Lineitem name")
    ap.add_argument("--changed", required=True, help="YYYY-MM-DD, the day the new price went live")
    args = ap.parse_args()
    t = load_thresholds()
    r = analyse(load_orders(args.orders), t, args.product, datetime.fromisoformat(args.changed))
    d = r["days"]
    (ub, rb), (ua, ra) = r["before"], r["after"]
    print(f"{args.product}: {d} days before vs {d} days after {args.changed} (change day excluded)")
    print(table(["", "Units", "Units/day", "Revenue", "Revenue/day", "Avg price"],
                [["Before", ub, f"{ub / d:.2f}", f"{rb:,.2f}", f"{rb / d:,.2f}", f"{rb / ub:,.2f}" if ub else "-"],
                 ["After", ua, f"{ua / d:.2f}", f"{ra:,.2f}", f"{ra / d:,.2f}", f"{ra / ua:,.2f}" if ua else "-"]]))
    if r["verdict"] == "needs_data":
        why = "the after-window isn't complete yet" if not r["after_complete"] else \
            f"fewer than {threshold(t, 'pricing.min_units'):g} units on one side"
        print(f"needs_data: {why}")
        return
    print(f"Units/day {pct(r['units_change'])}, revenue/day {pct(r['revenue_change'])} -> {r['verdict']}")


if __name__ == "__main__":
    main()
