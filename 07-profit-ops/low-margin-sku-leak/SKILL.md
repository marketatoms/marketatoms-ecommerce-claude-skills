---
name: low-margin-sku-leak
description: Works out gross margin per SKU from net sales and cost per item, and finds products that sell in volume but leave too little after product cost to pay for shipping, fees and ads. Use before putting ad budget behind a product, after supplier price increases, or when revenue grows and profit doesn't. Boundary: contribution-margin-leak adds up profit for the whole store or channel; this skill finds the individual products dragging it down.
---

# Low Margin SKU Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Revenue grows and profit doesn't.
- A supplier raised prices.
- Choosing which products to push with ads.

## Required input

- **Shopify Sales by product:** Shopify admin > **Analytics** > **Reports** >
  "Sales by product" (or by variant) > date range > export. Columns: product
  or variant, net quantity, net sales (after discounts and returns).
- **Shopify Products export** for costs: Shopify admin > **Products** >
  **Export** > CSV. Columns: Title, Variant SKU, Cost per item. If costs are
  not in Shopify, the owner supplies them per SKU.

## Live data (MarketAtoms MCP)

`store_snapshot` gives store totals only. Use the exports.

## Analysis workflow

1. Match each product or variant to its cost per item.
2. SKUs with fewer than `sku.min_units` units sold: not judged, listed.
3. Gross profit = net sales - units x cost per item. Gross margin = gross
   profit / net sales. This is before shipping, payment fees and ads.
4. Rank SKUs under the floor by units sold: the more they sell, the more the
   thin margin costs.
5. SKUs without a cost: `needs_data` for that SKU.

## Decision rules

- Gross margin < `sku.gross_margin_floor`: `low_margin`. Options for the
  owner: price, supplier cost, bundling, or not advertising it.
- Gross margin negative: `loss_making`, listed first.
- At or above the floor: `ok`.
- Under the unit minimum or no cost: `needs_data` for that SKU.
- Net sales are after discounts, so a SKU can be low-margin because it is
  always discounted; check discount-leak and markdown-depth-leak before
  blaming the cost.

## Output format

Summary line: SKUs judged, `low_margin` and `loss_making` counts, their units.

| SKU | Product | Units | Net sales | Cost per item | Gross profit | Gross margin | Verdict |
|---|---|---|---|---|---|---|---|

Then: **Not judged**, **Missing costs**, **Hand-off to contribution-margin-leak**,
**Approval needed**.

## Practical example

*Made-up numbers for illustration.* 90 days.

| SKU | Units | Net sales | Cost | Gross profit | Margin | Verdict |
|---|---|---|---|---|---|---|
| ODP-M | 450 | $13,050.00 | $17.60 | $5,130.00 | 39.3% | low_margin |
| ODP-L | 568 | $16,900.00 | $17.60 | $6,903.20 | 40.8% | ok |
| BW-6 | 451 | $3,800.00 | $4.10 | $1,950.90 | 51.3% | ok |

The two diaper sizes cost the same and list at the same price; size M sells at
a lower net price, so the gap is discounting, not cost.

## Guardrails

- Never change prices, costs or products.
- Gross margin is not profit; shipping, fees and ads come after it.
- Use the owner's costs; never estimate a product's cost.
