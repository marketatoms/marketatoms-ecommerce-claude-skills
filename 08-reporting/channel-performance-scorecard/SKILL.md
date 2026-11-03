---
name: channel-performance-scorecard
description: One table comparing paid channels (Meta, Google, TikTok and others) on the same footing - spend, Shopify-attributed orders and revenue, cost per order and ROAS from Shopify's numbers, each platform's own claim beside it, and whether its tracking can be trusted - plus the store's blended marketing efficiency. Use for a monthly channel review, before moving budget between channels, or for a client report. Boundary: it scores channels on agreed numbers; tracking-gap-leak and wasted-ad-spend-leak investigate the problems it surfaces.
---

# Channel Performance Scorecard

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/tracking_gap.py`.

## Use this skill when

- Monthly channel review.
- Before moving budget from one channel to another.
- A client or founder asks "which channel works?"

## Required input

- **Spend and platform-reported purchases per channel** for the period:
  Meta Ads Manager (**Campaigns** > **Export table data**: Amount spent,
  Purchases, Purchases conversion value), Google Ads (**Campaigns** >
  **Download**: Cost, Conversions, Conv. value), and the same from any other
  ad platform.
- **Shopify orders and sales attributed to each channel:** Shopify admin >
  **Analytics** > **Reports** > "Sales attributed to marketing".
- **Store total revenue** for the period.
- Target cost per order, if the store has one.

## Live data (MarketAtoms MCP)

If connected, `meta_summary` gives Meta spend and purchases and
`store_snapshot` the store revenue. Google, other platforms and Shopify
channel attribution still need exports. Same dates for every number.

## Analysis workflow

1. Per channel, from Shopify's numbers: cost per order = spend / Shopify
   orders; ROAS = Shopify-attributed revenue / spend.
2. Beside it, the platform's own purchases and ROAS.
3. Tracking verdict per channel with the shared rule:
   `python3 scripts/tracking_gap.py --channel Meta <reported> <shopify> ...`
   (`tracking.gap_flag`, minimum `tracking.min_orders`).
4. Blended marketing efficiency (MER) = store revenue / total ad spend.
5. Compare each channel's cost per order with the target, if given.

## Decision rules

- Tracking `reconcile`: the channel's row is marked provisional (AGENTS.md
  rule 1); no budget conclusion from it.
- Fewer than `tracking.min_orders` Shopify orders: `needs_data` for that
  channel; show spend only.
- Cost per order above target: `over_target`; at or under: `on_target`. No
  target: report the figures without a verdict.
- The scorecard ranks nothing by platform-reported ROAS; Shopify's numbers
  lead, the platform's claim is context.

## Output format

Summary line: total spend, store revenue, MER, channels provisional.

| Channel | Spend | Shopify orders | Shopify revenue | Cost/order | ROAS (Shopify) | Platform purchases | Tracking | Verdict |
|---|---|---|---|---|---|---|---|---|

Then: **Provisional rows**, **Hand-offs** (which check to run for each problem),
**Approval needed** (budget moves are the owner's).

## Practical example

*Made-up numbers for illustration.* October, target cost per order $30. Store
revenue $62,000, ad spend $12,600: MER 4.92.

| Channel | Spend | Shopify orders | Shopify revenue | Cost/order | ROAS | Platform purchases | Tracking | Verdict |
|---|---|---|---|---|---|---|---|---|
| Meta | $6,000 | 236 | $15,340 | $25.42 | 2.56 | 200 | reconcile (-15.3%) | on_target, provisional |
| Google | $5,400 | 172 | $11,180 | $31.40 | 2.07 | 180 | trusted (+4.7%) | over_target |
| TikTok | $1,200 | 22 | $1,050 | - | - | 31 | needs_data | needs_data |

## Guardrails

- Never move budget or change campaigns.
- Shopify attribution under-credits channels when UTMs are missing; check
  utm-coverage-leak before reading small differences.
- Same dates and time zone for every number on the card.
