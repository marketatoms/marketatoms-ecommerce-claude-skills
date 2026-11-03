---
name: branded-search-share-leak
description: Splits Google Ads conversions and ROAS into brand-name searches and everything else, to show how much of Google's reported performance comes from people who were already looking for the store. Use when Google ROAS looks strong but new customers don't grow, before raising Google budgets, or when comparing Google with Meta. Boundary: tracking-gap-leak checks whether the counts are right; this skill checks what the counts are made of.
---

# Branded Search Share Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- "Google says ROAS 5, but it doesn't feel like Google brings new customers."
- Before shifting budget from Meta to Google, or raising Google spend.
- Planning whether to keep bidding on the store's own name.

## Required input

- **Google Ads Search terms report:** Google Ads > **Insights and reports** >
  **Search terms** > date range > **Download** > CSV. Columns: Search term,
  Campaign, Cost, Conversions, Conv. value.
- **Brand terms:** the store name and its common misspellings, typed in by
  the owner.
- Performance Max and Shopping campaigns show only part of their search terms;
  if their spend is large, say that the split covers Search campaigns fully
  and the rest partly.

## Live data (MarketAtoms MCP)

No live Google tool yet. Use the export.

## Analysis workflow

1. Mark each search term as brand if it contains a brand term (case-insensitive).
2. Total cost, conversions and conversion value for brand and non-brand.
3. If total conversions are under `brand.min_conversions`: `needs_data`.
4. Brand share = brand conversions / all conversions.
5. Show three ROAS figures: blended, brand only, non-brand only.

## Decision rules

- Brand share >= `brand.conversion_share_flag`: `brand_heavy` - blended Google
  ROAS mostly reflects demand the store already had. Report non-brand ROAS as
  the figure to judge Google on.
- Under the flag: `ok`, still report the split.
- Under the minimum conversions: `needs_data`.
- Never conclude "stop brand bidding": competitors may bid on the name. That is
  a test for the owner (for example pause brand in one region for two weeks
  and compare Shopify orders).

## Output format

Summary line: brand share of conversions, blended vs non-brand ROAS.

| Segment | Cost | Conversions | Conv. value | ROAS | Share of conversions |
|---|---|---|---|---|---|

Then: **Coverage note** (search terms hidden in Performance Max/Shopping),
**Suggested test**, **Approval needed**.

## Practical example

*Made-up numbers for illustration.* 28 days, 180 conversions.

| Segment | Cost | Conversions | Conv. value | ROAS | Share |
|---|---|---|---|---|---|
| Brand | $600 | 117 | $17,550 | 29.25 | 65.0% |
| Non-brand | $4,800 | 63 | $9,450 | 1.97 | 35.0% |
| Blended | $5,400 | 180 | $27,000 | 5.00 | 100% |

Brand share 65.0%, over the 50% flag: `brand_heavy`. Google's 5.00 ROAS rests
on brand searches; new-demand Google spend returns 1.97.

## Guardrails

- Never pause or change campaigns or keywords.
- The owner defines the brand terms; don't guess them from campaign names.
- Brand conversions are not worthless; the question is how much of them would
  happen anyway, which only a test can answer.
