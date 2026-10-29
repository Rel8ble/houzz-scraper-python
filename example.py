"""Houzz contractor leads -> CSV + a quick prospect shortlist.

pip install -r requirements.txt
APIFY_TOKEN=<YOUR_APIFY_TOKEN> python example.py
"""
import csv
import os
import sys

from apify_client import ApifyClient

TOKEN = os.environ.get("APIFY_TOKEN", "<YOUR_APIFY_TOKEN>")
ACTOR = "rel8ble/houzz-professionals-scraper"

run_input = {
    "categories": ["general contractors", "plumbers"],
    "locations": ["Charlotte, NC", "Austin, TX"],
    "minRating": "0",
    "maxResults": 200,
}

FIELDS = ["name", "category", "rating", "reviewCount", "phone", "address",
          "city", "state", "postalCode", "costEstimate", "sponsored",
          "verifiedLicense", "projectCount", "profileUrl"]


def summarize(rows):
    with open("houzz_leads.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)} businesses -> houzz_leads.csv")
    print(f"sponsored (already pay for ads): {sum(1 for r in rows if r.get('sponsored'))}")
    print(f"no reviews yet: {sum(1 for r in rows if not r.get('reviewCount'))}")

    # Prospects for a marketing agency: well rated, few reviews, not advertising yet
    shortlist = [r for r in rows
                 if (r.get("rating") or 0) >= 4.5
                 and 0 < (r.get("reviewCount") or 0) < 15
                 and not r.get("sponsored")]
    shortlist.sort(key=lambda r: -(r.get("projectCount") or 0))
    print("\nshortlist (4.5+ stars, <15 reviews, not sponsored):")
    for r in shortlist[:15]:
        print(f"  {r['name']:<40} {r.get('rating')}* {r.get('reviewCount')} reviews  "
              f"{r.get('phone') or '-'}  {r.get('city')}, {r.get('state')}")


def main():
    if TOKEN.startswith("<"):
        sys.exit("Set APIFY_TOKEN first (console.apify.com/settings/integrations).")
    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input=run_input)
    summarize(list(client.dataset(run["defaultDatasetId"]).iterate_items()))


if __name__ == "__main__":
    main()
