---
name: cross-sell-pair-leak
description: Finds pairs of products that customers already buy together far more often than chance - real bundle and cross-sell candidates taken from the store's own orders - and flags the ones not yet offered as a bundle or cart suggestion. Use when planning bundles, setting up "frequently bought together", or when average order value is flat. Boundary: basket-value-gap-leak covers the free-shipping gap and single-item share; this skill covers which products belong together.
---

# Cross-sell Pair Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/cross_sell_pairs.py`.

## Use this skill when

- Planning bundles or a "frequently bought together" block.
- Average order value is flat and single-product orders dominate.
- Choosing which product to suggest in the cart or post-purchase.

## Required input

- **Shopify Orders export:** Shopify admin > **Orders** > **Export** > date
  range (90 days or more is best) > CSV. One row per line item; the script
  groups them by order.
- **Existing bundles or cart suggestions** the store already runs, typed in as
  "Product A+Product B", so they aren't reported as new.

## Live data (MarketAtoms MCP)

`store_snapshot` gives totals only; pairs need line items. Use the export.

## Analysis workflow

1. Run the script:
   `python3 scripts/cross_sell_pairs.py --orders orders.csv --bundled "A+B"`.
2. It refuses to look for pairs below `pairs.min_orders` (`needs_data`).
3. For every pair bought together in at least `pairs.min_pair_orders` orders it
   computes lift = orders with both x all orders / (orders with A x orders with B).
   Lift 1 means "together as often as chance"; it reports pairs at or above
   `pairs.lift_flag`.
4. "Share of A orders" = orders with both / orders with A: how often a buyer
   of A also takes B today.
5. For each unbundled pair, suggest the cheapest test: cart suggestion first,
   bundle second.

## Decision rules

- Lift >= `pairs.lift_flag`, together >= `pairs.min_pair_orders`, not already
  bundled: `opportunity`.
- Same but already bundled: `already_served`, listed.
- No pair meets the rule: say so. Many stores have one hero product and no
  strong pair; that is a finding, not a failure.
- Under `pairs.min_orders`: `needs_data`.

## Output format

Summary line: orders, multi-product share, opportunities.

| Product A | Product B | Orders with both | Lift | Share of A orders | Already bundled | Verdict |
|---|---|---|---|---|---|---|

Then: **Suggested test per pair**, **Approval needed** (any bundle, price or
theme change is the owner's).

## Practical example

*Made-up numbers for illustration.* 2,000 orders in 90 days. Overnight Diaper
Pants M in 600 orders, Baby Wipes 6-pack in 400, both together in 210.
Lift = 210 x 2,000 / (600 x 400) = 1.75: `opportunity`. 35.0% of diaper buyers
already add wipes. Suggested test: wipes as the cart suggestion on the diaper
page for 14 days. Romper + Gift Box: 30 orders together, lift 1.33, under the
1.5 flag: not reported.

On the repository's own sample store the script finds no pair that meets the
rule, and says so.

## Guardrails

- Never create bundles, discounts or cart rules.
- Lift shows what customers do now, not what a bundle would sell.
- Don't suggest a bundle discount by default; a suggestion at full price is
  the first test.
