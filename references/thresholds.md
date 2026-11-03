# Thresholds

Every number this library uses lives in this file, once. Skills cite a number by
its **key** (for example `discount.order_share_flag`) and never restate the
value. Change a number here and every skill and script follows.

Each entry has one tag:

- `[platform]` - stated by Shopify, Google or Meta in their own documentation
  or interface.
- `[heuristic]` - a practitioner starting point from MarketAtoms client work.
  Recalibrate it against the store's own history.

Almost everything here is `[heuristic]`, and that is the honest label.
Shopify, Google and Meta publish requirements, not benchmarks for a "healthy"
repeat rate or discount share. Numbers from other tools (Klaviyo, GA4 settings)
are `[heuristic]` too: only Shopify, Meta and Google statements earn `[platform]`.

## Rules for using a threshold

1. **One number, not a range.** Two people applying the same rule to the same
   store should land in the same place.
2. **Use the default unless you have a reason.** When you move a value for a
   store, say in the output which key you moved, to what, and why. An
   unexplained change reads as a fact.
3. **Respect the minimum sample.** Every check has a minimum volume key. Below
   it, the verdict is `needs_data`, never a guess.

## Words used in this file

| Term | Means | Does not mean |
| --- | --- | --- |
| **order** | One completed Shopify order, counted once however many line items it has. Test and cancelled orders excluded. | A checkout, a cart or a session |
| **customer** | One unique email address in the Orders export | A Shopify customer record with no orders |
| **period** | The date range under review, in the store's own time zone | A rolling window in another time zone |
| **previous period** | The same number of days immediately before the period | The same dates last year (unless the skill says so) |
| **revenue** | Order `Total` after discounts, before refunds, in the store currency | Gross sales before discounts |
| **net revenue** | Revenue minus `Refunded Amount` | |
| **CVR** | Orders divided by sessions for the same period and segment | Add-to-cart rate |

## Checkout and conversion

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `funnel.min_sessions` | **1000 sessions** | [heuristic] | Minimum sessions in each period before a funnel step change is judged. Below this, normal day-to-day noise is bigger than most real changes. |
| `funnel.step_drop_flag` | **15% relative drop** | [heuristic] | A funnel step rate (for example "reached checkout -> completed") that fell by this share or more against the previous period. 15% relative, not 15 percentage points. |
| `device.min_sessions` | **500 sessions** | [heuristic] | Minimum sessions per device type before mobile and desktop are compared. |
| `device.mobile_cvr_ratio_floor` | **0.5** | [heuristic] | Mobile CVR divided by desktop CVR. Below this, mobile converts at less than half of desktop: a leak worth fixing, because most paid social traffic is mobile. |
| `pdp.min_views` | **300 product views** | [heuristic] | Minimum views in the period before a product page's add-to-cart rate is judged. |
| `pdp.atc_ratio_floor` | **0.5** | [heuristic] | A product's add-to-cart rate divided by the store's median product add-to-cart rate. Below this, the page under-converts its own traffic. |

## Basket value

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `aov.near_threshold_band` | **15%** | [heuristic] | Orders whose subtotal sits within this share **below** the free-shipping threshold count as "near misses" (for a $50 threshold: $42.50 to $49.99). |
| `aov.near_threshold_share_flag` | **20% of orders** | [heuristic] | If this share of orders are near misses, the threshold or the cart upsell is costing basket value. |
| `aov.single_item_share_flag` | **70% of orders** | [heuristic] | Share of orders with exactly one unit. Above this, there is room for bundles or cross-sells. |
| `aov.min_orders` | **100 orders** | [heuristic] | Minimum orders in the period before basket checks are judged. |

## Retention

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `repeat.window_days` | **90 days** | [heuristic] | How long after a first order the pack looks for a second order. Use 60 for consumables bought monthly; 180 for slow categories such as furniture. Say which you used. |
| `repeat.second_order_rate_floor` | **20%** | [heuristic] | Share of first-time customers who place a second order within `repeat.window_days`. Below this, retention is a leak. Strongly category-dependent: recalibrate against the store's own best cohort. |
| `repeat.min_cohort_customers` | **50 customers** | [heuristic] | Minimum first-time customers in a cohort (month or first product) before its repeat rate is judged. |
| `repeat.product_gap_ratio` | **0.5** | [heuristic] | A first product whose second-order rate is below this share of the store average: customers who start there rarely come back. |

