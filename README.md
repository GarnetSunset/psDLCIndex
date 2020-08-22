All credits goes to [GarnetSunset](https://github.com/GarnetSunset) for [original script](https://github.com/GarnetSunset/psDLCIndex), [Maxton](https://github.com/maxton) for [LibOrbisPkg](https://github.com/maxton/LibOrbisPkg) and [TheRadziu](https://github.com/TheRadziu) for [Easy Fake DLC / DLC without Extra Data Generator](https://gist.github.com/TheRadziu/b7321fdf2672197d14b87eeb2a5bd919)!

Adding stuff|bugs to the code - [DeniZz](https://github.com/krugdenis)

# psDLCIndex
Playstation Store DLC Indexer, and list generator.

## What is this?
This is a script that will go through a playstation store entry for a certain title, which is given at runtime, and get the titleIDS of all DLC associated with them. 

## How to use?
Make sure you run "requirements.bat" if you're on windows, but then, just run the "dlcIndex.py" script and input the Full URL or Content_ID or CUSAxxxxx of the app you wish to crawl. This can take a while so be patient.

By default CUSAxxxxx indexing is using EU-region of playstation store. If you want to get DLC for another region, type letter 'j' for JP, 'u' for US, 'r' for RU and 'h' for HK at the end of CUSAxxxxx, e.g.: CUSA00000j, CUSA00000u, CUSA00000r, CUSA00000h