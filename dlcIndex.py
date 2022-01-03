import sys

try:
    input = raw_input
except NameError:
    pass

store_code_mappings = {
    "DE/de": ["de-de", "E"],
    "NL/nl": ["nl-nl", "E"],
    "US/en": ["us-en", "U"],
    "JP/jp": ["jp-jp", "J"],
}

# https://store.playstation.com/en-us/product/UP0177-CUSA27065_00-9569812838891386

if len(sys.argv) == 1:
    URL = input(
        "Input the URL of the game you want the DLC for in this format:\nhttps://store.playstation.com/**-**/product/HP0700-CUSA00000_00-0000ENDOFTHEURL0\n>"
    )

region = URL.split("/")[3]
contentID = URL.split("/")[5]
print(contentID)