## Discounts and refunds

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `discount.order_share_flag` | **40% of orders** | [heuristic] | Share of orders using any discount code. Above this, full price has stopped being the normal price. |
| `discount.depth_flag` | **20%** | [heuristic] | Average discount amount divided by (revenue + discount amount) on discounted orders. |
| `discount.spike_multiple` | **3x** | [heuristic] | A code's weekly uses against its own average over the previous 4 weeks. A sudden spike on a code meant for a small group often means it leaked to a coupon site. |
| `discount.min_code_orders` | **20 orders** | [heuristic] | Minimum uses of a code in the period before it is judged on its own. |
| `refund.product_rate_flag` | **10% of a product's revenue** | [heuristic] | Refunded value divided by revenue, per product, for the period. |
| `refund.min_product_orders` | **20 orders** | [heuristic] | Minimum orders containing a product before its refund rate is judged. |
| `refund.store_rate_flag` | **8% of revenue** | [heuristic] | Store-wide refunded value divided by revenue. Above this, profit reported on gross revenue is overstated enough to change decisions. |

## Tracking and ads

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `tracking.gap_flag` | **15%** | [heuristic] | Gap between orders Shopify attributes to a channel and purchases that channel's ad platform reports, for the same dates, time zone and attribution basis. Above this, reconcile before trusting either number for budget decisions. |
| `tracking.min_orders` | **30 orders** | [heuristic] | Minimum Shopify orders attributed to a channel in the period before its gap is judged. |
| `ads.wasted_cpa_multiple` | **1.5x target CPA** | [heuristic] | An ad set, campaign or search term that has spent this multiple of the store's target cost per purchase with zero purchases. |
| `ads.wasted_min_spend` | **20 in store currency** | [heuristic] | Used only when no target CPA is given: minimum spend with zero purchases to flag. |
| `ads.learning_days` | **4 days** | [heuristic] | Ad sets launched more recently than this are excluded from wasted-spend verdicts; they have not had time to learn. |
| `stock.days_of_cover_floor` | **7 days** | [heuristic] | Units in stock divided by average daily units sold (last 28 days). Below this, a product receiving ad traffic is about to run out. |

## Profit

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `margin.contribution_floor` | **10% of net revenue** | [heuristic] | Contribution margin = net revenue - cost of goods - shipping cost - payment fees - discounts already in revenue - ad spend. Below this, growth is buying revenue, not profit. Negative = `critical`. |
| `margin.payment_fee_default` | **3% of revenue** | [heuristic] | Used only when the store does not supply its own payment fee rate. Say when the default was used. |

## Meta creative and audiences

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `creative.frequency_flag` | **3.0** | [heuristic] | 7-day frequency of a single ad at or above which fatigue becomes likely. |
| `creative.ctr_drop_flag` | **30% relative drop** | [heuristic] | An ad's latest-week link CTR against its own first `creative.baseline_days`. 30% relative, not 30 percentage points. |
| `creative.baseline_days` | **7 days** | [heuristic] | The ad's first days live, used as its own baseline. |
| `creative.min_impressions` | **5000 impressions** | [heuristic] | Minimum impressions in each compared week before an ad is judged. |
| `placement.cpa_ratio_flag` | **2x** | [heuristic] | A placement's cost per purchase divided by the account's cost per purchase for the same period. At or above this, the placement buys sales at double the price. |
| `placement.min_spend_share` | **10% of spend** | [heuristic] | Placements below this share of spend are listed but not judged; they can't move the total. |
| `placement.min_purchases` | **30 purchases** | [heuristic] | Minimum account purchases in the period before placements are compared. |
| `audience.prospecting_frequency_flag` | **2.5** | [heuristic] | 7-day frequency on a prospecting (cold) ad set. Above this the same people see the ad repeatedly; the audience is running out. |
| `audience.retargeting_frequency_flag` | **6.0** | [heuristic] | 7-day frequency on a retargeting ad set. |
| `audience.cpm_rise_flag` | **25% relative rise** | [heuristic] | Latest-week CPM against the ad set's average for the 4 weeks before. A frequency flag plus a CPM rise = `saturated`. |
| `audience.min_weekly_reach` | **5000 people** | [heuristic] | Minimum weekly reach before an ad set's frequency is judged. |

