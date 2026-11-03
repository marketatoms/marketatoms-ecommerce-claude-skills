# How this library works as a system

Guidance for any AI agent (or person) running these skills. Forty prompts
become a system only when the order and the blocking rules below are followed.

## The order: trust the numbers, then find the leak, then size it, then decide

```
1. Measurement          03-tracking
                        tracking-gap-leak, ga4-order-gap-leak,
                        google-conversion-action-leak,
                        conversion-value-mismatch-leak, utm-coverage-leak
        |
        v
2. Ad money leaving     01-meta-ads
                        wasted-ad-spend-leak, stockout-ad-spend-leak,
                        creative-fatigue-leak, audience-saturation-leak,
                        placement-spend-leak
                        02-google-shopping
                        product-disapproval-leak, feed-zero-impressions-leak,
                        shopping-product-roas-leak, branded-search-share-leak,
                        price-competitiveness-leak
        |
        v
3. Store money leaving  discount-leak, markdown-depth-leak (05-basket-pricing)
                        refund-and-return-leak (07-profit-ops)
        |
        v
4. Money not won        04-conversion
                        checkout-drop-leak, mobile-conversion-gap-leak,
                        product-page-conversion-leak, site-search-leak,
                        traffic-source-conversion-leak
                        05-basket-pricing
                        basket-value-gap-leak, cross-sell-pair-leak,
                        price-change-leak
        |
        v
5. Retention            06-retention
                        second-order-gap-leak, abandoned-checkout-recovery-leak,
                        email-list-health-leak, email-flow-coverage-leak,
                        lapsed-customer-leak
        |
        v
6. Profit               07-profit-ops
                        contribution-margin-leak, shipping-cost-recovery-leak,
                        low-margin-sku-leak, dead-stock-leak
        |
        v
7. Decision             08-reporting
                        daily-revenue-pulse (every morning)
                        weekly-revenue-leak-readout (every Monday, max 3 actions)
                        channel-performance-scorecard, monthly-revenue-leak-review
                        (month end), leak-fix-tracker (two weeks after each fix)
```

**First audit of a store:** run top to bottom. Measurement first, because every
later number stands on it. Within a box, run the skills in the order listed.

**Something already looks wrong:** start at the section that matches the
symptom, then work upwards to check the measurement under it.

**Folders are for installing; this order is for running.** A folder groups
skills by area (all Meta skills together); the order above mixes folders where
one check depends on another.

## Blocking rules

Apply these without being asked. Rules 1-8 are unchanged from
shopify-revenue-leak-skills 1.0.0.

1. **A tracking gap makes every ad-platform number provisional.** If
   `tracking-gap-leak` returns `reconcile` for a platform, any cost per
   purchase, ROAS or "wasted" verdict from that platform for the same period is
   reported with the caveat "platform purchases under-counted by about X%".
   Wasted-spend findings may still be listed, but never as "pause this".
2. **A zero-purchase ad set inside its learning window is not waste.** Ad sets
   younger than `ads.learning_days` are listed separately as "too new to judge".
3. **A stock-out outranks a conversion problem on the same product.** If
   `stockout-ad-spend-leak` flags a product, `product-page-conversion-leak`
   does not report that product's low add-to-cart rate as a page problem; the
   product may simply be unavailable in some variants.
4. **Refunds come off before anyone says "profitable".**
   `contribution-margin-leak` always starts from net revenue (after refunds).
   No skill reports a margin on gross revenue.
5. **Discounts are counted once.** Shopify's `Total` is already after
   discounts. `discount-leak` reports the discount given away; it is never
   subtracted a second time in `contribution-margin-leak`.
6. **A device gap and a checkout drop can be the same finding.** If
   `mobile-conversion-gap-leak` and `checkout-drop-leak` both flag, and the
   checkout drop is concentrated on mobile, report one finding (mobile
   checkout), not two.
7. **Small samples get `needs_data`, never a verdict.** Every check has a
   minimum volume key in `references/thresholds.md`. Below it, say what volume
   is missing.
8. **The readout combines; it does not re-analyse.** `weekly-revenue-leak-readout`
   uses the other skills' outputs. If a skill was not run, it says which one
   and what it therefore cannot state. It never upgrades a low-confidence
   finding to a fact.
9. **A Google settings problem blocks Google verdicts like a tracking gap.** If
   `google-conversion-action-leak` returns `double_counting` or `wrong_goal`,
   every Google figure for the period (`wasted-ad-spend-leak` for Google,
   `shopping-product-roas-leak`, `branded-search-share-leak`, the Google row of
   `channel-performance-scorecard`) is provisional under rule 1.
