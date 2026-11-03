---
name: shopping-product-roas-leak
description: Finds products in Google Shopping or Performance Max that spend real money but return less than half the store's target ROAS, and the spend that brought in too little. Use when Shopping ROAS is below target but some products clearly sell, before raising a Shopping budget, or in a monthly Google review. Boundary: wasted-ad-spend-leak covers spend with zero conversions; this skill covers products that convert, but too expensively.
---

# Shopping Product ROAS Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Shopping ROAS is under target overall.
- Before raising a Shopping or Performance Max budget.
- Deciding which products to split into their own campaign or exclude.

## Required input

- **Google Ads Products report:** Google Ads > **Campaigns** > **Products** >
  date range (28 days or more) > **Download** > CSV. Columns: Item ID, Product
  title, Cost, Conversions, Conv. value.
- **Target ROAS** (conversion value / cost) the store is working to. If there
  is none, ask; this check has no meaning without one.
- Which conversion action is counted (see google-conversion-action-leak) and
  the Google tracking-gap verdict, if they exist.

## Live data (MarketAtoms MCP)

No live Google tool yet. Use the export.

## Analysis workflow

1. Per product: ROAS = conv. value / cost.
2. Products with cost under `shopping.min_product_cost`: not judged, listed.
3. Products with cost at or above it and zero conversions: refer to
   wasted-ad-spend-leak.
4. The rest: ratio = product ROAS / target ROAS. Apply the decision rules.
5. Money at stake per `drag` product = cost - conv. value / target ROAS: the
   spend that went beyond what its value justified at target.

## Decision rules

- Ratio < `shopping.roas_ratio_floor`: `drag`. Suggest a lower product-level
  target, a separate campaign, or exclusion as options for the owner.
- Ratio between the floor and 1: `below_target`, listed.
- Ratio >= 1: `ok`.
- No target ROAS given: `needs_data`.
- If Google tracking is `reconcile` or the counted conversion action is wrong,
  all verdicts are provisional and say why.

## Output format

Summary line: target ROAS, products judged, `drag` products, money at stake.

| Item ID | Product | Cost | Conversions | Conv. value | ROAS | x target | Verdict | At stake |
|---|---|---|---|---|---|---|---|---|

Then: **Zero conversions** (hand-off to wasted-ad-spend-leak), **Not judged**,
**Approval needed**.

## Practical example

*Made-up numbers for illustration.* Target ROAS 4.0, last 28 days.

| Product | Cost | Conv. value | ROAS | x target | Verdict | At stake |
|---|---|---|---|---|---|---|
| Bamboo Sleep Set | $820 | $4,510 | 5.50 | 1.38 | ok | - |
| Gift Box Set | $640 | $1,152 | 1.80 | 0.45 | drag | $352 |
| Changing Mat | $310 | $0 | 0 | - | to wasted-ad-spend-leak | - |
| Teething Ring | $38 | $96 | - | - | not judged (cost under 50) | - |

Gift Box Set: $640 - $1,152 / 4.0 = $352 spent beyond what its sales justified
at target.

## Guardrails

- Never change bids, targets, listing groups or exclusions.
- ROAS here is platform conversion value; it is before refunds and margin. For
  profit, hand off to contribution-margin-leak.
- No target, no verdict.
