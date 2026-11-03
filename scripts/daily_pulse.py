#!/usr/bin/env python3
"""Arithmetic for daily-revenue-pulse.

Compares one day's orders and revenue with the same weekday over the previous
`pulse.baseline_weeks`, from a Shopify Orders export. Reads pulse.* keys from
references/thresholds.md. Defaults to the last full day in the export.

Usage:
  python3 scripts/daily_pulse.py --orders orders.csv [--day 2026-10-30]
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta

from leakkit import load_orders, load_thresholds, pct, table, threshold


def totals(orders, d: date):
    day = [o for o in orders if o.created.date() == d]
    return len(day), sum(o.total for o in day)


def analyse(orders, t, day: date | None = None):
    weeks = int(threshold(t, "pulse.baseline_weeks"))
    flag = threshold(t, "pulse.deviation_flag")
    min_orders = threshold(t, "pulse.min_daily_orders")
    if day is None:
        day = orders[-1].created.date() - timedelta(days=1)  # last full day
    base_days = [day - timedelta(weeks=w) for w in range(1, weeks + 1)]
    if base_days[-1] < orders[0].created.date():
        return {"day": day, "verdict": "needs_data", "reason": "not enough history for the baseline"}
    o_day, r_day = totals(orders, day)
    base = [totals(orders, d) for d in base_days]
    avg_o = sum(b[0] for b in base) / weeks
    avg_r = sum(b[1] for b in base) / weeks
    r = {"day": day, "orders": o_day, "revenue": r_day, "base_orders": avg_o, "base_revenue": avg_r}
    if avg_o < min_orders:
        r.update(verdict="needs_data", reason=f"baseline averages {avg_o:.1f} orders, under {min_orders:g}")
        return r
    r["orders_dev"] = (o_day - avg_o) / avg_o
    r["revenue_dev"] = (r_day - avg_r) / avg_r if avg_r else 0.0
    worst = max(abs(r["orders_dev"]), abs(r["revenue_dev"]))
    r["verdict"] = ("down" if min(r["orders_dev"], r["revenue_dev"]) <= -flag else "up") if worst >= flag else "normal"
    return r


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orders", required=True)
    ap.add_argument("--day", help="YYYY-MM-DD (default: last full day in the export)")
    args = ap.parse_args()
    t = load_thresholds()
    r = analyse(load_orders(args.orders), t, date.fromisoformat(args.day) if args.day else None)
    print(f"Day: {r['day']:%Y-%m-%d (%A)}; baseline: same weekday, previous {threshold(t, 'pulse.baseline_weeks'):g} weeks")
    if "orders" in r:
        print(table(["", "Orders", "Revenue"],
                    [["This day", r["orders"], f"{r['revenue']:,.2f}"],
                     ["Baseline average", f"{r['base_orders']:.1f}", f"{r['base_revenue']:,.2f}"]]))
    if r["verdict"] == "needs_data":
        print(f"needs_data: {r['reason']}")
        return
    print(f"Orders {pct(r['orders_dev'])}, revenue {pct(r['revenue_dev'])} vs baseline "
          f"(flag +/-{pct(threshold(t, 'pulse.deviation_flag'))}) -> {r['verdict']}")


if __name__ == "__main__":
    main()
