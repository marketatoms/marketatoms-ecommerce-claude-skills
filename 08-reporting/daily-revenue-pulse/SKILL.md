---
name: daily-revenue-pulse
description: A one-minute morning check - yesterday's orders and revenue against the same weekday over the previous four weeks - that flags a day far off normal so something broken (checkout, payments, an ad account, the site) is caught the same day. Use every morning, after a deploy or theme change, or during a sale. Boundary: it flags that a day is unusual and points to the check to run; it does not diagnose why.
---

# Daily Revenue Pulse

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.
Arithmetic: `../../scripts/daily_pulse.py`.

## Use this skill when

- Every morning: "Was yesterday normal?"
- After a theme, app, checkout or payment change.
- During a sale or launch.

## Required input

- **Shopify Orders export** covering yesterday and the previous
  `pulse.baseline_weeks` weeks: Shopify admin > **Orders** > **Export** > CSV.
- Or the two numbers per day (orders and revenue) from Shopify admin >
  **Analytics** for the same days, typed in.
- Known events on the day (a sale, an email send, a holiday).

## Live data (MarketAtoms MCP)

If connected, call `store_snapshot` for yesterday and for each of the same
weekdays in the previous `pulse.baseline_weeks` weeks instead of exporting.
Don't mix live and exported days in one comparison.

## Analysis workflow

1. Run the script:
   `python3 scripts/daily_pulse.py --orders orders.csv` (defaults to the last
   full day in the export; `--day YYYY-MM-DD` for another).
2. Baseline = average orders and revenue on the same weekday over the previous
   `pulse.baseline_weeks` weeks.
3. If the baseline averages fewer than `pulse.min_daily_orders` orders:
   `needs_data` - single days are noise at this volume; suggest a weekly view
   (weekly-revenue-leak-readout).
4. Deviation = (day - baseline) / baseline, for orders and for revenue.
5. If flagged down, list the first checks in order: payments and checkout
   working, site up, ad accounts delivering (spend yesterday), stock on best
   sellers, then a known event.

## Decision rules

- Orders or revenue down by `pulse.deviation_flag` or more: `down` - check today.
- Up by the flag or more: `up` - note what drove it (a send, a sale) so it
  isn't mistaken for a trend.
- Within the flag: `normal`. Say so in one line.
- Baseline under `pulse.min_daily_orders`: `needs_data`.
- A known event explains the day: verdict stands, with the event noted.

## Output format

One line first: "Yesterday: X orders, $Y revenue - normal / down Z% / up Z%."
Then:

| | Orders | Revenue |
|---|---|---|
| Yesterday | | |
| Same weekday, 4-week average | | |
| Change | | |

Then, only if `down`: **Check in this order** (the list above).

## Practical example

*Made-up numbers for illustration.* Monday: 18 orders, $1,206 revenue. The
previous four Mondays averaged 30 orders and $2,010. Both -40.0%, past the 30%
flag: `down`. First check: payments. A payment app update on Sunday night had
switched off one card provider.

On the repository's sample store (about 7 orders a day) the script returns
`needs_data`, as it should.

## Guardrails

- Never change anything in the store, apps or ad accounts.
- One day is a prompt to look, not a trend.
- Don't run it on a store under the daily minimum; use the weekly readout.
