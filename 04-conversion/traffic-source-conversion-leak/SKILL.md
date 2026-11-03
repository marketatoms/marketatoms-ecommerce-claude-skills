---
name: traffic-source-conversion-leak
description: Compares the conversion rate of each traffic source (Meta, Google, TikTok, email, organic and others) with the store's own conversion rate, and finds sources whose visitors rarely buy - often a landing page or audience mismatch rather than a site problem. Use when traffic grows but orders don't, when a new channel is being tested, or before scaling paid traffic. Boundary: mobile-conversion-gap-leak compares devices and checkout-drop-leak compares funnel steps; this skill compares where visitors come from.
---

# Traffic Source Conversion Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Sessions are up but orders aren't.
- A new paid channel (TikTok, Pinterest) is being tested.
- Before scaling a source: do its visitors actually buy?

## Required input

- **Shopify sessions and conversion by source:** Shopify admin >
  **Analytics** > **Reports** > the sessions report by referrer or by UTM
  source with conversion (search for "sessions by referrer" or "conversion
  rate") > date range > export. Columns: source or referrer, sessions,
  sessions converted (or orders).
- Store total sessions and orders for the same period.
- The UTM coverage verdict if it exists: if many paid sessions land in
  "direct", source rates are blurred (see utm-coverage-leak).

## Live data (MarketAtoms MCP)

`store_snapshot` gives store orders; sessions by source still need the
Shopify report.

## Analysis workflow

1. Store CVR = store orders / store sessions.
2. Per source: CVR = orders / sessions. Sources under `source.min_sessions`
   are listed, not judged.
3. Ratio = source CVR / store CVR.
4. For sources under `source.cvr_ratio_floor`: orders short of the floor =
   sessions x (store CVR x `source.cvr_ratio_floor`) - orders. This is the
   gap to "half as good as the store", not to the store average.
5. For paid sources, name what to check from the data: where the ads land
   (homepage vs product page), whether the offer in the ad matches the page,
   whether the audience is broad prospecting (naturally lower).

## Decision rules

- Ratio < `source.cvr_ratio_floor` and sessions >= `source.min_sessions`:
  `low_converting`.
- Ratio between the floor and 1: `below_store`, listed.
- Ratio >= 1: `ok`.
- Fewer than `source.min_sessions`: `needs_data` for that source.
- If UTM coverage is a `leak`, every source verdict carries that caveat.

## Output format

Summary line: store CVR, sources judged, `low_converting` sources, orders
short of the floor.

| Source | Sessions | Orders | CVR | x store | Orders short | Verdict |
|---|---|---|---|---|---|---|

Then: **Not enough sessions**, **What to check**, **Approval needed**.

## Practical example

*Made-up numbers for illustration.* 28 days: 40,000 sessions, 800 orders,
store CVR 2.00%.

| Source | Sessions | Orders | CVR | x store | Orders short | Verdict |
|---|---|---|---|---|---|---|
| Google Shopping | 5,000 | 140 | 2.80% | 1.40 | - | ok |
| Meta | 14,000 | 168 | 1.20% | 0.60 | - | below_store |
| TikTok | 6,000 | 30 | 0.50% | 0.25 | 30 | low_converting |
| Pinterest | 400 | 2 | 0.50% | - | - | needs_data |

TikTok: 6,000 x 1.00% = 60 orders at half the store rate, 30 actual: 30
orders short. Its ads all land on the homepage.

## Guardrails

- Never change ads, budgets or landing pages.
- Prospecting traffic converts below returning traffic by nature; say so
  rather than calling every cold channel a leak.
- Don't rank sources that are under the session minimum.
