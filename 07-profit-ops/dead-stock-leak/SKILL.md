---
name: dead-stock-leak
description: Finds SKUs with stock on hand that have not sold a single unit in 90 days, values them at cost, and shows what share of inventory money is tied up in them. Use before reordering, at quarter end, when cash is tight, or before planning a clearance. Boundary: stockout-ad-spend-leak covers products running out while ads push them; this skill covers products that sit still.
---

# Dead Stock Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/dead_stock.py`.

## Use this skill when

- Before placing a reorder.
- Cash is tight: how much money is sitting on the shelf?
- Quarter end, or planning a clearance.

## Required input

- **Shopify Orders export** covering at least `stock.dead_days`: Shopify admin
  > **Orders** > **Export** > CSV (`Lineitem sku` must be filled).
- **Shopify inventory export:** Shopify admin > **Products** > **Inventory** >
  **Export** > CSV. Columns: SKU, Available (one row per location; the script
  adds them up).
- **Shopify Products export** for costs: Shopify admin > **Products** >
  **Export** > CSV. Columns: Variant SKU, Cost per item. SKUs with no cost are
  valued at 0 and listed.

## Live data (MarketAtoms MCP)

No live tool reads inventory yet. Use the exports.

## Analysis workflow

1. Run the script:
   `python3 scripts/dead_stock.py --orders orders.csv --inventory inventory.csv --products products.csv`.
2. The window is the `stock.dead_days` up to the last order date in the export.
   If the export is shorter: `needs_data`.
3. Dead SKU = units available > 0 and no units sold in the window. Value =
   units x cost per item.
4. Dead stock share = dead value / value of all stock on hand at cost.
5. Ask the owner which dead SKUs are new arrivals, pre-orders or seasonal
   (for example swimwear in winter); those are reported separately, not as dead.

## Decision rules

- Dead stock share >= `stock.dead_value_share_flag`: `leak` - inventory money
  is tied up at store level.
- Dead SKUs but share under the flag: `skus` - list them for a decision each.
- No dead SKUs: `ok`.
- Orders export shorter than `stock.dead_days`: `needs_data`.
- SKUs with missing cost: listed; the share is understated and says so.

## Output format

Summary line: dead SKUs, value at cost, share of inventory, verdict.

| SKU | Title | Units on hand | Cost per item | Value at cost | New/seasonal? |
|---|---|---|---|---|---|

Then: **Missing costs**, **Options for the owner** (bundle, clearance, return
to supplier, stop reordering), **Approval needed**.

## Practical example

*Made-up numbers for illustration* (the repository's sample store and
`examples/sample-inventory-export.csv`, `examples/sample-products-export.csv`):
in the 90 days to October 31, Muslin Swaddle 2-pack (140 units, $1,260.00 at
cost) and Silicone Teething Ring (260 units, $1,040.00) sold nothing.
$2,300.00 of $16,140.90 stock at cost: 14.2%, under the 20% flag: `skus`.
Two decisions for the owner, not a store-wide problem.

## Guardrails

- Never change inventory, prices, or create discounts or clearance collections.
- A SKU that sells only in one season is not dead; ask before calling it.
- Value at cost, never at retail price.
