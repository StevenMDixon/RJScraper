import requests
import time
import json
import os

BASE_URL = "https://www.retrojunk.com/api/content/promo-endpoints/v1/commercials"
SEARCHURL = "https://www.retrojunk.com/api/content/promo-endpoints/v1/commercials/search"

config = {}

with open('config.json', 'r') as f:
    config = json.load(f)

useSearchMode = True if config["query"] != "" else False

params = {
    "itemsPerPage": 1000,
    "sortColumn": "DateAdded",
    "sortOrder": "Desc",
    "categoryId": config["categoryId"],
    "yearStart": config["yearStart"],
    "yearEnd": config["yearEnd"],
}

if useSearchMode:
    params = {
        "query": config["query"],
        "decade": config["decade"]
    }

print("Fetching first page to determine total pages...")
params["page"] = 1
response = requests.get(SEARCHURL if useSearchMode else BASE_URL, params=params)
response.raise_for_status()
data = response.json()

page_count = data.get("pageCount", 1)
print(f"Total pages: {page_count}")

mp4_links = set()
id_name_map = {}

for page in range(1, page_count + 1):
    print(f"Fetching page {page} of {page_count}...")
    params["page"] = page

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    for item in data.get("items", []):
        item_id = item.get("id")
        name = item.get("title")
        yearAired = item.get("yearFirstAired")
        mp4 = item.get("mp4Uri")
        linkid = mp4.split("/")[-1].replace(".mp4", "")
        print(linkid)
        print(name)
        if mp4:
            mp4_links.add(mp4)

        if linkid and name:
            id_name_map[linkid] = name + " " + str(yearAired)

    time.sleep(0.5)  # be polite

outputLinksLoc = os.path.join(config["fileLocation"], config["linksFile"])
with open(outputLinksLoc, "w", encoding="utf-8") as f:
    for link in sorted(mp4_links):
        f.write(link + "\n")

outputTitleMapLoc = os.path.join(config["fileLocation"], config["OutputTitleFile"])
with open(outputTitleMapLoc, "w", encoding="utf-8") as f:
    json.dump(id_name_map, f, indent=2)

print(f"\nDone!")
print(f"Saved {len(mp4_links)} unique mp4 links.")
print(f"Saved {len(id_name_map)} id->name mappings.")