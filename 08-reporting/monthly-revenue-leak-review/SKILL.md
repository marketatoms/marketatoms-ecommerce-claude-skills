---
name: monthly-revenue-leak-review
description: Combines a month of leak-check results with month-over-month store totals into one review for the owner or a board - what changed, which leaks were found and fixed, what is still open, and at most three priorities for next month. Use at month end, for an investor or client update, or after running several checks across the month. Boundary: it combines other skills' outputs and never re-analyses raw exports; weekly-revenue-leak-readout is the weekly version.
---

# Monthly Revenue Leak Review

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Order of checks and blocking rules: `../../AGENTS.md`.

## Use this skill when

- Month end.
- Writing an investor, board or client update.
- Several leak checks were run during the month and need one summary.

## Required input

- **Store totals** for this month and last month: orders, revenue, net revenue
  (after refunds), AOV. From Shopify admin > **Analytics** > **Reports** >
  "Sales over time" (or the Orders export).
- **Outputs of the leak checks run this month** (pasted or attached), and any
  `leak-fix-tracker` results for fixes made.
- Ad spend per channel for the month, if contribution or channel results are
  included.

## Live data (MarketAtoms MCP)

If connected, `store_snapshot` gives this month's and last month's totals, and
`meta_summary` Meta's month. Leak-check results still come from the checks.

## Analysis workflow

1. Store totals table: this month, last month, change.
2. Collect every finding from this month's checks: skill, verdict, money at
   stake (only if the skill computed it), confidence.
3. Apply AGENTS.md blocking rules before ranking: provisional ad findings stay
   provisional, `needs_data` stays `needs_data`.
4. Rank open findings by money at stake, then by confidence. Name at most
   `readout.max_actions` priorities.
5. List fixes made and their `leak-fix-tracker` verdicts.
6. List checks not run this month, and what the review therefore cannot say.

## Decision rules

- A finding enters the priorities only with a computed amount or a `critical`
  verdict; otherwise it is listed as open.
- Never more than `readout.max_actions` priorities.
- A fix without a tracker result is "done, effect not yet measured".
- Never upgrade a finding's confidence or turn `needs_data` into a number.
- If tracking was `reconcile` for any platform this month, the review says so
  at the top.

## Output format

1. **The month in one paragraph** (plain language).
2. **Store totals** table.
3. **Fixed this month** (with tracker verdicts).
4. **Open leaks** table: skill, finding, money at stake, confidence.
5. **Priorities for next month** (max `readout.max_actions`).
6. **Not checked this month**.

## Practical example

*Made-up numbers for illustration.* October revenue $62,000 vs $58,400 in
September (+6.2%). Net revenue after refunds $57,600. Checks run: tracking
(Meta `reconcile`, -23.9%), contribution margin (8.4%, under the 10% floor),
mobile checkout fix (tracker: `improved`, mobile CVR 1.00% -> 1.30%), lapsed
customers (`leak`, 106 lapsed repeat buyers). Priorities for November:
1. Reconcile Meta tracking before any budget change. 2. Raise contribution
margin: start with the low-margin SKU list. 3. Build the win-back flow.
Not checked: Google Shopping feed, site search.

## Guardrails

- Never change anything; this is a report.
- No number appears that a check or the store totals didn't produce.
- Keep `needs_data` findings visible; don't drop them to make the review look clean.
