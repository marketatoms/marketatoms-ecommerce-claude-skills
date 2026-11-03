---
name: price-change-leak
description: Checks what a past price change actually did to one product - units and revenue per day for four weeks before and after, and gross profit if costs are known - so the owner can see whether the new price earned or cost money. Use after raising or lowering a price, before a store-wide price change, or when a product's sales fell for no obvious reason. Boundary: price-competitiveness-leak compares the store's price with other sellers; this skill compares the store's own price before and after a change.
---

# Price Change Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/price_change.py`.

## Use this skill when

- "I raised the price last month - did it help or hurt?"
- Before rolling a price change out to more products.
- A product's sales dropped and a price change is a suspect.

## Required input

- **Shopify Orders export** covering `pricing.compare_days` before and after
  the change: Shopify admin > **Orders** > **Export** > CSV.
- The **product name** exactly as it appears in `Lineitem name`, and the
  **date** the new price went live.
- Optional: **cost per item** (Products export, `Cost per item`) to compare
  gross profit, not just revenue.
- Anything else that changed in the same weeks (ads, a sale, a stock-out).

## Live data (MarketAtoms MCP)

No live tool gives product-level daily sales. Use the export.

## Analysis workflow

1. Run the script:
   `python3 scripts/price_change.py --orders orders.csv --product "Name" --changed YYYY-MM-DD`.
   It compares `pricing.compare_days` on each side, excluding the change day.
2. It returns `needs_data` if the after-window isn't finished or either side
   has fewer than `pricing.min_units` units.
3. Read units per day, revenue per day and average price on each side.
4. If cost per item is given: gross profit = (average price - cost) x units,
   per side.
5. List other changes in the same weeks; if there were any, the result is
   confounded and says so.

## Decision rules

- Units per day down by `pricing.units_drop_flag` or more **and** revenue per
  day down: `cost_revenue`.
- Revenue per day up: `gained_revenue`.
- Anything else: `no_clear_change`.
- Report gross profit next to the verdict when costs are known: a price rise
  can lose revenue and still gain profit. Both go to the owner.
- Other big changes in the same window: verdict marked `confounded`.

## Output format

Summary line: product, change date, verdict, gross profit change if known.

| Window | Units | Units/day | Revenue | Revenue/day | Avg price | Gross profit |
|---|---|---|---|---|---|---|

Then: **Other changes in the window**, **Approval needed** (any price change
is the owner's).

## Practical example

*Made-up numbers for illustration.* Bamboo Sleep Set, $60 -> $70 on
September 15; cost $31.50.

| Window | Units | Units/day | Revenue | Revenue/day | Gross profit |
|---|---|---|---|---|---|
| 28 days before | 112 | 4.00 | $6,720 | $240.00 | $3,192 |
| 28 days after | 84 | 3.00 | $5,880 | $210.00 | $3,234 |

Units per day -25.0%, revenue per day -12.5%: `cost_revenue`. Gross profit is
$42 higher, so the rise lost revenue but not profit. Keeping the price is a
volume-vs-margin decision for the owner.

## Guardrails

- Never change a price.
- Same number of days on both sides, always; never compare a partial window.
- Seasonality and ads can move sales as much as price; name what else changed.
