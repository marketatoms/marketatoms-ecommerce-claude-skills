---
name: utm-coverage-leak
description: Measures how many Shopify orders arrive with no traffic source (direct, unknown, no UTM) and finds the ads and links sending traffic without UTM parameters, so paid channels stop being under-credited in Shopify. Use when Shopify shows most sales as "direct", when Shopify and the ad platforms disagree on which channel sells, or before a channel budget review. Boundary: tracking-gap-leak compares the counts; this skill fixes the labels Shopify needs to count by channel.
---

# UTM Coverage Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Shopify reports a large share of sales as "direct" or "unknown".
- Shopify and Meta or Google disagree on which channel drives sales.
- Before judging channels from Shopify's own reports.

## Required input

- **Shopify attribution report:** Shopify admin > **Analytics** > **Reports**
  > "Sales attributed to marketing" (or "Sessions by referrer" / "Sales by
  referrer" if that is what your plan shows) > date range > export. Columns:
  channel or referrer, orders, sales.
- **Ad URLs** (optional, for the second half of the check): Meta Ads Manager >
  **Ads** > **Export table data** with the "Website URL" and "URL parameters"
  columns; Google Ads > **Ads** > download with "Final URL" and the account's
  tracking template or final URL suffix.
- Email and SMS links: the owner says whether the tool adds UTMs (most email
  tools can).

## Live data (MarketAtoms MCP)

`store_snapshot` gives order totals but not attribution. Use the Shopify report.

## Analysis workflow

1. Total orders in the report. If under `utm.min_orders`: `needs_data`.
2. Unattributed orders = orders labelled direct, unknown, none or "(not set)".
   Share = unattributed / total.
3. List paid channels' attributed orders next to the totals, so the owner
   sees what is credited.
4. From the ad exports, list every active ad whose URL has no `utm_source`
   parameter (and no tracking template doing the same job).
5. Add email/SMS if the owner says links carry no UTMs.

## Decision rules

- Share >= `utm.unattributed_share_flag`: `leak` - Shopify can't tell channels
  apart well enough for budget decisions.
- Any active paid ad without UTMs: `untagged_ads`, listed by spend.
- Share under the flag and no untagged ads: `ok`.
- Under the minimum orders: `needs_data`.
- Direct traffic is never zero; returning customers typing the address are
  real. The finding is about the share, not about direct existing.

## Output format

Summary line: total orders, unattributed share, untagged active ads.

| Channel / referrer | Orders | Share |
|---|---|---|

| Ad | Platform | Spend | URL has utm_source |
|---|---|---|---|

Then: **Suggested UTM pattern** (for example
`utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}`), **Approval
needed** (editing ads is the owner's job).

## Practical example

*Made-up numbers for illustration.* 28 days, 1,200 orders. Direct 312 and
unknown 96: 408 unattributed, 34.0%, over the 30% flag: `leak`. Meta export:
14 active ads, 5 with no URL parameters, together $2,140 of spend. Those ads'
sales land in "direct" in Shopify, which is one reason Shopify credits Meta
with fewer orders than Meta claims.

## Guardrails

- Never edit ads, URL parameters or tracking templates.
- Don't count an order as "Meta" or "Google" from guesswork; only Shopify's
  labels count here.
- A fix changes future orders only; past orders stay unattributed.
