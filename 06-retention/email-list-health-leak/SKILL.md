---
name: email-list-health-leak
description: Checks the health of the email list from campaign results - bounce rate, unsubscribe rate and the Gmail spam rate from Google Postmaster Tools - to catch deliverability problems before email starts landing in spam. Use when email revenue falls without a clear reason, after importing a list, or before a big send such as Black Friday. Boundary: email-flow-coverage-leak checks which flows exist; this skill checks whether the emails reach inboxes.
---

# Email List Health Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Email clicks and revenue fall with no change in sending.
- After importing contacts or a list from another tool.
- Before a high-volume send.

## Required input

- **Campaign results:** in Klaviyo, **Campaigns** > the sent campaigns for the
  period > export or a campaign performance report. Columns: campaign name,
  send date, recipients, delivered, bounced, unsubscribes, spam complaints,
  clicks. Other tools have the same fields under similar names.
- **Gmail spam rate:** Google Postmaster Tools > the sending domain > spam
  rate for the same weeks. Only available if the domain is verified there;
  if not, say so and skip that check.

## Live data (MarketAtoms MCP)

No live tool reads the email platform or Postmaster Tools yet. Use the exports.

## Analysis workflow

1. Keep campaigns with at least `email.min_campaign_recipients` recipients.
   If none qualify: `needs_data`.
2. Bounce rate = bounced / recipients (all qualifying campaigns together).
3. Unsubscribe rate = unsubscribes / delivered.
4. Gmail spam rate: the highest daily value in Postmaster Tools for the period.
5. List the campaigns with the worst bounce and unsubscribe rates; a single
   bad send to an old or imported segment is the usual cause.

## Decision rules

- Gmail spam rate >= `email.spam_rate_ceiling`: `critical` - Google's own
  sender guidelines; inbox placement at Gmail is at risk. This outranks every
  other email finding.
- Bounce rate >= `email.bounce_rate_flag`: `bounce_problem` - suggest
  reviewing the list source and suppressing hard bounces.
- Unsubscribe rate >= `email.unsubscribe_rate_flag`: `list_fatigue` - sending
  too often or to the wrong segment.
- All under: `ok`.
- No qualifying campaigns: `needs_data`. No Postmaster data: that check is
  `needs_data`, the others stand.
- Opens are not used: mail privacy features inflate them.

## Output format

Summary line: campaigns checked, bounce, unsubscribe and Gmail spam rates,
verdict.

| Measure | Value | Flag | Verdict |
|---|---|---|---|

Then: **Worst campaigns**, **What to check**, **Approval needed** (list
cleaning and sending changes are the owner's).

## Practical example

*Made-up numbers for illustration.* 6 campaigns over 1,000 recipients each:
61,500 recipients, 1,500 bounced (2.4%, over the 2% flag): `bounce_problem`.
60,000 delivered, 210 unsubscribes (0.35%): under the flag. Postmaster Tools
peak spam rate 0.12%: under the 0.3% ceiling, though above the 0.1% Google
recommends staying under, so watch it. Most bounces came from one campaign
sent to a contact list imported in September.

## Guardrails

- Never send, schedule, suppress or delete contacts.
- Spam rate comes from Google Postmaster Tools, not from the email tool's
  complaint count; don't mix them.
- Don't list individual email addresses; counts only.
