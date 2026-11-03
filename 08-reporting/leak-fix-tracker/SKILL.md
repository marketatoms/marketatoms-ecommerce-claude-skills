---
name: leak-fix-tracker
description: Checks whether a fix actually worked - the metric a leak check flagged, measured for the same number of days before and after the change, with the original check's minimum sample - and records improved, worse, no clear change or too early. Use two weeks after any fix from a leak check, before reporting a win to a client, or when deciding whether to roll a fix out further. Boundary: other skills find leaks; this one judges the fixes.
---

# Leak Fix Tracker

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Two weeks after fixing something a leak check found.
- Before telling a client or team "the fix worked".
- Deciding whether to roll a change out more widely.

## Required input

- **What was fixed and when:** the leak check that found it, the date the fix
  went live, and the metric it should move (for example mobile CVR, abandoned
  checkout coverage, discount share).
- **The same export or report the original check used**, covering
  `fix.compare_days` before and after the fix date (for example Shopify
  Analytics sessions by device for a mobile fix).
- Other changes in the same weeks (sales, new campaigns, price changes).

## Live data (MarketAtoms MCP)

If the original check used a live tool (`store_snapshot`, `meta_summary`,
`meta_wasted_spend`), use it for both windows. Never compare a live window
with an exported one.

## Analysis workflow

1. Windows: `fix.compare_days` before the fix day and the same number after,
   excluding the fix day itself. If the after-window isn't finished:
   `too_early`.
2. Compute the metric in both windows exactly as the original skill does.
3. Check each window against the original skill's minimum sample key (for
   example `device.min_sessions` for a mobile fix). Below it: `needs_data`.
4. Relative change = (after - before) / before. For metrics where lower is
   better (cost, share given away), flip the sign so "improved" always means
   better.
5. List other changes in the windows.

## Decision rules

- Change >= `fix.min_change` in the right direction: `improved`.
- Change >= `fix.min_change` in the wrong direction: `worse` - put in front of
  the owner today.
- Smaller change: `no_clear_change`.
- After-window not finished: `too_early`. Under the original minimum:
  `needs_data`.
- Other big changes in the window: verdict marked `confounded`.

## Output format

Summary line: fix, metric, before, after, change, verdict.

| Window | Dates | Volume | Metric |
|---|---|---|---|
| Before | | | |
| After | | | |

Then: **Other changes in the windows**, **Next step** (roll out, revert, wait),
**Approval needed**.

## Practical example

*Made-up numbers for illustration.* Fix: mobile checkout button moved above
the fold on October 6, after mobile-conversion-gap-leak flagged mobile.

| Window | Dates | Mobile sessions | Orders | Mobile CVR |
|---|---|---|---|---|
| Before | Sep 22 - Oct 5 | 9,800 | 98 | 1.00% |
| After | Oct 7 - Oct 20 | 10,200 | 133 | 1.30% |

Both windows are over `device.min_sessions`. Change +30.4%, above the 10%
minimum: `improved`. No other site or ad change in the windows.

## Guardrails

- Never revert or roll out a change.
- Same window length on both sides, always.
- One fix, one metric: don't credit a fix with every number that moved.