## Google Shopping and feed

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `feed.zero_impression_days` | **14 days** | [heuristic] | An approved, in-stock product with zero Shopping impressions for this long is invisible: it is in the feed but Google isn't showing it. |
| `feed.zero_share_flag` | **20% of products** | [heuristic] | If this share of approved, in-stock products is invisible, the problem is the feed or campaign structure, not single products. |
| `feed.min_products` | **20 products** | [heuristic] | Minimum approved, in-stock products before the feed-level share is judged. Single products are still listed below this. |
| `disapproval.share_flag` | **5% of products** | [heuristic] | Share of submitted products that are disapproved. Above this, treat it as a feed problem, not a product problem. |
| `disapproval.lookback_days` | **90 days** | [heuristic] | Shopify sales window used to rank disapproved products by revenue at stake. |
| `shopping.roas_ratio_floor` | **0.5** | [heuristic] | A product's Shopping ROAS divided by the store's target ROAS. Below this, the product drags the campaign. |
| `shopping.min_product_cost` | **50 in store currency** | [heuristic] | Minimum cost on a product in the period before its ROAS is judged. |
| `brand.conversion_share_flag` | **50% of conversions** | [heuristic] | Share of Google conversions that come from brand-name searches. Above this, blended Google ROAS mostly measures people who already knew the store. |
| `brand.min_conversions` | **30 conversions** | [heuristic] | Minimum Google conversions in the period before the brand share is judged. |
| `benchmark.price_gap_flag` | **10% above benchmark** | [heuristic] | A product priced this much above the benchmark price in Google Merchant Center's price competitiveness report. |
| `benchmark.min_clicks` | **50 clicks** | [heuristic] | Minimum Shopping clicks on a product in the period before its price gap is ranked. Products below are listed, not ranked. |

## Tracking hygiene

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `utm.unattributed_share_flag` | **30% of orders** | [heuristic] | Share of orders Shopify marks as direct, unknown or with no referrer/UTM. Above this, paid channels are being under-credited in Shopify. |
| `utm.min_orders` | **100 orders** | [heuristic] | Minimum orders in the period before the attribution share is judged. |
| `value.mismatch_flag` | **20%** | [heuristic] | Platform-reported value per purchase against the Shopify AOV of that channel's orders. Beyond this either way, the platform is sending the wrong value (tax, shipping, currency, or a fixed value). |
| `value.min_purchases` | **30 purchases** | [heuristic] | Minimum platform purchases before value per purchase is compared. |

## Conversion

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `search.no_result_share_flag` | **10% of searches** | [heuristic] | Share of on-site searches that return no results. |
| `search.min_term_searches` | **20 searches** | [heuristic] | Minimum searches for one term before it is listed as a lost demand term. |
| `search.min_searches` | **500 searches** | [heuristic] | Minimum on-site searches in the period before the no-results share is judged. |
| `source.cvr_ratio_floor` | **0.5** | [heuristic] | A traffic source's CVR divided by the store CVR for the same period. Below this, the store pays for visits that rarely buy. |
| `source.min_sessions` | **500 sessions** | [heuristic] | Minimum sessions from a source before its CVR is judged. |

## Basket and pricing

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `pairs.lift_flag` | **1.5** | [heuristic] | How much more often two products are bought together than chance would predict (lift). At or above this, the pair is a real bundle or cross-sell candidate. |
| `pairs.min_pair_orders` | **30 orders** | [heuristic] | Minimum orders containing both products before a pair is reported. |
| `pairs.min_orders` | **300 orders** | [heuristic] | Minimum orders in the period before pairs are looked for at all. |
| `pricing.compare_days` | **28 days** | [heuristic] | Days before and after a price change that are compared. Same length on both sides. |
| `pricing.units_drop_flag` | **20% relative drop** | [heuristic] | Fall in units per day after a price change. With revenue per day also down, the change cost money. |
| `pricing.min_units` | **50 units** | [heuristic] | Minimum units sold on each side of the change before it is judged. |
| `markdown.revenue_share_flag` | **50% of revenue** | [heuristic] | Share of product revenue sold with a compare-at ("was") price. Above this, the sale price has become the real price. |
| `markdown.depth_flag` | **30%** | [heuristic] | Average (compare-at - price) / compare-at on marked-down products. |
| `markdown.min_products` | **10 products** | [heuristic] | Minimum active products before the markdown share is judged. |

