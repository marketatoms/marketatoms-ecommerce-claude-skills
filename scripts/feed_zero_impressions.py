#!/usr/bin/env python3
"""Arithmetic for feed-zero-impressions-leak.

Lists approved, in-stock products with zero Shopping impressions over the
report's date range, and the share of the eligible feed they make up. The
report must cover at least `feed.zero_impression_days`. Reads feed.* keys from
references/thresholds.md.

Input: a Google Ads Products report (or Merchant Center product performance)
downloaded as CSV, one row per item, joined with Merchant Center status and
availability if those columns are not already in it.

Usage:
  python3 scripts/feed_zero_impressions.py --products products.csv --days 14
"""

from __future__ import annotations

import argparse

from leakkit import load_rows, load_thresholds, money, pct, table, threshold

COLUMNS = {
    "id": ["Item ID", "Offer ID", "id"],
    "title": ["Product title", "Title", "Item title"],
    "impressions": ["Impr.", "Impressions"],
    "clicks": ["Clicks"],
    "status": ["Status", "Approval status", "Item status"],
    "availability": ["Availability"],
}


def analyse(rows, t, days: int):
    need_days = threshold(t, "feed.zero_impression_days")
    share_flag = threshold(t, "feed.zero_share_flag")
    min_products = threshold(t, "feed.min_products")
    if days < need_days:
        return {"verdict": "needs_data", "reason": f"report covers {days} days, needs {need_days:g}"}
    eligible = [r for r in rows
                if (not r["status"] or r["status"].lower() in ("approved", "active", "eligible"))
                and (not r["availability"] or r["availability"].lower().replace("_", " ") == "in stock")]
    invisible = [r for r in eligible if money(r["impressions"]) == 0]
    out = {"rows": len(rows), "eligible": len(eligible), "invisible": invisible,
           "excluded": len(rows) - len(eligible)}
    if len(eligible) < min_products:
        out["verdict"] = "products_only"  # list them, don't judge the feed
        return out
    out["share"] = len(invisible) / len(eligible)
    out["verdict"] = "feed_problem" if out["share"] >= share_flag else ("products" if invisible else "ok")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--products", required=True)
    ap.add_argument("--days", type=int, required=True, help="Number of days the report covers")
    args = ap.parse_args()
    t = load_thresholds()
    rows = load_rows(args.products, COLUMNS, ["id", "impressions"])
    r = analyse(rows, t, args.days)
    if r["verdict"] == "needs_data":
        print(f"needs_data: {r['reason']}")
        return
    print(f"Products in report: {r['rows']}; approved and in stock: {r['eligible']} "
          f"({r['excluded']} disapproved or out of stock, not judged here)")
    print(f"Zero impressions in {args.days} days: {len(r['invisible'])}")
    if "share" in r:
        print(f"Share of eligible feed: {pct(r['share'])} (flag {pct(threshold(t, 'feed.zero_share_flag'))}) -> {r['verdict']}")
    else:
        print(f"Fewer than {threshold(t, 'feed.min_products'):g} eligible products: products listed, feed share not judged")
    if r["invisible"]:
        print(table(["Item ID", "Title"], [[x["id"], x["title"]] for x in r["invisible"]]))


if __name__ == "__main__":
    main()
