# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import datetime, errno, os, os.path, re, requests, shutil, subprocess, sys, time

try: input = raw_input
except NameError: pass

dragNDrop = ""

def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

DLCList = []
DLCIter = 0
pageIter = 0
pageNums = 2
US = "https://store.playstation.com/en-us/"

addons = "/1?relationship=add-ons"

try: input = raw_input
except NameError: pass

if len(sys.argv) == 1:
    titleID = US + "product/NP1111-" + input("Input the CUSAXXXXX of the app you want\nIn the example format of:\nCUSA00000\n>") + "_00-1111111111111111"
else:
    titleID = US + "product/NP1111-" + sys.argv[1] + "_00-1111111111111111"

r = requests.get(titleID)
titleID = r.url
print("Looks like your game is located here:\n" + titleID)
packageName = titleID[44:]

URL = US + "grid/"
ProductURL = US + "product/"

URLfull = URL + packageName + addons
regexp = "\"Product\",\"name\":\"(.*?)\".*?sku\":\"(.*?)\""
r = requests.get(URLfull)
c = r.content

soup = BeautifulSoup(c, 'lxml')

try:
    pages = str(soup.find('a', {'class': 'paginator-control__end paginator-control__arrow-navigation internal-app-link ember-view'}))
    relationship = pages.index('relationship')
    titleURL = pages.index(packageName)
    pageNums = int(pages[titleURL+37:relationship-1])
    pageNums = pageNums + 1
except:
    pass

if(pageIter == pageNums):
    pattern = re.findall(regexp, r.text)
    for item in pattern:
        DLCList.append(item)   
else:
    while(pageIter != pageNums):
        pageIter += 1
        pattern = re.findall(regexp, r.text)
        for item in pattern:
            DLCList.append(item)
        r = requests.get(URL+packageName+"/"+str(pageIter)+"?relationship=add-ons")
        c = r.content
        soup = BeautifulSoup(c, 'lxml')
        time.sleep(2)

DLCList = Remove(DLCList)

if DLCList:
    print("Making fake DLCs!!!")
else:
    print("No DLC for this app, mate")
    
for item in DLCList:
    for small in item:
        if DLCIter == 0:
            Name = small
            DLCIter += 1
        else:
            DLCID = small
            DLCIter = 0
        if DLCIter == 0:
            os.system("ez_dlc.py " + ProductURL + DLCID)
