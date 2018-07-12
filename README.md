# psDLCIndex
Playstation Store DLC Indexer, and list generator.

## What is this?
 
This is a script that will go through a playstation store entry for a certain title, which is given at runtime, and get the 
titleIDS of all DLC associated with them. This can then be funnelled into "mysteriouslink.py" which can parse it out and, using some outside programs, generate some cool pkgs. 

## How to use?

Make sure you run "requirements.bat" if you're on windows, but then, just run the "dlcIndex.py" script and input the full title ID of the 
app you wish to crawl. This can take a while so be patient. 

When done, make sure to run mysteriouslink, with all the files required, which I can't link, in this directory. You should have a bunch of PKGs. 
