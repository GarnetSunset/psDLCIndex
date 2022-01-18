import sys
from pprint import pprint

import requests

store_code_mappings = {
    "de-de": "DE/de",
    "gb-de": "GB/en",
    "se-en": "SE/en",
    "en-us": "US/en",
    "ja-jp": "JP/ja",
}

if len(sys.argv) == 1:
    URL = input(
        "Input the URL of the game you want the DLC for in this format:\nhttps://store.playstation.com/**-**/product/HP0700-CUSA00000_00-0000ENDOFTHEURL0\n>"
    )
elif len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    Exception("No URL provided")

region = URL.split("/")[3]
contentID = URL.split("/")[5]

chihiro_base_url = f"https://store.playstation.com/store/api/chihiro/00_09_000/container/{store_code_mappings[region]}/999/{contentID}?relationship=ADD-ONS%27"
response = requests.get(chihiro_base_url)
item = response.json()
print(chihiro_base_url)

dlcList = {}
for link in item["links"]:
    dlcList[link["name"]] = link["id"]
if dlcList == {}:
    exit("No DLC found")
pprint(dlcList)
