All credits goes to [GarnetSunset](https://github.com/GarnetSunset) for [original script](https://github.com/GarnetSunset/psDLCIndex), [Maxton](https://github.com/maxton) for [LibOrbisPkg](https://github.com/maxton/LibOrbisPkg) and [TheRadziu](https://github.com/TheRadziu) for [Easy Fake DLC / DLC without Extra Data Generator](https://gist.github.com/TheRadziu/b7321fdf2672197d14b87eeb2a5bd919)!

Adding stuff|bugs to the code - [DeniZz](https://github.com/krugdenis)

# psDLCIndex
Playstation Store DLC indexer, and package generator.

## What is this?
This is a script that will go through a playstation store entry for a certain title, which is given at runtime, 
and get the titleIDS of all DLC associated with them. 

## How to use?
You can pass the URL of the software you're trying to generate for example:

```python dlcIndex.py https://store.playstation.com/en-us/product/UP0177-CUSA13186_00-JUDGMENTRYUGAENG```

### Reminder!

This script can only create flags for DLC that are empty DLCs. 
If your DLC contains data, it will not work. 