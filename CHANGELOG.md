# Changelog

## 1.0.0 - 2026-11-03

First release of the e-commerce library: 40 Claude Skills in 8 folders that
find revenue leaks in a Shopify store.

### Added

- **01-meta-ads:** `creative-fatigue-leak`, `placement-spend-leak`,
  `audience-saturation-leak` (new); `wasted-ad-spend-leak`,
  `stockout-ad-spend-leak` (carried over)
- **02-google-shopping (all new):** `feed-zero-impressions-leak`,
  `product-disapproval-leak`, `shopping-product-roas-leak`,
  `branded-search-share-leak`, `price-competitiveness-leak`
- **03-tracking:** `utm-coverage-leak`, `conversion-value-mismatch-leak`,
  `ga4-order-gap-leak`, `google-conversion-action-leak` (new);
  `tracking-gap-leak` (carried over)
- **04-conversion:** `site-search-leak`, `traffic-source-conversion-leak` (new);
  `checkout-drop-leak`, `mobile-conversion-gap-leak`,
  `product-page-conversion-leak` (carried over)
- **05-basket-pricing:** `cross-sell-pair-leak`, `price-change-leak`,
  `markdown-depth-leak` (new); `basket-value-gap-leak`, `discount-leak`
  (carried over)
- **06-retention:** `abandoned-checkout-recovery-leak`,
  `email-flow-coverage-leak`, `lapsed-customer-leak`, `email-list-health-leak`
  (new); `second-order-gap-leak` (carried over)
- **07-profit-ops:** `shipping-cost-recovery-leak`, `dead-stock-leak`,
  `low-margin-sku-leak` (new); `contribution-margin-leak`,
  `refund-and-return-leak` (carried over)
- **08-reporting:** `daily-revenue-pulse`, `monthly-revenue-leak-review`,
  `channel-performance-scorecard`, `leak-fix-tracker` (new);
  `weekly-revenue-leak-readout` (carried over)
- `references/thresholds.md`: 95 keys (30 carried over, 65 new); one
  `[platform]` key (`email.spam_rate_ceiling`, from Google's Gmail sender
  guidelines), all others `[heuristic]`
- `references/shopify-exports.md`: inputs for Meta breakdowns, Google Ads,
  Merchant Center, GA4, email tools, Postmaster Tools and shipping labels
- `AGENTS.md`: the order of checks across all 8 folders and 19 blocking rules
  (8 carried over, 11 new)
- Scripts (standard library only): `feed_zero_impressions.py`,
  `cross_sell_pairs.py`, `price_change.py`, `lapsed_customers.py`,
  `dead_stock.py`, `daily_pulse.py`; `load_rows()` added to `leakkit.py`
- `examples/`: made-up Products, inventory and Google Shopping exports for the
  sample store
- `validate_skills.py`: checks the 8 x 5 layout, the new-skill rules,
  threshold tags and usage, and the launch-post values; `selftest.py`: 20 new
  checks; `build_zips.py`: one ZIP per folder, one full ZIP and
  self-contained skill folders for Claude Code

### Carried over

12 skills from shopify-revenue-leak-skills 1.0.0, unchanged except for their
relative paths (`../` became `../../` for the folder level).

### Notes

Every threshold is at its first default. Expect recalibration in 1.1 as
results from real stores come in.
