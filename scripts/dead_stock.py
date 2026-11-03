#!/usr/bin/env python3
"""Arithmetic for dead-stock-leak.

SKUs with stock on hand and zero units sold in the last `stock.dead_days`
(ending on the last order date in the export), valued at cost. Reads stock.*
keys from references/thresholds.md.

Inputs:
  --orders     Shopify Orders export covering at least stock.dead_days
  --inventory  Shopify inventory export (SKU, Available; one row per location)
  --products   Shopify Products export (Variant SKU, Cost per item)

Usage:
  python3 scripts/dead_stock.py --orders orders.csv --inventory inventory.csv --products products.csv
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import timedelta

from leakkit import load_orders, load_rows, load_thresholds, money, pct, table, threshold

INVENTORY = {"sku": ["SKU", "Variant SKU"], "available": ["Available", "On hand"], "title": ["Title"]}
PRODUCTS = {"sku": ["Variant SKU", "SKU"], "cost": ["Cost per item", "Cost"]}


def sold_skus(orders_path, start):
    """SKUs sold since `start`. Reads Lineitem sku directly (load_orders keeps names, not SKUs)."""
    sold = set()
    with open(orders_path, newline="", encoding="utf-8-sig") as fh:
        current_cancelled = {}
        for row in csv.DictReader(fh):
            name = row.get("Name", "")
            if name not in current_cancelled:
                current_cancelled[name] = bool((row.get("Cancelled at") or "").strip())
            if current_cancelled[name]:
                continue
            created = (row.get("Created at") or "")[:10]
            if created and created >= start.strftime("%Y-%m-%d") and row.get("Lineitem sku"):
                sold.add(row["Lineitem sku"].strip())
    return sold


def window(orders, t):
    """(as_of, start, covered): the dead-stock window ends on the last order date."""
    days = int(threshold(t, "stock.dead_days"))
    as_of = orders[-1].created
    start = as_of - timedelta(days=days)
    return as_of, start, orders[0].created <= start


def analyse(sold: set[str], covered: bool, as_of, inventory, products, t):
    days = int(threshold(t, "stock.dead_days"))
    share_flag = threshold(t, "stock.dead_value_share_flag")
    if not covered:
        return {"verdict": "needs_data", "reason": f"orders export covers less than {days} days"}
    units = defaultdict(float)
    titles = {}
    for r in inventory:
        if r["sku"]:
            units[r["sku"]] += money(r["available"])
            titles.setdefault(r["sku"], r["title"])
    cost = {r["sku"]: money(r["cost"]) for r in products if r["sku"]}
    missing_cost = sorted(s for s, u in units.items() if u > 0 and s not in cost)
    total_value = sum(u * cost.get(s, 0) for s, u in units.items() if u > 0)
    dead = sorted(((s, titles.get(s, ""), u, u * cost.get(s, 0)) for s, u in units.items()
                   if u > 0 and s not in sold), key=lambda x: -x[3])
    dead_value = sum(d[3] for d in dead)
    share = dead_value / total_value if total_value else 0.0
    return {"as_of": as_of, "days": days, "dead": dead, "dead_value": dead_value, "total_value": total_value,
            "share": share, "missing_cost": missing_cost,
            "verdict": "leak" if share >= share_flag else ("skus" if dead else "ok")}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orders", required=True)
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--products", required=True)
    args = ap.parse_args()
    t = load_thresholds()
    as_of, start, covered = window(load_orders(args.orders), t)
    r = analyse(sold_skus(args.orders, start), covered, as_of,
                load_rows(args.inventory, INVENTORY, ["sku", "available"]),
                load_rows(args.products, PRODUCTS, ["sku", "cost"]), t)
    if r["verdict"] == "needs_data":
        print(f"needs_data: {r['reason']}")
        return
    print(f"No units sold in the {r['days']} days to {r['as_of']:%Y-%m-%d}, but in stock:")
    if r["dead"]:
        print(table(["SKU", "Title", "Units on hand", "Value at cost"],
                    [[s, ti, f"{u:g}", f"{v:,.2f}"] for s, ti, u, v in r["dead"]]))
    else:
        print("none")
    print(f"Dead stock at cost: {r['dead_value']:,.2f} of {r['total_value']:,.2f} "
          f"({pct(r['share'])}, flag {pct(threshold(t, 'stock.dead_value_share_flag'))}) -> {r['verdict']}")
    if r["missing_cost"]:
        print(f"No cost per item for: {', '.join(r['missing_cost'])} (valued at 0; add costs in Shopify)")


if __name__ == "__main__":
    main()
