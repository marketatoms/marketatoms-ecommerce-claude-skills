---
name: abandoned-checkout-recovery-leak
description: Checks whether shoppers who abandon checkout actually get a reminder, and how many of those reminders bring an order back - finding stores where most abandoners are never contacted or where the flow rarely recovers anyone. Use when checkout abandonment is high, after changing email tools, or when setting up retention flows. Boundary: checkout-drop-leak finds where people leave the funnel; this skill checks what happens after they leave.
---

# Abandoned Checkout Recovery Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Many shoppers reach checkout and don't pay.
- The store moved email tools (for example to Klaviyo) and isn't sure the
  reminder still runs.
- Setting up or reviewing retention flows.

## Required input

- **Shopify abandoned checkouts:** Shopify admin > **Orders** > **Abandoned
  checkouts** > date range > **Export** (CSV). Count checkouts that have an
  email address.
- **Email tool flow report:** in Klaviyo, **Flows** > the abandoned checkout
  flow > **Analytics** (or a flow performance report) for the same dates:
  recipients of the first email and orders placed from the flow. Other tools
  (Omnisend, Mailchimp, Shopify Email) have the same numbers under similar
  names; say which tool was used.
- If Shopify's own abandoned checkout emails are on as well, say so: both can
  send.

## Live data (MarketAtoms MCP)

No live tool reads abandoned checkouts or email flows yet. Use the exports.

## Analysis workflow

1. Abandoned checkouts with email in the period. Under
   `recovery.min_checkouts`: `needs_data`.
2. Coverage = flow recipients (first email) / abandoned checkouts with email.
3. Recovery rate = orders placed from the flow / flow recipients.
4. If there is no live abandoned checkout flow at all: `no_flow`.
5. Orders per extra 100 recipients at today's recovery rate = recovery rate x
   100. This shows what better coverage is worth without inventing a target.

## Decision rules

- No live flow: `no_flow` - the most urgent retention finding.
- Coverage < `recovery.flow_coverage_floor`: `coverage_leak`. Typical causes
  to check: flow filters excluding people, consent settings, the flow's trigger
  not connected to Shopify checkouts.
- Recovery rate < `recovery.recovery_rate_floor`: `weak_recovery` - check
  timing of the first email, subject line, and whether the link restores the cart.
- Both above their floors: `ok`.
- Under the checkout minimum: `needs_data`.

## Output format

Summary line: abandoned checkouts with email, coverage, recovery rate, verdict.

| Measure | Value | Floor | Verdict |
|---|---|---|---|

Then: **What to check**, **Approval needed** (flow edits are the owner's).

## Practical example

*Made-up numbers for illustration.* 28 days: 1,200 abandoned checkouts with an
email address. The Klaviyo flow's first email reached 480: coverage 40.0%,
under the 50% floor: `coverage_leak`. 31 orders came back from those 480:
recovery rate 6.5%, above the 5% floor. At that rate every extra 100 people
reached is worth about 6.5 orders.

## Guardrails

- Never edit, switch on or send a flow or email.
- Don't double count: if Shopify's own reminder also sends, say both exist.
- Don't contact customers or export their addresses for any other use.
