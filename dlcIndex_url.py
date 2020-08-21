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
EU = "https://store.playstation.com/en-gb/"
JP = "https://store.playstation.com/ja-jp/"
US = "https://store.playstation.com/en-us/"
HK = "https://store.playstation.com/en-hk/"
RU = "https://store.playstation.com/ru-ru/"

addons = "/1?relationship=add-ons"

##UP is for US, EP is for EU, JP is for Japan##

try: input = raw_input
except NameError: pass

if len(sys.argv) == 1:
    titleID = input("Input the URL of the app you want\nIn the example format of:\nhttps://store.playstation.com/en-**/product/HP0700-CUSA00000_00-ENDOFTHEURL0\n>")
else:
    titleID = sys.argv[1]

packageName = titleID[44:]
letter = titleID[44]

if(letter == "U"):
    URL = US + "grid/"
    ProductURL = US + "product/"
elif(letter == "E"):
    URL = EU + "grid/"
    ProductURL = EU + "product/"
elif(letter == "H"):
    URL = HK + "grid/"
    ProductURL = HK + "product/"
else:
    URL = JP + "grid/"
    ProductURL = JP + "product/"

URLfull = URL + packageName + addons
regexp = "\"Product\",\"name\":\"(.*?)\".*?sku\":\"(.*?)\""
r = requests.get(URLfull)
c = r.content
print("Looks like your DLCs are located here:\n" + URLfull)

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

# text_file = open(packageName + ".txt", "w")

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
#            text_file.write(ProductURL + DLCID + " | " + Name + "\n")
            os.system("ez_dlc.py " + ProductURL + DLCID)
# text_file.close()
