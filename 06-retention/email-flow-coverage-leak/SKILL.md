---
name: email-flow-coverage-leak
description: Checks which core automated email flows exist and are live (welcome, abandoned checkout, browse abandonment, post-purchase, win-back) and how much email revenue comes from flows versus one-off campaigns, to find stores that depend on sending campaigns to make email work. Use when setting up Klaviyo or a similar tool, when email revenue rises and falls with each campaign, or in a retention review. Boundary: abandoned-checkout-recovery-leak measures one flow in depth; this skill checks whether the set of flows is complete.
---

# Email Flow Coverage Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- Email revenue spikes on campaign days and is near zero between them.
- Setting up or auditing Klaviyo (or Omnisend, Mailchimp, Shopify Email).
- Retention review.

## Required input

- **Flows list:** in Klaviyo, **Flows** > the list with each flow's name,
  trigger and status (Live / Manual / Draft), plus each flow's attributed
  revenue for the period (flow analytics or a flow performance report).
- **Email-attributed revenue split** for the same period: total from flows and
  total from campaigns (Klaviyo's analytics dashboard or a custom report).
- **Subscribed profiles** count.
- The tool's attribution window if shown; flows and campaigns use the same one.

## Live data (MarketAtoms MCP)

No live tool reads the email platform yet. Use the exports.

## Analysis workflow

1. Subscribed profiles under `email.min_profiles`: `needs_data` (the list is
   too small for flows to matter much yet; say what to build first).
2. Map the store's flows to the five core flows by trigger, not by name:
   welcome (joined list), abandoned checkout (started checkout), browse
   abandonment (viewed product), post-purchase (placed order), win-back
   (no order for a period).
3. A core flow is **covered** only if a flow with that trigger is Live.
4. Flow revenue share = flow revenue / (flow + campaign revenue).
5. For a missing win-back flow, point to lapsed-customer-leak for the size of
   the lapsed group.

## Decision rules

- Any core flow missing or not Live: `gap`, one line per missing flow.
- Flow revenue share < `email.flow_revenue_share_floor`: `campaign_dependent`.
- All five live and share at or above the floor: `ok`.
- Under the profile minimum: `needs_data`.
- Don't judge flows by open rate: opens are inflated by mail privacy features;
  use clicks and orders.

## Output format

Summary line: core flows live (x of 5), flow revenue share, verdict.

| Core flow | Trigger | Status | Revenue (period) | Finding |
|---|---|---|---|---|

Then: **Order to build missing flows** (abandoned checkout, welcome,
post-purchase, browse, win-back), **Approval needed**.

## Practical example

*Made-up numbers for illustration.* 8,400 subscribed profiles. Live: welcome,
abandoned checkout. Draft: post-purchase. Missing: browse abandonment,
win-back. Last 30 days email revenue $9,000: flows $2,250, campaigns $6,750.
Flow share 25.0%, under the 30% floor: `campaign_dependent`, and 3 `gap`
findings. lapsed-customer-leak shows how many past buyers a win-back flow
would reach.

## Guardrails

- Never create, edit or switch on flows, and never send email.
- Match flows by trigger; names are often misleading.
- Revenue attribution is the email tool's, not Shopify's; say so.
