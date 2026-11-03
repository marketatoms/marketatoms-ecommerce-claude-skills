---
name: price-competitiveness-leak
description: Uses Google Merchant Center's price competitiveness report to find products priced well above what other sellers charge for the same item, ranked by the Shopping clicks they get, so the owner can see where price may be costing conversions. Use when Shopping clicks don't convert, before a pricing review, or when a competitor undercuts. Boundary: price-change-leak judges the store's own price changes over time; this skill compares the store's price with the market today.
---

# Price Competitiveness Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Shopping products get clicks but few sales.
- Before a pricing review.
- "Am I more expensive than everyone else on Google?"

## Required input

- **Merchant Center price competitiveness report:** Google Merchant Center >
  the **price competitiveness** report (under Performance or Analytics,
  depending on the Merchant Center version) > **Download**. Columns: Item ID or
  title, your price, benchmark price. Only products that other sellers also
  list have a benchmark.
- **Google Ads Products report** for the same period (Clicks, Cost,
  Conversions) to rank by traffic.

## Live data (MarketAtoms MCP)

No live Google tool yet. Use the exports.

## Analysis workflow

1. Per product with a benchmark: gap = (your price - benchmark price) /
   benchmark price.
2. Join Shopping clicks and conversions by Item ID.
3. Products with fewer than `benchmark.min_clicks`: listed, not ranked.
4. Rank products with gap >= `benchmark.price_gap_flag` by clicks: clicks are
   shoppers who saw the price next to others and may have left.
5. Compare their Shopping conversion rate with products priced at or under
   the benchmark, if both groups have enough clicks; otherwise don't compare.

## Decision rules

- Gap >= `benchmark.price_gap_flag` and clicks >= `benchmark.min_clicks`:
  `above_market`. Present the options (match, bundle to change the
  comparison, accept and exclude from Shopping) as decisions for the owner.
- Gap under the flag: `in_market`.
- No benchmark for a product: not covered; say how many.
- No price competitiveness report available: `needs_data`.

## Output format

Summary line: products with a benchmark, `above_market` count, their clicks.

| Item | Your price | Benchmark | Gap | Clicks | Conversions | Verdict |
|---|---|---|---|---|---|---|

Then: **Listed, not ranked** (few clicks), **No benchmark**, **Approval needed**.

## Practical example

*Made-up numbers for illustration.* 28 days.

| Item | Your price | Benchmark | Gap | Clicks | Verdict |
|---|---|---|---|---|---|
| Bamboo Sleep Set | $70.00 | $59.90 | +16.9% | 210 | above_market |
| Organic Cotton Romper | $28.00 | $27.50 | +1.8% | 340 | in_market |
| Gift Box Set | $44.00 | $36.00 | +22.2% | 31 | listed, not ranked |

The sleep set is 16.9% above the benchmark on 210 clicks: the price is worth a
decision. The gift box gap is larger, but 31 clicks are too few to rank.

## Guardrails

- Never change a price. This skill reports the gap; pricing is the owner's call.
- The benchmark is Google's figure for other sellers' prices; it is not a cost
  floor or a recommendation.
- Products without a benchmark are not "competitive"; they are unmeasured.
