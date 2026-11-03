---
name: lapsed-customer-leak
description: Counts repeat customers who have stopped buying - their last order is well past the store's own normal reorder gap - and what they spent before they went quiet, to size a win-back flow or campaign. Use when repeat revenue is falling, before planning a win-back email, or in a quarterly retention review. Boundary: second-order-gap-leak covers first-time buyers who never return; this skill covers proven repeat buyers who stopped.
---

# Lapsed Customer Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/lapsed_customers.py`.

## Use this skill when

- Repeat revenue is shrinking.
- Planning a win-back flow or campaign: how many people, how valuable?
- Quarterly retention review.

## Required input

- **Shopify Orders export** covering as much history as possible (12 months
  or more is best): Shopify admin > **Orders** > **Export** > CSV. Customers
  are identified by email; orders without an email are skipped.

## Live data (MarketAtoms MCP)

`store_snapshot` gives totals, not customer histories. Use the export.

## Analysis workflow

1. Run the script:
   `python3 scripts/lapsed_customers.py --orders orders.csv`.
2. It finds repeat customers (2+ orders) and the median days between their
   first and second order.
3. Lapse point = `lapse.gap_multiple` x that median. If there are fewer than
   `lapse.min_repeat_customers` repeat customers, it uses `lapse.default_days`
   and says so.
4. A repeat customer is lapsed if their last order is older than the lapse
   point, counted back from the last order date in the export.
5. Lapsed share = lapsed / repeat customers. It also sums what lapsed
   customers spent before, as a measure of their past value (not a forecast).

## Decision rules

- Lapsed share >= `lapse.repeat_share_flag`: `leak` - a win-back flow is worth
  building or fixing (see email-flow-coverage-leak).
- Under the flag: `ok`.
- Fewer than `lapse.min_repeat_customers` repeat customers: `needs_data`.
- A very long export makes more people look lapsed simply because it reaches
  further back; say how many months the export covers.

## Output format

Summary line: repeat customers, median reorder gap, lapse point, lapsed share,
verdict.

| Measure | Value |
|---|---|
| Repeat customers (2+ orders) | |
| Median days first -> second order | |
| Lapse point (days) | |
| Lapsed repeat customers | |
| Lapsed share (flag) | |
| What they spent before | |

Then: **Win-back suggestion** (timing from the lapse point), **Approval needed**.

## Practical example

*Made-up numbers for illustration* (the repository's sample store,
`examples/sample-orders-export.csv`, April to October 2026): 1,305 customers,
211 with 2+ orders. Median gap first to second order 43 days, so the lapse
point is 2 x 43 = 86 days. 106 repeat customers haven't ordered for longer:
50.2%, over the 30% flag: `leak`. Before going quiet they spent $9,251.95.
A win-back email around day 60-86 after the last order would reach them
before they cross the lapse point.

## Guardrails

- Never send email, create segments in the email tool, or export customer
  lists for other uses.
- Past spend is history, not a forecast of what a win-back will recover.
- Don't list individual customers' emails in the output; counts only.
