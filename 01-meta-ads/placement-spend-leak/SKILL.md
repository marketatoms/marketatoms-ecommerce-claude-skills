---
name: placement-spend-leak
description: Breaks Meta spend down by placement (Facebook Feed, Instagram Reels, Audience Network and so on) and finds placements that take a real share of the budget but buy purchases at double the account's cost or more. Use when Advantage+ placements are on and cost per purchase is rising, or in a monthly Meta review. Boundary: wasted-ad-spend-leak finds ad sets with zero purchases; this skill compares the cost of purchases across placements.
---

# Placement Spend Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- "Where is Meta actually showing my ads, and is it worth it?"
- Automatic (Advantage+) placements are on and cost per purchase is drifting up.
- Monthly Meta review.

## Required input

- **Meta Ads Manager, placement breakdown:** Ads Manager > **Campaigns** (or
  **Ad sets**) > date range > **Breakdown** > **By delivery** > **Placement**
  > **Reports** > **Export table data** (CSV). Columns: Platform, Placement,
  Amount spent, Impressions, Link clicks, Purchases, Purchases conversion value.
- The attribution setting shown in the column header (for example "7-day click
  or 1-day view").
- The tracking-gap verdict for Meta, if it exists (AGENTS.md rule 1).

## Live data (MarketAtoms MCP)

`meta_summary` gives account totals for context. The placement breakdown still
needs the export.

## Analysis workflow

1. Account cost per purchase = total spend / total purchases for the period.
   If total purchases are under `placement.min_purchases`, stop: `needs_data`.
2. Per placement: spend share = placement spend / total spend; cost per
   purchase = spend / purchases.
3. Placements under `placement.min_spend_share` are listed but not judged.
4. For the rest: ratio = placement cost per purchase / account cost per
   purchase. Apply the decision rules.
5. Money at stake for an `expensive` placement = its spend - (its purchases x
   account cost per purchase): what those purchases cost above the account
   average.

## Decision rules

- Spend share >= `placement.min_spend_share` and ratio >=
  `placement.cpa_ratio_flag`: `expensive`. Suggest testing the campaign with
  that placement excluded, as an A/B test, not a switch-off.
- Spend share >= the minimum and zero purchases: refer to
  wasted-ad-spend-leak (same bar, `ads.wasted_cpa_multiple`).
- Ratio under the flag: `ok`.
- Below the spend-share minimum: `not_judged`, listed for completeness.
- Account purchases under `placement.min_purchases`: `needs_data`.
- Meta tracking `reconcile`: all verdicts become provisional and say so.

## Output format

Summary line: account cost per purchase, placements judged, spend on
`expensive` placements and the money at stake.

| Platform | Placement | Spend | Share | Purchases | Cost/purchase | x account | Verdict |
|---|---|---|---|---|---|---|---|

Then: **Not judged (small share)**, **Caveats** (attribution setting, tracking),
**Approval needed**.

## Practical example

*Made-up numbers for illustration.* 28 days, $6,000 spend, 200 purchases:
account cost per purchase $30.00.

| Placement | Spend | Share | Purchases | Cost/purchase | x account | Verdict |
|---|---|---|---|---|---|---|
| Facebook Feed | $2,700 | 45.0% | 107 | $25.23 | 0.84 | ok |
| Instagram Feed | $1,500 | 25.0% | 55 | $27.27 | 0.91 | ok |
| Instagram Reels | $1,050 | 17.5% | 30 | $35.00 | 1.17 | ok |
| Audience Network | $720 | 12.0% | 8 | $90.00 | 3.00 | expensive |
| Messenger | $30 | 0.5% | 0 | - | - | not_judged |

Audience Network: 8 purchases that would cost $240 at the account average cost
$720, so $480 at stake. Suggested test: duplicate the campaign without
Audience Network for 14 days.

## Guardrails

- Never change placements or edit a campaign. Recommend a test; the owner runs it.
- Placement purchases depend on Meta's attribution; say which setting the
  export used.
- Don't judge a placement on a handful of purchases; respect the minimums.
