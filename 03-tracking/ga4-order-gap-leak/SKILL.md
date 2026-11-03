---
name: ga4-order-gap-leak
description: Compares the purchases Google Analytics 4 records with the orders Shopify recorded for the same days, to show whether GA4 misses sales (consent, ad blockers, checkout not tagged) or double counts them, before anyone uses GA4 for channel or funnel decisions. Use when GA4 and Shopify revenue disagree, after a theme or checkout change, or before using GA4 reports in a client report. Boundary: tracking-gap-leak compares ad platforms with Shopify; this skill compares GA4 with Shopify.
---

# GA4 Order Gap Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/tracking_gap.py`.

## Use this skill when

- GA4 revenue or purchases don't match Shopify.
- After a theme change, a checkout change or a new consent banner.
- Before using GA4 funnel or channel reports for decisions.

## Required input

- **GA4 purchases by date:** Google Analytics > **Reports** > **Monetization**
  > **Ecommerce purchases** (or an Exploration with the Transactions and
  Purchase revenue metrics) > same date range > share/download as CSV.
- **Shopify orders for the same dates:** Shopify admin > **Orders** >
  **Export** (or the Analytics "Sales over time" report). Exclude test and
  cancelled orders.
- GA4 property time zone and the Shopify store time zone; line the dates up
  first.

## Live data (MarketAtoms MCP)

`store_snapshot` gives the Shopify order count for the period. GA4 still needs
its report.

## Analysis workflow

1. Count Shopify orders and GA4 transactions for the same dates.
2. Run the shared gap rule:
   `python3 scripts/tracking_gap.py --channel GA4 <GA4 transactions> <Shopify orders>`.
   It uses `tracking.gap_flag` and `tracking.min_orders`.
3. If GA4 is lower: list likely causes from what the owner can check -
   consent mode or banner blocking analytics, checkout events not reaching GA4
   (Shopify's checkout runs separately from the theme, so a tag added only to
   the theme misses it), ad blockers.
4. If GA4 is higher: look for duplicate purchase events (the same transaction
   ID twice, for example from both a theme tag and an app).
5. Compare by day if the totals differ: a gap that starts on one date points to
   a change made that day.

## Decision rules

- |gap| > `tracking.gap_flag`: `reconcile`. GA4 channel and funnel reports are
  provisional until it is fixed; say "GA4 under-counts by about X%" (or
  over-counts).
- Within the flag: `trusted` for this period.
- Fewer than `tracking.min_orders` Shopify orders: `needs_data`.
- Shopify is the order record; GA4 is the measurement. The gap is always
  stated as GA4 against Shopify, never the other way round.

## Output format

Summary line: Shopify orders, GA4 transactions, gap, verdict.

| Source | Purchases | Gap vs Shopify | Direction | Verdict |
|---|---|---|---|---|

Then: **Day where the gap starts** (if any), **Likely causes to check**,
**Approval needed** (tag and consent changes are the owner's).

## Practical example

*Made-up numbers for illustration.* October 1-28: Shopify 1,000 orders, GA4
790 transactions. Gap -21.0%, under-tracking: `reconcile`. By day, GA4 matched
Shopify within 3% until October 9 and ran about 25% short afterwards; the
consent banner app was installed on October 9. GA4 funnel reports for October
are provisional.

## Guardrails

- Never edit GA4, Google Tag Manager, consent settings or the theme.
- Don't use GA4 revenue as the store's revenue; Shopify is the record.
- Line up time zones before comparing days.
