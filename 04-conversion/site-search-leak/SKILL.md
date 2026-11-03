---
name: site-search-leak
description: Finds what shoppers search for on the store and don't find - the share of on-site searches with no results and the specific terms behind them - so missing products, synonyms and spelling variants can be fixed. Use when search is used a lot, after adding or renaming products, or in a CRO review. Boundary: product-page-conversion-leak covers shoppers who found a product and didn't add it; this skill covers shoppers who never found one.
---

# Site Search Leak

Thresholds: `../../references/thresholds.md` (or `references/thresholds.md` in a
single-skill download). Inputs: `../../references/shopify-exports.md`.

## Use this skill when

- "What are people looking for that I don't have (or that they can't find)?"
- After renaming products or changing the catalogue.
- CRO review: search is often used by the shoppers closest to buying.

## Required input

- **Shopify search reports:** Shopify admin > **Analytics** > **Reports** >
  search for "online store searches" - the report of top searches and the
  report of top searches **with no results** > same date range > export (or
  copy the tables). Columns: search query, searches.
- The total number of searches in the period (from the first report).
- If a search app replaces Shopify search, use that app's "no results" report
  instead and say which.

## Live data (MarketAtoms MCP)

No live tool reads search reports yet. Use the export.

## Analysis workflow

1. Total searches. Under `search.min_searches`: `needs_data` for the share
   (terms can still be listed).
2. No-results share = searches with no results / all searches.
3. List no-results terms with at least `search.min_term_searches`, ranked by
   searches.
4. Classify each, from the term and the catalogue only:
   - **synonym** - the store sells it under another name (searched "swaddle",
     product is "Muslin Wrap");
   - **spelling** - a misspelling or plural of a product name;
   - **missing** - nothing in the catalogue matches: demand the store doesn't serve;
   - **non-product** - "returns", "discount code", "shipping".
5. Non-product terms go to a separate list: they point at navigation or FAQ,
   not search.

## Decision rules

- No-results share >= `search.no_result_share_flag`: `leak`.
- Each term at or above `search.min_term_searches` is listed with its class;
  synonym and spelling terms are fixable without new products.
- `missing` terms are demand signals for the owner to judge, not instructions
  to stock something.
- Share under the flag: `ok`, still list the top terms.
- Under `search.min_searches`: `needs_data` for the share.

## Output format

Summary line: total searches, no-results share, terms listed.

| Search term | Searches | No results | Class | Suggested fix |
|---|---|---|---|---|

Then: **Non-product searches**, **Below the term minimum** (count only),
**Approval needed** (catalogue and search-setting changes are the owner's).

## Practical example

*Made-up numbers for illustration.* 28 days, 2,400 searches, 312 with no
results: 13.0%, over the 10% flag: `leak`.

| Term | Searches | Class | Suggested fix |
|---|---|---|---|
| swaddle | 64 | synonym | Add "swaddle" to the Muslin Wrap title or tags |
| night light | 41 | missing | Demand signal: 41 searches in 28 days |
| sleep sack | 26 | synonym | The Bamboo Sleep Bag is the match |

These three terms are 131 of the 312 no-result searches. "teether" (12
searches) is under the 20-search minimum and is counted, not listed.

## Guardrails

- Never edit products, tags, search settings or apps.
- Don't treat a `missing` term as proof of profitable demand; it is a count of
  searches.
- Don't list personal data typed into the search box (emails, names, order numbers).
