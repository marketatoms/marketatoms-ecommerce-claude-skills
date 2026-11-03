---
name: product-disapproval-leak
description: Lists products Google Merchant Center has disapproved or limited, ranks them by the Shopify revenue they normally bring, and says whether disapprovals are isolated or a feed-wide problem. Use after a Merchant Center warning email, when Shopping sales drop suddenly, or in a monthly feed check. Boundary: feed-zero-impressions-leak covers approved products that get no impressions; this skill covers products Google won't show at all.
---

# Product Disapproval Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Merchant Center sent a warning or a product count dropped.
- Shopping sales fell suddenly without a budget change.
- Monthly feed health check.

## Required input

- **Merchant Center product list with status:** Google Merchant Center >
  **Products** > filter or sort by status (for example "Not approved" /
  "Limited" / "Approved") > **Download** (CSV). Columns: Item ID, Title,
  Status, Issue (the reason Merchant Center shows).
- **Shopify Sales by product** for the last `disapproval.lookback_days`:
  Shopify admin > **Analytics** > **Reports** > "Sales by product" > export.
  Columns: product title, net sales.

## Live data (MarketAtoms MCP)

No live Google tool yet. `store_snapshot` gives store totals only; product
sales still need the Shopify report.

## Analysis workflow

1. Count submitted items and items per status. Disapproval share =
   disapproved / submitted.
2. Match each disapproved or limited item to its Shopify product title and
   take its net sales over `disapproval.lookback_days`.
3. Rank by those sales: that is revenue the product earned when it could be
   shown, now at risk.
4. Group by issue text. One issue on many items usually means one feed fix
   (an attribute, an image rule, a policy setting), not many product fixes.

## Decision rules

- Share >= `disapproval.share_flag`: `feed_problem`. Lead with the most common
  issue.
- Disapproved item with Shopify sales in the lookback: `revenue_at_risk`,
  ranked by sales.
- Disapproved item with no sales: `low_priority`.
- "Limited" items are reported separately: they still show, but not
  everywhere.
- If the product list has no Status column: `needs_data` - ask for the
  Merchant Center download, don't infer status from impressions.

## Output format

Summary line: submitted, disapproved (share), limited, Shopify sales at risk.

| Item ID | Title | Status | Issue | Shopify net sales (90 days) | Verdict |
|---|---|---|---|---|---|

Then: **Issues by count**, **Limited items**, **Approval needed** (feed edits
are the owner's).

## Practical example

*Made-up numbers for illustration.* 240 items submitted, 18 disapproved
(7.5%, flag 5%): `feed_problem`. 14 of the 18 share one issue, "Image too
small", so one image fix in the theme or feed app clears most of them.
Top revenue at risk: "Night Light" ($3,420 net sales in 90 days) and
"Sleep Sack" ($2,180). Together $5,600 of sales that Shopping can't currently
reach.

## Guardrails

- Never edit products, the feed or Merchant Center settings, and never
  request a review on the owner's behalf.
- Quote Merchant Center's issue text as given; don't invent policy reasons.
- Shopify sales show what is at risk, not what Google would have sold.
