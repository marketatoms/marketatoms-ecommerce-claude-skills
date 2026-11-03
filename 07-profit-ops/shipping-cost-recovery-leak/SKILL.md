---
name: shipping-cost-recovery-leak
description: Compares what customers paid for shipping with what the store paid for shipping labels, to show how much of every shipping bill the store absorbs and what that costs as a share of revenue. Use when free-shipping offers grew, after carrier rate increases, or when margin is thin and nobody has looked at shipping. Boundary: basket-value-gap-leak looks at the free-shipping threshold from the customer's side; this skill looks at the shipping bill from the store's side.
---

# Shipping Cost Recovery Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Free shipping was extended, or the threshold lowered.
- Carrier rates went up.
- Margin is thin and shipping has never been checked.

## Required input

- **Shopify Orders export** for the period: Shopify admin > **Orders** >
  **Export** > CSV. The `Shipping` column is what customers paid; `Total` is
  revenue.
- **Shipping labels paid** for the same orders or dates, from one of:
  Shopify Shipping label charges (Shopify admin > **Settings** > **Billing**),
  the shipping app's export (for example ShipStation or Sendcloud), or the
  carrier invoice. A total for the period is enough; per-order costs are better.
- Whether label costs include returns labels; separate them if possible.

## Live data (MarketAtoms MCP)

`store_snapshot` gives orders and revenue for the period; label costs still
need the shipping export.

## Analysis workflow

1. Shipped orders in the period (exclude pickup and digital). Under
   `shipping.min_orders`: `needs_data`.
2. Shipping charged = sum of `Shipping` on those orders.
3. Labels paid = sum of label costs for the same orders or dates.
4. Recovery = charged / paid. Net shipping cost = paid - charged.
5. Net shipping cost share = net shipping cost / revenue.
6. If per-order costs exist: split free-shipping orders from paid-shipping
   orders and show the average label cost of each.

## Decision rules

- Recovery < `shipping.recovery_floor`: `under_recovered`.
- Net shipping cost share >= `shipping.cost_share_flag`: `margin_drain` -
  feeds straight into contribution-margin-leak's shipping line.
- Both fine: `ok`.
- Under the order minimum, or no label costs supplied: `needs_data`.
- Free shipping is a pricing choice, not a mistake; the finding is its cost,
  stated plainly, for the owner to weigh.

## Output format

Summary line: shipped orders, recovery, net shipping cost and share of revenue.

| Measure | Value | Flag | Verdict |
|---|---|---|---|

Then: **Free vs paid shipping orders** (if per-order costs exist), **Hand-off
to contribution-margin-leak**, **Approval needed**.

## Practical example

*Made-up numbers for illustration.* 28 days, 1,000 shipped orders, revenue
$62,000. Customers paid $3,600 for shipping; labels cost $8,400. Recovery
0.43, under the 0.5 floor: `under_recovered`. Net shipping cost $4,800 = 7.7%
of revenue, under the 10% flag. The store pays for 57% of every shipping bill.

## Guardrails

- Never change shipping rates, zones, thresholds or carriers.
- Use label costs the owner supplies; never estimate carrier rates.
- Keep returns labels separate; they belong with refund-and-return-leak.
