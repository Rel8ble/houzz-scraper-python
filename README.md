# Houzz scraper in Python: export contractor, designer and home-service leads to CSV

Get Houzz professionals (general contractors, plumbers, interior designers, architects, landscapers, roofers and 70+ other categories, US and Canada) as JSON or CSV with a few lines of Python: name, star rating, review count, phone, address, cost estimate, sponsored flag, verified license and profile URL.

> Disclosure: I built this actor; it's a paid tool on Apify ([rel8ble/houzz-professionals-scraper](https://apify.com/rel8ble/houzz-professionals-scraper)), **$0.90 per 1,000 businesses, no start fee**. Apify's free plan credit covers small runs.

## Quick start

```bash
pip install -r requirements.txt
export APIFY_TOKEN=<YOUR_APIFY_TOKEN>   # console.apify.com/settings/integrations
python example.py
```

`example.py` searches 2 categories x 2 cities, writes `houzz_leads.csv`, counts sponsored and unreviewed businesses, and prints a prospect shortlist: 4.5+ stars, fewer than 15 reviews, not advertising yet (a typical list for a marketing or review-generation agency).

### Minimal call

```python
from apify_client import ApifyClient

client = ApifyClient("<YOUR_APIFY_TOKEN>")
run = client.actor("rel8ble/houzz-professionals-scraper").call(run_input={
    "categories": ["general contractors"],
    "locations": ["Charlotte, NC"],
})
for biz in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(biz["name"], biz["rating"], biz["phone"])
```

### Node.js

```js
import { ApifyClient } from 'apify-client';
const client = new ApifyClient({ token: '<YOUR_APIFY_TOKEN>' });
const run = await client.actor('rel8ble/houzz-professionals-scraper').call({
  categories: ['plumbers'], locations: ['Austin, TX'],
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items.length, items[0]);
```

## Input

| Field | Example | Notes |
|---|---|---|
| `categories` | `["general contractors", "plumbers"]` | Houzz categories; unknown names are skipped and reported, not charged |
| `locations` | `["Charlotte, NC", "28277", "Toronto, ON"]` | City, ST / US ZIP / Canadian city; 50-mile radius |
| `keywords` | `["kitchen remodel"]` | optional free-text search inside each category + location |
| `minRating` | `"4"` | `"0"` (any, default), `"3"`, `"4"`, `"5"` |
| `priceLevels` | `["$$$", "$$$$"]` | optional |
| `includeDetails` | `true` | adds website, licence number and services (slower) |
| `maxResults` | `200` | cap on businesses saved |

## Real output (20-business sample run, 20 Oct 2026: Charlotte contractors, Texas designers, Toronto-area plumbers)

```json
{
  "name": "Viro Builders LLC",
  "category": "General Contractors",
  "rating": 5,
  "reviewCount": 2,
  "costEstimate": "$10,000 - 250,000",
  "phone": "(980) 552-5981",
  "address": "9402 huey blvd",
  "city": "waxhaw",
  "state": "NC",
  "postalCode": "28173",
  "sponsored": true,
  "verifiedLicense": false,
  "projectCount": 6,
  "profileUrl": "https://www.houzz.com/professionals/general-contractors/viro-builders-llc-pfvwus-pf~727042406"
}
```

In that sample all 20 businesses had a phone number, 19 were rated and 5 were sponsored listings. `example.py`'s shortlist on it (4.5+ stars, under 15 reviews, not sponsored) kept 9:

| name | rating | reviews | city |
|---|---|---|---|
| Conservation Renovations Inc. | 4.7 | 13 | Charlotte, NC |
| Cameron Getter Design | 4.9 | 8 | Lakeway, TX |
| JM Customs & Restorations | 5 | 14 | Charlotte, NC |
| Parksdale Building Co. | 5 | 5 | Monroe, NC |
| Drain King Plumbers | 5 | 2 | Toronto, ON |

## Pricing and limits

- $0.90 per 1,000 businesses, no start fee; failed or skipped searches are not charged.
- Business listing data only: no reviews or reviewer names.
- Houzz's search radius is fixed at 50 miles around a place.

## Related

- [yellowpages-scraper-python](https://github.com/Rel8ble/yellowpages-scraper-python): US business leads from YellowPages
- [bbb-scraper-python](https://github.com/Rel8ble/bbb-scraper-python): Better Business Bureau ratings and accreditation
- [website-contact-scraper-python](https://github.com/Rel8ble/website-contact-scraper-python): emails and socials from the websites you collect

MIT licensed.
