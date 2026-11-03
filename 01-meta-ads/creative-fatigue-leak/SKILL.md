---
name: creative-fatigue-leak
description: Finds Meta ads that have worn out - the same people see them again and again while link click-through rate falls below the ad's own first week - and the extra cost per purchase that fatigue is causing. Use when cost per purchase creeps up with no change in targeting, when a winning ad has run for weeks, or before planning new creative. Boundary: audience-saturation-leak judges the audience; this skill judges the individual ad.
---

# Creative Fatigue Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- "My best ad stopped working."
- Cost per purchase rose for weeks while targeting and budget stayed the same.
- Planning the next creative batch: which ads need replacing first?

## Required input

- **Meta Ads Manager, ad level:** Ads Manager > **Ads** tab > date range
  covering each ad's first week up to today > **Breakdown** > **By time** >
  **Week** > **Reports** > **Export table data** (CSV). Columns: Ad name,
  Ad set name, Reporting starts, Amount spent, Impressions, Frequency,
  Link clicks, CTR (link click-through rate), Purchases.
- Each ad's start date (the "Starts" column, or the first week it has spend).
- The tracking-gap verdict for Meta for the same period, if it exists
  (AGENTS.md rule 1).

## Live data (MarketAtoms MCP)

`meta_summary` gives campaign context only; it does not break down by ad and
week. This skill needs the export.

## Analysis workflow

1. For each ad, take its first `creative.baseline_days` live as the baseline
   and compute baseline link CTR = link clicks / impressions.
2. Take the latest full week: 7-day frequency, link CTR, cost per purchase.
3. Skip any ad with fewer than `creative.min_impressions` in either the
   baseline or the latest week: `needs_data`.
4. CTR change = (latest CTR - baseline CTR) / baseline CTR.
5. Apply the decision rules. Rank fatigued ads by latest-week spend: that is
   the money currently going through a tired ad.
6. For each fatigued ad, show cost per purchase in the baseline and now, so
   the owner sees what fatigue costs per sale.

## Decision rules

- Frequency >= `creative.frequency_flag` **and** CTR change at or below
  -`creative.ctr_drop_flag`: `fatigued`. Suggest a refresh (new hook, new first
  3 seconds, new format), never pause on its own.
- Frequency >= `creative.frequency_flag`, CTR holding: `watch`.
- CTR down by the flag but frequency under it: `not_fatigue` - the drop is
  something else (offer, landing page, season); say so.
- Below the impression minimum: `needs_data`, with the impressions it has.
- If Meta tracking is `reconcile`, cost-per-purchase figures carry the
  under-counting caveat; CTR and frequency are unaffected.

## Output format

Summary line: ads checked, ads fatigued, latest-week spend on fatigued ads.

| Ad | Ad set | Weeks live | Frequency (7d) | Link CTR first week | Link CTR latest | Change | Cost/purchase first week | Cost/purchase latest | Verdict |
|---|---|---|---|---|---|---|---|---|---|

Then: **Watch list**, **Not enough data**, **Approval needed** (any refresh or
pause is the owner's decision).

## Practical example

*Made-up numbers for illustration.*

- "UGC unboxing v2": first 7 days 48,000 impressions, 1,008 link clicks
  (CTR 2.10%), $1,120 spent, 50 purchases ($22.40 each). Latest week: 61,000
  impressions, frequency 3.4, 793 link clicks (CTR 1.30%), $1,270 spent,
  40 purchases ($31.75 each). CTR change -38.1%: `fatigued`. Each sale now
  costs $9.35 more than in week one.
- "Founder story": frequency 3.2, CTR 1.70% -> 1.62% (-4.7%): `watch`.
- "Static price card": 3,900 impressions last week: `needs_data`.

One fatigued ad, carrying $1,270 of last week's spend.

## Guardrails

- Never pause, edit or duplicate an ad. List, explain, and leave the decision
  to the owner.
- Never call an ad fatigued on CTR alone; frequency must back it up.
- Don't compare an ad with other ads' CTR: each ad is judged against its own
  first week.
- Fatigue is not waste: a fatigued ad may still sell profitably. Report both
  numbers and let the owner decide.
