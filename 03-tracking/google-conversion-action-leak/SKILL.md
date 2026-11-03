---
name: google-conversion-action-leak
description: Audits the Google Ads conversion actions that bidding optimises towards - two purchase actions both set as primary (double counting), a non-purchase action such as add-to-cart set as primary, or a purchase action counting one per click - and checks the result against Shopify's Google orders. Use when Google conversions look higher than Shopify's Google sales, after connecting GA4 or a Shopify app to Google Ads, or before trusting Smart Bidding. Boundary: tracking-gap-leak measures the gap; this skill finds the setting that causes it.
---

# Google Conversion Action Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/tracking_gap.py`.

## Use this skill when

- Google reports noticeably more purchases than Shopify attributes to Google.
- GA4, the Google & YouTube Shopify app or a tracking app was connected to
  Google Ads recently.
- Before trusting automated bidding with a target ROAS or CPA.

## Required input

- **Google Ads conversion actions:** Google Ads > **Goals** > **Conversions**
  > **Summary** > download the table. Columns: Conversion action, Action
  optimization (Primary / Secondary), Source, Count (Every / One), Category,
  Conversions, All conv.
- **Shopify orders attributed to Google** for the same dates: Shopify admin >
  **Analytics** > **Reports** > "Sales attributed to marketing".
- Whether campaigns bid towards purchases (target ROAS / target CPA /
  maximise conversion value).

## Live data (MarketAtoms MCP)

No live Google tool yet. Use the exports.

## Analysis workflow

1. List purchase-category actions and their optimisation setting.
2. Count primary purchase actions. Two or more primary purchase actions from
   different sources (for example a Google tag and a GA4 import) usually count
   the same order twice.
3. List any non-purchase action (page view, add to cart, begin checkout) set to
   Primary while campaigns bid towards purchases.
4. Note any purchase action with Count = One: repeat orders by the same click
   are dropped.
5. Cross-check: Google conversions (primary only) vs Shopify Google orders with
   `python3 scripts/tracking_gap.py --channel Google <Google conversions> <Shopify Google orders>`
   (rule: `tracking.gap_flag`, minimum `tracking.min_orders`).

## Decision rules

- Two or more primary purchase actions **and** the cross-check shows
  over-claiming beyond `tracking.gap_flag`: `double_counting`.
- Two primary purchase actions but the cross-check is within the flag:
  `review` - one action may not be firing; check both.
- Non-purchase action primary in purchase-bidding campaigns: `wrong_goal`.
- Purchase action counting One: `undercount_repeat`.
- Shopify Google orders under `tracking.min_orders`: settings findings still
  stand, the cross-check is `needs_data`.
- None of the above: `ok`.

## Output format

Summary line: primary purchase actions, findings, cross-check gap.

| Conversion action | Source | Category | Optimization | Count | Conversions | Finding |
|---|---|---|---|---|---|---|

Then: **Cross-check with Shopify**, **What to change (for the owner)**,
**Approval needed**.

## Practical example

*Made-up numbers for illustration.* 28 days. Primary purchase actions:
"Purchase (Google tag)" 142 and "Shopify - purchase (GA4 import)" 138, so the
Conversions column shows 280. Shopify attributes 140 orders to Google. Gap
+100.0%, over-claiming: `double_counting`. Every Google conversion figure,
and the bidding built on it, counts most orders twice. Fix for the owner: keep
one purchase action as Primary, set the other to Secondary.

## Guardrails

- Never change conversion actions, goals or bidding.
- Primary vs Secondary affects bidding; recommending which to keep is advice,
  the switch is the owner's.
- Don't judge "All conv." as purchases; it includes secondary actions.
