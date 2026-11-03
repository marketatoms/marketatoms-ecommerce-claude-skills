# Where each input comes from

Every skill in this library works from something you can download or copy in a
few minutes. Nothing here logs into your store or your ad accounts. Shopify
renames reports from time to time; if a name below doesn't match your admin,
look for the report with the same columns.

If the **MarketAtoms MCP** is connected to Claude, several of these inputs are
read live instead (see each skill's "Live data" section). You never need both.

## Orders export

**Where:** Shopify admin > **Orders** > **Export** > choose the date range >
"Export orders" as CSV (plain CSV or CSV for Excel).

**Used by:** second-order gap, discount leak, refund and return leak, tracking
gap, basket value gap, contribution margin, weekly readout, cross-sell pairs,
price change, lapsed customers, dead stock, shipping cost recovery, daily
pulse, GA4 order gap.

**Columns this pack reads:** `Name` (order number), `Email`, `Financial Status`,
`Currency`, `Subtotal`, `Shipping`, `Total`, `Discount Code`, `Discount Amount`,
`Created at`, `Lineitem quantity`, `Lineitem name`, `Lineitem price`,
`Lineitem sku`, `Cancelled at`, `Refunded Amount`, `Source`.

**Read this before using it:**

- The export has **one row per line item**. An order with 3 products has 3
  rows; the order-level columns (`Total`, `Discount Code`, `Refunded Amount`,
  ...) are filled only on the first row. The scripts handle this; if you read
  the CSV by eye, count orders by unique `Name`, not by rows.
- `Created at` is in the store's time zone. Ad platforms may report in another
  time zone; line the dates up before comparing.
- `Source` is the **sales channel** (web, pos, shopify_draft_order, an app),
  not the ad that drove the order. Use Shopify Analytics' "Sales attributed to
  marketing" for channel attribution.
- Exclude test orders and cancelled orders (`Cancelled at` not empty).

## Products and inventory exports

**Products:** Shopify admin > **Products** > **Export** > CSV. Reads `Handle`,
`Title`, `Variant SKU`, `Variant Price`, `Status`.

**Inventory:** Shopify admin > **Products** > **Inventory** > **Export** > CSV.
Reads `SKU` and the `Available` quantity per location (sum the locations that
fulfil online orders).

The Products export also has `Variant Compare At Price` and `Cost per item`
(filled only if the store enters costs in Shopify).

**Used by:** stock-out ad spend, dead stock, markdown depth, low-margin SKU.

## Shopify Analytics reports

**Where:** Shopify admin > **Analytics** > **Reports**. Set the date range,
then export as CSV or copy the table.

| Report (search for it by name) | Columns needed | Used by |
| --- | --- | --- |
| Conversion rate breakdown / online store conversion over time | sessions, sessions with cart additions, sessions reaching checkout, sessions converted | checkout drop |
| Sessions by device type (with conversion) | device type, sessions, sessions converted | mobile conversion gap |
| Product analytics / product views and add-to-carts | product title, product views (or sessions with product views), add-to-carts | product page conversion |
| Sales attributed to marketing / sales by referrer | channel or referrer, orders, sales | tracking gap |
| Sales by product | product title, net quantity, net sales | stock-out ad spend, contribution margin |

## Ad platform reports

**Meta Ads Manager:** Ads Manager > choose **Ad sets** (or Campaigns) > set the
date range > **Reports** > **Export table data** (CSV). Include the columns
Ad set name, Amount spent, Purchases, Purchases conversion value, Starts (or
the ad set's start date) and Website URL of the ads if you have it.
Note the **attribution setting** shown in the column header (for example
"7-day click or 1-day view").

**Google Ads:** Campaigns report or Search terms report > **Download** > CSV.
Columns: Campaign / Search term, Cost, Conversions, Conv. value. Note which
conversion action is counted.

**Used by:** tracking gap, wasted ad spend, stock-out ad spend, contribution
margin, weekly readout.

## More Shopify reports

| Report | Where | Columns needed | Used by |
| --- | --- | --- | --- |
| Abandoned checkouts | Shopify admin > **Orders** > **Abandoned checkouts** > **Export** | checkout date, email present, total | abandoned checkout recovery |
| Online store searches, and searches with no results | **Analytics** > **Reports**, search "online store searches" | search query, searches | site search |
| Sales attributed to marketing / sessions by referrer or UTM | **Analytics** > **Reports** | channel or source, sessions, orders, sales | UTM coverage, traffic-source conversion, conversion value mismatch, Google conversion action, channel scorecard |

## Meta Ads Manager breakdowns

Same export as above (**Reports** > **Export table data**), with a breakdown
added first:

- **By time > Week** at **Ads** level: creative fatigue (Frequency, Link
  clicks, CTR (link click-through rate)).
- **By time > Week** at **Ad sets** level: audience saturation (Reach,
  Frequency, CPM).
- **By delivery > Placement**: placement spend.
- For UTM coverage, add the "Website URL" and "URL parameters" columns.

## Google Ads and Merchant Center

| Report | Where | Columns needed | Used by |
| --- | --- | --- | --- |
| Products | Google Ads > **Campaigns** > **Products** > **Download** | Item ID, Product title, Impr., Clicks, Cost, Conversions, Conv. value | feed zero impressions, shopping product ROAS, price competitiveness |
| Search terms | **Insights and reports** > **Search terms** > **Download** | Search term, Campaign, Cost, Conversions, Conv. value | wasted ad spend, branded search share |
| Conversion actions | **Goals** > **Conversions** > **Summary** > download | Conversion action, Action optimization, Source, Count, Category, Conversions | Google conversion action |
| Product list with status | Merchant Center > **Products** > **Download** | Item ID, Title, Status, Issue, Availability | product disapproval, feed zero impressions |
| Price competitiveness | Merchant Center > price competitiveness report (under Performance or Analytics, depending on version) | Item, your price, benchmark price | price competitiveness |

## Google Analytics 4

Reports > **Monetization** > **Ecommerce purchases**, or an Exploration with
Transactions and Purchase revenue by date. Check the property's time zone
against the store's. **Used by:** GA4 order gap.

## Email tool (Klaviyo or similar)

| Data | Where (Klaviyo) | Used by |
| --- | --- | --- |
| Flows list with status and trigger | **Flows** | email flow coverage |
| Flow performance (recipients, orders, revenue) | the flow's **Analytics**, or a flow performance report | abandoned checkout recovery, email flow coverage |
| Campaign results (recipients, delivered, bounced, unsubscribes, clicks) | **Campaigns**, export or a campaign performance report | email list health |
| Flow vs campaign revenue | analytics dashboard or a custom report | email flow coverage |

Omnisend, Mailchimp and Shopify Email report the same numbers under similar
names; say which tool the numbers came from. Open rates are not used anywhere
in this library: mail privacy features inflate them.

**Google Postmaster Tools** (for a verified sending domain): daily Gmail spam
rate. **Used by:** email list health.

## Shipping label costs

Shopify Shipping label charges (Shopify admin > **Settings** > **Billing**), a
shipping app's export (for example ShipStation or Sendcloud) or the carrier
invoice: label cost per order or a total for the period, with returns labels
separate. **Used by:** shipping cost recovery, contribution margin.

## Store settings you type in

Some checks need a number only you know. The skill asks for it:

- **Free-shipping threshold** (basket value gap)
- **Target cost per purchase** (wasted ad spend, channel scorecard)
- **Target ROAS** (shopping product ROAS)
- **Brand terms** - the store's name and its misspellings (branded search share)
- **Existing bundles and cart suggestions** (cross-sell pairs)
- **Date and product of a price change**, or of a fix (price change, leak-fix tracker)
- **Cost of goods** per product or as an average % of price, **shipping cost**
  per order, **payment fee** rate (contribution margin)
