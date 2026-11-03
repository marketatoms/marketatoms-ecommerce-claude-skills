---
name: feed-zero-impressions-leak
description: Finds products that are approved and in stock in Google Merchant Center but got zero Shopping impressions for two weeks - products the store pays to list but Google never shows - and says whether it is a few products or the whole feed. Use when Shopping traffic is concentrated on a few products, after adding new products, or in a monthly Google review. Boundary: product-disapproval-leak covers products Google refuses; this skill covers approved products Google ignores.
---

# Feed Zero Impressions Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/feed_zero_impressions.py`.

## Use this skill when

- "Half my catalogue never shows up on Google Shopping."
- New products were added weeks ago and still have no traffic.
- Monthly Google Shopping review.

## Required input

- **Google Ads Products report** covering at least `feed.zero_impression_days`:
  Google Ads > **Campaigns** > **Products** (Shopping and Performance Max) >
  date range > **Download** > CSV. Columns: Item ID, Product title, Impr.,
  Clicks, Cost.
- **Status and availability** per item from Google Merchant Center >
  **Products** (download the product list), joined on Item ID if the Google
  Ads report doesn't include them. Without status, the skill treats every row
  as eligible and says so.
- How many days the report covers.

## Live data (MarketAtoms MCP)

No live Google tool yet. Use the exports.

## Analysis workflow

1. Run the script:
   `python3 scripts/feed_zero_impressions.py --products products.csv --days 14`.
   It refuses reports shorter than `feed.zero_impression_days` (`needs_data`).
2. It keeps only approved, in-stock items (disapproved items belong to
   product-disapproval-leak; out-of-stock items are expected to get no
   impressions).
3. It lists items with zero impressions and, if there are at least
   `feed.min_products` eligible items, the share of the feed they make up.
4. For each invisible item, look in the report and Merchant Center for the
   likely reason, from data only: not in any campaign's listing group,
   excluded by a product filter, price far above similar items, very new item,
   or a weak title (missing product type, size or brand).

## Decision rules

- Share >= `feed.zero_share_flag`: `feed_problem` - look at campaign structure
  (listing groups, product filters, budget limited) before single products.
- Invisible items but share under the flag: `products` - fix item by item,
  starting with best sellers in Shopify.
- Fewer than `feed.min_products` eligible items: list the items, don't judge
  the feed.
- Report shorter than `feed.zero_impression_days`: `needs_data`.
- No invisible items: say so. No finding is a good finding.

## Output format

Summary line: eligible items, invisible items, share, verdict.

| Item ID | Title | Impressions | Shopify sales last 90 days | Likely reason |
|---|---|---|---|---|

Then: **Excluded from this check** (disapproved, out of stock), **Approval
needed** (any feed or campaign change).

## Practical example

*Made-up numbers for illustration* (the repository's sample feed,
`examples/sample-google-products.csv`): 24 products in a 14-day report;
2 disapproved and 2 out of stock are excluded; 20 eligible. 5 have zero
impressions: 25.0%, at or above the 20% flag: `feed_problem`. The report alone
can't say why, so the next step is to check whether those five items sit in a
listing group or product filter that any campaign actually serves, before
looking at titles or prices.

## Guardrails

- Never edit the feed, Merchant Center, listing groups or campaigns.
- Never call a product invisible on a report shorter than the window.
- Don't blame Google for out-of-stock or disapproved items; they are excluded
  here on purpose.
