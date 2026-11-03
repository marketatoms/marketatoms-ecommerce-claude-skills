---
name: audience-saturation-leak
description: Finds Meta ad sets whose audience is running out - prospecting ad sets showing the same people the ads repeatedly while CPM climbs, and retargeting ad sets hitting a small pool far too often. Use when CPM rises week after week, before raising a budget, or when retargeting costs climb. Boundary: creative-fatigue-leak judges individual ads; this skill judges the audience behind the ad set.
---

# Audience Saturation Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- "CPM keeps rising and I haven't changed anything."
- Before scaling an ad set's budget: is there room in the audience?
- Retargeting cost per purchase is climbing.

## Required input

- **Meta Ads Manager, ad set level, weekly:** Ads Manager > **Ad sets** > last
  5 weeks > **Breakdown** > **By time** > **Week** > **Reports** >
  **Export table data** (CSV). Columns: Ad set name, Reporting starts, Reach,
  Impressions, Frequency, CPM (cost per 1,000 impressions), Amount spent,
  Purchases.
- Which ad sets are **prospecting** (cold audiences) and which are
  **retargeting** (site visitors, engagers, customers). Ask if names don't say.

## Live data (MarketAtoms MCP)

No live tool yet gives weekly reach and frequency by ad set. Use the export.

## Analysis workflow

1. Take the latest full week per ad set: reach, 7-day frequency, CPM.
2. Ad sets with weekly reach under `audience.min_weekly_reach`: `needs_data`.
3. CPM change = latest-week CPM / average CPM of the 4 weeks before - 1.
4. Apply the decision rules separately to prospecting and retargeting.
5. For saturated ad sets, show spend in the latest week and the CPM increase
   in money: (latest CPM - earlier CPM) x latest impressions / 1,000.

## Decision rules

- **Prospecting:** frequency >= `audience.prospecting_frequency_flag` and CPM
  change >= `audience.cpm_rise_flag`: `saturated`. Suggest broadening the
  audience or adding new creative angles, never a budget increase.
- Prospecting frequency over the flag, CPM steady: `watch`.
- **Retargeting:** frequency >= `audience.retargeting_frequency_flag`:
  `overexposed` - the budget is larger than the pool. Suggest lowering the
  budget or widening the window (for example 30 to 60 days).
- Weekly reach under the minimum: `needs_data`.
- A CPM rise during a known seasonal peak (for example the weeks around Black
  Friday) is reported with that note; it is not saturation on its own.

## Output format

Summary line: ad sets checked, saturated or overexposed, extra CPM cost last week.

| Ad set | Type | Reach (week) | Frequency (7d) | CPM latest | CPM 4 weeks before | Change | Spend latest week | Verdict |
|---|---|---|---|---|---|---|---|---|

Then: **Watch list**, **Not enough data**, **Approval needed**.

## Practical example

*Made-up numbers for illustration.*

- "Broad - US 25-44" (prospecting): reach 41,000, frequency 2.9, 118,900
  impressions, CPM $14.80 vs $11.20 before (+32.1%): `saturated`. Extra CPM cost
  last week: ($14.80 - $11.20) x 118.9 = $428.04.
- "Site visitors 30d" (retargeting): reach 6,200, frequency 7.4:
  `overexposed`.
- "LAL 2% purchasers": reach 3,800 last week: `needs_data`.

## Guardrails

- Never change an audience, budget or ad set. Suggest; the owner decides.
- Frequency alone is not a verdict for prospecting; CPM must back it up.
- Don't guess prospecting vs retargeting from spend; ask if names are unclear.