## Email and lapsed customers

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `recovery.flow_coverage_floor` | **50% of abandoned checkouts** | [heuristic] | Abandoned-checkout emails sent divided by abandoned checkouts with an email address. Below this, most abandoners never get a reminder. |
| `recovery.recovery_rate_floor` | **5% of recipients** | [heuristic] | Share of abandoned-checkout email recipients who then place an order. |
| `recovery.min_checkouts` | **200 checkouts** | [heuristic] | Minimum abandoned checkouts in the period before recovery is judged. |
| `email.flow_revenue_share_floor` | **30% of email revenue** | [heuristic] | Share of email-attributed revenue that comes from automated flows rather than one-off campaigns. |
| `email.min_profiles` | **1000 profiles** | [heuristic] | Minimum subscribed profiles before flow coverage and list health are judged. |
| `email.bounce_rate_flag` | **2% of sends** | [heuristic] | Average bounce rate across campaigns in the period. |
| `email.unsubscribe_rate_flag` | **0.5% of deliveries** | [heuristic] | Average unsubscribe rate across campaigns in the period. |
| `email.spam_rate_ceiling` | **0.3%** | [platform] | Google's Gmail sender guidelines: keep the spam rate reported in Google Postmaster Tools below 0.3% (Google recommends staying under 0.1%). Measured in Postmaster Tools, not in the email tool's complaint column. |
| `email.min_campaign_recipients` | **1000 recipients** | [heuristic] | Minimum recipients per campaign before its rates count towards the average. |
| `lapse.gap_multiple` | **2x** | [heuristic] | A repeat customer counts as lapsed when their last order is older than this multiple of the store's median gap between first and second order. |
| `lapse.default_days` | **180 days** | [heuristic] | Used only when the store has too few second orders to compute its own median gap. Say when the default was used. |
| `lapse.repeat_share_flag` | **30% of repeat customers** | [heuristic] | Share of repeat customers (2+ orders) who are lapsed. Above this, a win-back flow is worth building or fixing. |
| `lapse.min_repeat_customers` | **50 customers** | [heuristic] | Minimum repeat customers before the lapsed share is judged. |

## Shipping, stock and SKU margin

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `shipping.recovery_floor` | **0.5** | [heuristic] | Shipping charged to customers divided by shipping labels paid, for the period. Below this, the store pays more than half of every shipping bill. |
| `shipping.cost_share_flag` | **10% of revenue** | [heuristic] | Shipping labels paid minus shipping charged, as a share of revenue. |
| `shipping.min_orders` | **100 orders** | [heuristic] | Minimum shipped orders before shipping recovery is judged. |
| `stock.dead_days` | **90 days** | [heuristic] | A SKU with stock on hand and zero units sold for this long is dead stock. |
| `stock.dead_value_share_flag` | **20% of inventory value** | [heuristic] | Dead stock at cost as a share of all inventory at cost. |
| `sku.gross_margin_floor` | **40%** | [heuristic] | (Price - cost per item) / price, after discounts, before shipping, fees and ads. Below this, little is left to pay for the rest. |
| `sku.min_units` | **20 units** | [heuristic] | Minimum units sold in the period before a SKU's margin is judged. |

## Reporting

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `pulse.deviation_flag` | **30%** | [heuristic] | A day's orders or revenue against the average of the same weekday over the previous `pulse.baseline_weeks`. Beyond this either way, look today. |
| `pulse.baseline_weeks` | **4 weeks** | [heuristic] | Same-weekday history used as the baseline. |
| `pulse.min_daily_orders` | **20 orders** | [heuristic] | Minimum average daily orders in the baseline before a day is judged. Below this, single days are noise. |
| `fix.compare_days` | **14 days** | [heuristic] | Days before and after a fix that are compared. Same length on both sides. |
| `fix.min_change` | **10% relative** | [heuristic] | Smallest relative change in the fixed metric that counts as `improved` or `worse`. Smaller = `no_clear_change`. |

## Readout

| Key | Value | Tag | Notes |
| --- | --- | --- | --- |
| `readout.max_actions` | **3** | [heuristic] | The weekly readout names at most this many actions. More than three and none get done. |
