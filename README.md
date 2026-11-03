# E-commerce Claude Skills by MarketAtoms

**40 free Claude Skills that find where a Shopify store is losing money** - in
Meta and Google ads, in tracking, on the site, in the basket, in retention and
in the margin - and say how much is at stake.

Built by [MarketAtoms](https://www.marketatoms.com), from the checks we run on
client stores. *Find the leak. Fix the system. Scale what works.*

- **Read-only.** No skill logs into your store, ad accounts, Merchant Center,
  GA4 or email tool, and none of them edits a product, price, discount, feed,
  flow, campaign or budget. Every finding is a decision for you.
- **Honest.** When the data can't support an answer, a skill says `needs_data`
  instead of guessing. Every number it uses is written down once, in one file,
  and tagged as a platform fact or a heuristic.
- **Whole store, not just ads.** Most AI packs stop at ROAS. These follow the
  money from the ad click to the second order and the margin left over.

## The 40 skills

### 01 - Meta ads

| # | Skill | The question it answers |
|---|---|---|
| 1 | [`wasted-ad-spend-leak`](01-meta-ads/wasted-ad-spend-leak/SKILL.md) | Which ad sets and search terms spent money and sold nothing? |
| 2 | [`stockout-ad-spend-leak`](01-meta-ads/stockout-ad-spend-leak/SKILL.md) | Which ads are sending people to products that are sold out, or about to be? |
| 3 | [`creative-fatigue-leak`](01-meta-ads/creative-fatigue-leak/SKILL.md) | Which ads have worn out - seen too often, clicked less than in their first week? |
| 4 | [`placement-spend-leak`](01-meta-ads/placement-spend-leak/SKILL.md) | Which placements buy purchases at double the account's cost or more? |
| 5 | [`audience-saturation-leak`](01-meta-ads/audience-saturation-leak/SKILL.md) | Which audiences are running out, with frequency and CPM both climbing? |

### 02 - Google Shopping

| # | Skill | The question it answers |
|---|---|---|
| 6 | [`feed-zero-impressions-leak`](02-google-shopping/feed-zero-impressions-leak/SKILL.md) | Which approved, in-stock products got zero impressions for 14 days? |
| 7 | [`product-disapproval-leak`](02-google-shopping/product-disapproval-leak/SKILL.md) | Which products has Merchant Center disapproved, and what do they normally sell? |
| 8 | [`shopping-product-roas-leak`](02-google-shopping/shopping-product-roas-leak/SKILL.md) | Which Shopping products return less than half the target ROAS? |
| 9 | [`branded-search-share-leak`](02-google-shopping/branded-search-share-leak/SKILL.md) | How much of Google's ROAS comes from people already searching for the store? |
| 10 | [`price-competitiveness-leak`](02-google-shopping/price-competitiveness-leak/SKILL.md) | Which products are priced well above what other sellers charge on Google? |

### 03 - Tracking

| # | Skill | The question it answers |
|---|---|---|
| 11 | [`tracking-gap-leak`](03-tracking/tracking-gap-leak/SKILL.md) | Do Meta and Google report the same sales Shopify recorded? |
| 12 | [`utm-coverage-leak`](03-tracking/utm-coverage-leak/SKILL.md) | How many orders arrive with no source, and which ads have no UTMs? |
| 13 | [`conversion-value-mismatch-leak`](03-tracking/conversion-value-mismatch-leak/SKILL.md) | Do the platforms attach the right value to each purchase? |
| 14 | [`ga4-order-gap-leak`](03-tracking/ga4-order-gap-leak/SKILL.md) | Does GA4 count the same orders as Shopify? |
| 15 | [`google-conversion-action-leak`](03-tracking/google-conversion-action-leak/SKILL.md) | Is Google Ads counting purchases twice, or optimising for the wrong action? |

### 04 - Conversion

| # | Skill | The question it answers |
|---|---|---|
| 16 | [`checkout-drop-leak`](04-conversion/checkout-drop-leak/SKILL.md) | Which step between cart and payment started losing people? |
| 17 | [`mobile-conversion-gap-leak`](04-conversion/mobile-conversion-gap-leak/SKILL.md) | How many orders are lost because the store converts badly on phones? |
| 18 | [`product-page-conversion-leak`](04-conversion/product-page-conversion-leak/SKILL.md) | Which product pages get views but no add-to-carts? |
| 19 | [`site-search-leak`](04-conversion/site-search-leak/SKILL.md) | What do shoppers search for and not find? |
| 20 | [`traffic-source-conversion-leak`](04-conversion/traffic-source-conversion-leak/SKILL.md) | Which traffic sources send visitors who rarely buy? |

### 05 - Basket and pricing

| # | Skill | The question it answers |
|---|---|---|
| 21 | [`basket-value-gap-leak`](05-basket-pricing/basket-value-gap-leak/SKILL.md) | How many orders stop just short of free shipping, and how many are single items? |
| 22 | [`discount-leak`](05-basket-pricing/discount-leak/SKILL.md) | How much do codes give away, and has a private code leaked to coupon sites? |
| 23 | [`cross-sell-pair-leak`](05-basket-pricing/cross-sell-pair-leak/SKILL.md) | Which products do customers already buy together, and aren't bundled yet? |
| 24 | [`price-change-leak`](05-basket-pricing/price-change-leak/SKILL.md) | Did the last price change earn or cost money? |
| 25 | [`markdown-depth-leak`](05-basket-pricing/markdown-depth-leak/SKILL.md) | Has the "sale" price quietly become the real price? |

### 06 - Retention

| # | Skill | The question it answers |
|---|---|---|
| 26 | [`second-order-gap-leak`](06-retention/second-order-gap-leak/SKILL.md) | How many first-time buyers come back, and which first products lead nowhere? |
| 27 | [`abandoned-checkout-recovery-leak`](06-retention/abandoned-checkout-recovery-leak/SKILL.md) | Do checkout abandoners get a reminder, and does it bring them back? |
| 28 | [`email-flow-coverage-leak`](06-retention/email-flow-coverage-leak/SKILL.md) | Are the five core email flows live, or does email depend on campaigns? |
| 29 | [`lapsed-customer-leak`](06-retention/lapsed-customer-leak/SKILL.md) | How many repeat buyers have gone quiet, and what did they spend before? |
| 30 | [`email-list-health-leak`](06-retention/email-list-health-leak/SKILL.md) | Are bounces, unsubscribes or the Gmail spam rate putting the inbox at risk? |

### 07 - Profit and operations

| # | Skill | The question it answers |
|---|---|---|
| 31 | [`contribution-margin-leak`](07-profit-ops/contribution-margin-leak/SKILL.md) | After product cost, shipping, fees, refunds and ads, what is actually left? |
| 32 | [`refund-and-return-leak`](07-profit-ops/refund-and-return-leak/SKILL.md) | How much revenue comes back, from which products, and how much does it inflate ROAS? |
| 33 | [`shipping-cost-recovery-leak`](07-profit-ops/shipping-cost-recovery-leak/SKILL.md) | How much of every shipping bill does the store pay itself? |
| 34 | [`dead-stock-leak`](07-profit-ops/dead-stock-leak/SKILL.md) | Which SKUs haven't sold in 90 days, and how much cash is sitting in them? |
| 35 | [`low-margin-sku-leak`](07-profit-ops/low-margin-sku-leak/SKILL.md) | Which products sell well but leave too little after product cost? |

### 08 - Reporting

| # | Skill | The question it answers |
|---|---|---|
| 36 | [`weekly-revenue-leak-readout`](08-reporting/weekly-revenue-leak-readout/SKILL.md) | Of everything found this week, what are the 3 things to do first? |
| 37 | [`daily-revenue-pulse`](08-reporting/daily-revenue-pulse/SKILL.md) | Was yesterday normal, or is something broken? |
| 38 | [`monthly-revenue-leak-review`](08-reporting/monthly-revenue-leak-review/SKILL.md) | What changed this month, what was fixed, what is still open? |
| 39 | [`channel-performance-scorecard`](08-reporting/channel-performance-scorecard/SKILL.md) | Which channel works, judged on Shopify's numbers? |
| 40 | [`leak-fix-tracker`](08-reporting/leak-fix-tracker/SKILL.md) | Did the fix actually work? |

Skills 1-2, 11, 16-18, 21-22, 26, 31-32 and 36 come unchanged from
[shopify-revenue-leak-skills](https://github.com/marketatoms/shopify-revenue-leak-skills).

## Where to start

1. Run the **03-tracking** checks first, starting with **`tracking-gap-leak`**.
   If the numbers are wrong, every decision built on them is wrong too.
2. Then the folder for your biggest worry: ads, Google Shopping, conversion,
   basket, retention or profit.
3. Every morning **`daily-revenue-pulse`**; every Monday
   **`weekly-revenue-leak-readout`**; at month end
   **`monthly-revenue-leak-review`**.

The full order and the rules for how the skills depend on each other are in
[`AGENTS.md`](AGENTS.md).

## How to use them (pick one)

### A. Copy and paste - no setup, works anywhere

Open any skill's `SKILL.md`, copy all of it into a new Claude chat (ChatGPT
works too), then attach the export it asks for. Claude will tell you if
something is missing.

The skills point to `references/thresholds.md` for their numbers. If you only
paste one skill, paste [`references/thresholds.md`](references/thresholds.md)
in as well.

### B. Add skills to the Claude app - one ZIP per folder

1. Download a folder's ZIP (for example `03-tracking.zip`) from the
   **Releases** page of this repository, or build them yourself with
   `python3 scripts/build_zips.py` (creates `dist/`).
2. Unzip it. Inside are five ZIPs, one per skill, each already containing the
   thresholds file and any script it needs.
3. In Claude, open **Settings**, find **Skills** (under capabilities), and
   upload the skill ZIPs you want, one by one. Skills availability depends on
   your Claude plan and on whether your workspace admin has enabled them.
4. Start a new chat and ask, for example: *"Check my Google Shopping feed for
   products with no impressions"* and attach the export.

### C. Claude Code - the full library

```bash
git clone https://github.com/marketatoms/marketatoms-ecommerce-claude-skills.git
cd marketatoms-ecommerce-claude-skills
python3 scripts/build_zips.py
mkdir -p ~/.claude/skills
cp -R dist/skill-folders/. ~/.claude/skills/
```

`build_zips.py` turns each skill into a self-contained folder (its own
`references/`, the scripts it uses and, for the reporting skills,
`AGENTS.md`), because Claude Code expects every skill folder directly inside
`~/.claude/skills/`. To install for one project only, copy into that
project's `.claude/skills/` instead. Start a new Claude Code session; skills
switch on when your question matches their description.

The full ZIP (`ecommerce-claude-skills-1.0.0.zip` on the Releases page) is the
whole repository, for reading or for building your own selection.

## Live data with the MarketAtoms MCP

Every skill works from exports. If you connect the **MarketAtoms MCP** to
Claude, skills that have a live tool (store totals, Meta campaigns, Meta wasted
spend) read your Shopify and Meta data directly instead, so the same checks can
run every morning without downloading anything. Google, GA4, Merchant Center
and email-tool checks still use exports.

The connector is in a private pilot with a small number of stores. To join,
email **support@marketatoms.com** with the subject "Engine pilot", or book a
free Revenue Leak Audit at [marketatoms.com](https://www.marketatoms.com).

## How the numbers work

Every threshold lives once in [`references/thresholds.md`](references/thresholds.md).
Skills cite it by key (for example `feed.zero_impression_days`), so a number
can't drift between skills. Each one is tagged:

- `[platform]` - stated by Shopify, Google or Meta.
- `[heuristic]` - a starting point from our client work. Recalibrate it to your
  store, and say which one you moved and why.

Almost all of them are heuristics, and they say so. The headline ones:

| Check | Threshold |
|---|---|
| Wasted ad spend | 1.5x target CPA spent with zero purchases |
| Invisible feed products | 14 days with zero impressions |
| Tracking gap | 15% between platform and Shopify |
| Weak product page | under 0.5x the store's typical add-to-cart rate |
| Near-miss baskets | within 15% under the free-shipping threshold |
| Second-order window | 90 days |
| Contribution margin floor | 10% of net revenue |

Counting is done by small Python scripts (standard library only, no installs),
not by the AI reading a spreadsheet by eye:

| Script | Used by |
|---|---|
| `scripts/tracking_gap.py` | tracking-gap-leak, ga4-order-gap-leak, google-conversion-action-leak, channel-performance-scorecard |
| `scripts/discount_leak.py` | discount-leak |
| `scripts/basket_value.py` | basket-value-gap-leak |
| `scripts/repeat_rate.py` | second-order-gap-leak |
| `scripts/feed_zero_impressions.py` | feed-zero-impressions-leak |
| `scripts/cross_sell_pairs.py` | cross-sell-pair-leak |
| `scripts/price_change.py` | price-change-leak |
| `scripts/lapsed_customers.py` | lapsed-customer-leak |
| `scripts/dead_stock.py` | dead-stock-leak |
| `scripts/daily_pulse.py` | daily-revenue-pulse |

See them run on a made-up sample store in
[`examples/worked-example.md`](examples/worked-example.md).

## Checking the library yourself

```bash
python3 scripts/validate_skills.py   # 8 folders x 5 skills; every section, key and path exists
python3 scripts/selftest.py          # the scripts' maths agrees with an independent recount
```

`validate_skills.py` also checks that every new skill has a `needs_data` rule,
a practical example labelled as made-up and a "Never" guardrail; that every
threshold is tagged and used; and that the headline thresholds above still
have the values this README states.

`selftest.py` recounts orders, discounts, near-misses, repeat and lapsed
customers, feed impressions and dead stock straight from the CSVs without the
shared helper; checks hand-built cases with known answers (a 2.4 lift, a -40%
day, a price change that cost revenue); and checks that bad input is refused
with a message.

What they can't check: whether the advice in a skill is right for your store.
That's your call, and why every threshold is written down.

## What these skills won't do

- Log into Shopify, Meta, Google, GA4, Merchant Center, an email tool or
  anything else.
- Change a product, price, discount, feed, theme, flow, campaign or budget, or
  send a message.
- Invent a number to make a report look complete.
- Call something a leak on too little data.

## Licence

MIT. Use them, change them, build them into your own process. A link back is
appreciated.