10. **A value mismatch changes ROAS, not counts.** If
    `conversion-value-mismatch-leak` flags a platform, ROAS-based findings for
    it carry the adjusted ROAS beside the reported one. Purchase counts and
    cost per purchase are unaffected.
11. **Shopify attribution needs UTMs.** If `utm-coverage-leak` returns `leak`,
    `traffic-source-conversion-leak` and the Shopify columns of
    `channel-performance-scorecard` carry the caveat that paid channels are
    under-credited in Shopify.
12. **GA4 is checked before it is used.** No skill uses GA4 numbers while
    `ga4-order-gap-leak` is `reconcile` for the period.
13. **One product, one feed finding.** Disapproved and out-of-stock items are
    excluded from `feed-zero-impressions-leak`; a disapproved product appears
    once, under `product-disapproval-leak`.
14. **Ad and audience fatigue on the same ad set are one finding.** If
    `audience-saturation-leak` flags an ad set and `creative-fatigue-leak`
    flags ads inside it, report the audience finding and list the ads under
    it. A new ad won't fix an audience that has run out.
15. **Gmail spam rate outranks every email finding.** If
    `email-list-health-leak` returns `critical`, building or changing flows
    (`email-flow-coverage-leak`, `abandoned-checkout-recovery-leak`, a win-back
    for `lapsed-customer-leak`) waits until it is fixed.
16. **Margin lost to discounting is counted once.** If `low-margin-sku-leak`
    flags a SKU whose low margin comes from discounts or markdowns, the money is
    reported under `discount-leak` or `markdown-depth-leak` and the SKU finding
    points there.
17. **Shipping cost is counted once.** The net shipping cost from
    `shipping-cost-recovery-leak` is the shipping line in
    `contribution-margin-leak`, not a second deduction.
18. **A fix is judged with the original check's minimum.** `leak-fix-tracker`
    uses the same minimum-volume key as the skill that found the leak, and the
    same window length on both sides.
19. **Reporting skills combine; they do not re-analyse.** Rule 8 applies to
    `monthly-revenue-leak-review` and `channel-performance-scorecard` too.
    `daily-revenue-pulse` below its minimum volume hands over to the weekly
    readout instead of judging single days.

## Where the arithmetic lives

Counting is done by small Python scripts (standard library only), not by the
AI reading a CSV by eye:

| Script | Used by | Does |
| --- | --- | --- |
| `scripts/tracking_gap.py` | tracking-gap-leak, ga4-order-gap-leak, google-conversion-action-leak, channel-performance-scorecard | Platform-reported purchases vs Shopify orders, one rule for every source |
| `scripts/discount_leak.py` | discount-leak | Discount share, depth, per-code usage and weekly spikes |
| `scripts/basket_value.py` | basket-value-gap-leak | Near-miss orders under the free-shipping threshold, single-item share |
| `scripts/repeat_rate.py` | second-order-gap-leak | First-order cohorts by month and by first product; second orders inside the window |
| `scripts/feed_zero_impressions.py` | feed-zero-impressions-leak | Approved, in-stock products with zero impressions; share of the feed |
| `scripts/cross_sell_pairs.py` | cross-sell-pair-leak | Product pairs bought together, with lift |
| `scripts/price_change.py` | price-change-leak | Units and revenue per day before and after a price change |
| `scripts/lapsed_customers.py` | lapsed-customer-leak | Repeat customers past the store's own lapse point |
| `scripts/dead_stock.py` | dead-stock-leak | SKUs in stock with no sales in the window, valued at cost |
| `scripts/daily_pulse.py` | daily-revenue-pulse | A day against the same weekday over previous weeks |

Each script reads its thresholds from `references/thresholds.md` at run time,
so changing a number there changes the script. `scripts/selftest.py` checks the
scripts against the sample data in `examples/`.

If the AI client cannot run Python (for example a plain chat), the skill
explains the same calculation step by step and says the result was computed by
hand.

## Live data through the MarketAtoms MCP

If the MarketAtoms MCP is connected, prefer its tools to asking for exports:

| Tool | Replaces |
| --- | --- |
| `store_snapshot` | Orders export totals for a period (orders, revenue, AOV, discounts, refunds) |
| `meta_summary` | Meta Ads campaign export |
| `meta_wasted_spend` | Meta ad set export for the wasted-spend check |

Tools not yet available in the connector still need the export. Never mix a
live number and an exported number for different dates in one comparison.

## Hard limits, in one place

Nothing in this library logs into Shopify, an ad account, Merchant Center, GA4
or an email tool by itself, edits a product, price, discount, feed, theme,
flow or campaign, sends a message, or moves budget. Every finding is a decision
put in front of a person.
