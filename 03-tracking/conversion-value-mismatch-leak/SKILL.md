---
name: conversion-value-mismatch-leak
description: Compares the value per purchase that Meta and Google report with the real average order value of the orders Shopify attributes to them, to catch purchase events that send tax, shipping, the wrong currency or a fixed value - which makes ROAS wrong even when the purchase count is right. Use when ROAS looks too good, after installing a new tracking app, or when every purchase shows the same value. Boundary: tracking-gap-leak checks the number of purchases; this skill checks the value attached to each one.
---

# Conversion Value Mismatch Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- ROAS looks higher (or lower) than the bank account suggests.
- A new pixel, server-side tracking or tracking app was installed.
- Every purchase in an ad platform shows the same value.

## Required input

- **Meta Ads Manager:** **Campaigns** > date range > **Export table data**
  with Purchases and Purchases conversion value. Note the attribution setting.
- **Google Ads:** **Campaigns** > **Download** with Conversions and Conv. value,
  for the purchase conversion action only.
- **Shopify, orders attributed to each channel:** Shopify admin >
  **Analytics** > **Reports** > "Sales attributed to marketing" (orders and
  sales by channel) for the same dates, plus whether Shopify's figure includes
  tax and shipping (Total) or not (net sales).
- The store currency and each ad account's currency.

## Live data (MarketAtoms MCP)

`meta_summary` gives Meta purchases and purchase value for a period;
`store_snapshot` gives store AOV. Channel-level Shopify AOV still needs the
Shopify report. Don't mix live and exported numbers for different dates.

## Analysis workflow

1. Per platform: purchases under `value.min_purchases`: `needs_data`.
2. Platform value per purchase = conversion value / purchases.
3. Shopify AOV for that channel = channel sales / channel orders, on the same
   basis (with or without tax and shipping) - say which.
4. Ratio = platform value per purchase / Shopify AOV.
5. If the platform export lets you see individual values (or the owner checks
   a few test orders), look for one value repeated on every purchase: a fixed
   value set in the event.
6. Currency: if the ad account currency differs from the store currency, say
   so before comparing.

## Decision rules

- |ratio - 1| >= `value.mismatch_flag`, platform higher: `value_inflated`.
  Most common causes: value includes tax and shipping while Shopify's figure
  doesn't, or a currency mismatch.
- Same, platform lower: `value_deflated` (value before discounts excluded,
  only the first line item sent, or a fixed low value).
- Within the flag: `consistent`.
- Under the purchase minimum: `needs_data`.
- ROAS adjusted for the mismatch = reported ROAS / ratio. Show it, marked as
  an estimate.

## Output format

Summary line: platforms checked, any mismatch, adjusted ROAS.

| Platform | Purchases | Value per purchase | Shopify AOV (same channel) | Ratio | Verdict | Reported ROAS | Adjusted ROAS |
|---|---|---|---|---|---|---|---|

Then: **Likely cause**, **How to confirm** (a test order checked in the
platform's event tool), **Approval needed** (tracking changes are the owner's).

## Practical example

*Made-up numbers for illustration.* 28 days.

- Meta: 150 purchases, $12,090 value, $80.60 per purchase. Shopify AOV for
  Meta-attributed orders (before tax and shipping) $65.00. Ratio 1.24:
  `value_inflated`. Reported ROAS 3.10 becomes about 2.50 (3.10 / 1.24).
- Google: 90 conversions, $5,940 value, $66.00 per purchase vs $64.00:
  ratio 1.03, `consistent`.

## Guardrails

- Never edit pixels, events, tags or tracking apps.
- Compare like with like: same dates, same tax and shipping basis, same currency.
- An adjusted ROAS is an estimate for decisions, not a corrected report.
