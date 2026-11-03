---
name: markdown-depth-leak
description: Measures how much of the store's product revenue is sold with a compare-at ("was") price and how deep those markdowns go, to show when the sale price has quietly become the real price. Use when most products show a strike-through price, before a sale event, or when margin is thin despite few discount codes. Boundary: discount-leak covers checkout discount codes; this skill covers permanent markdowns set on the product.
---

# Markdown Depth Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Most products show a crossed-out price.
- Margin is thin even though few discount codes are used.
- Before planning a sale: is anything still at full price?

## Required input

- **Shopify Products export:** Shopify admin > **Products** > **Export** >
  CSV. Columns: Title, Variant SKU, Variant Price, Variant Compare At Price,
  Status.
- **Shopify Sales by product** for the period: Shopify admin > **Analytics** >
  **Reports** > "Sales by product" > export. Columns: product title, net sales.
- The period's dates. The Products export shows prices **today**; if compare-at
  prices changed during the period, say the result is approximate.

## Live data (MarketAtoms MCP)

No live tool reads product prices yet. Use the exports.

## Analysis workflow

1. Active products only. Under `markdown.min_products`: `needs_data`.
2. A product is marked down if Compare At Price is set and higher than Price.
3. Markdown revenue share = net sales of marked-down products / net sales of
   all products.
4. Depth per product = (compare-at - price) / compare-at. Report the simple
   average across marked-down products, and the deepest ones.
5. List products that have had a compare-at price for the whole period and
   sell mainly at that price: for those, the "sale" is the normal price.

## Decision rules

- Markdown revenue share >= `markdown.revenue_share_flag`: `permanent_sale` -
  full price is no longer the normal price for most of the revenue.
- Average depth >= `markdown.depth_flag`: `deep_markdowns`.
- Both: report both; they compound.
- Neither: `ok`.
- Fewer than `markdown.min_products` active products: `needs_data`.
- Compare-at prices are also a consumer-law matter in many countries (a "was"
  price must have been genuine). Mention it as a question for the owner, not a
  legal verdict.

## Output format

Summary line: active products, marked down, revenue share, average depth.

| Product | Price | Compare-at | Depth | Net sales | Share of product revenue |
|---|---|---|---|---|---|

Then: **Deepest markdowns**, **Questions for the owner**, **Approval needed**.

## Practical example

*Made-up numbers for illustration.* 40 active products, 22 with a compare-at
price. Net product sales $48,000, of which $31,200 from marked-down products:
65.0%, over the 50% flag: `permanent_sale`. Average depth 28.0%, under the 30%
flag. The Organic Cotton Romper ($28, was $35, depth 20.0%) has shown that
"was" price all period.

## Guardrails

- Never change a price or compare-at price.
- Don't give legal advice; raise the reference-price question and stop there.
- The Products export is a snapshot of today; say so when the period is long.
