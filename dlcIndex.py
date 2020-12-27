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
URL = 0
EU = "https://store.playstation.com/ru-ru/"
JP = "https://store.playstation.com/ja-jp/"
US = "https://store.playstation.com/en-us/"
HK = "https://store.playstation.com/en-hk/"
RU = "https://store.playstation.com/ru-ru/"

addons = "/1?gameContentType=addons&smcid=psapp"

##UP is for US, EP is for EU, JP is for Japan##

try: input = raw_input
except NameError: pass

if len(sys.argv) == 1:
    userinput = input("Input the CUSAxxxxx, Content_ID or URL of the app you want\nIn the example format of:\nCUSA00000 - for EU store\nCUSA00000j - for JP, u - for US, h - for HK, r - for RU store\nEP0700-CUSA00000_00-0000ENDOFTHECID0\nhttps://store.playstation.com/**-**/product/HP0700-CUSA00000_00-0000ENDOFTHEURL0\n>")
else:
    userinput = sys.argv[1]

if len(userinput) == 9:
    userinput = EU + "product/NP1111-" + userinput + "_00-1111111111111111?smcid=psapp"
    r = requests.get(userinput)
    userinput = r.url
    packageName = userinput[44:80]
    letter = packageName[0]
elif len(userinput) == 10:
    if(userinput[9] == "j"):
        userinput = JP + "product/NP1111-" + userinput[0:9] + "_00-1111111111111111?smcid=psapp"
        letter = "J"
    elif(userinput[9] == "u"):
        userinput = US + "product/NP1111-" + userinput[0:9] + "_00-1111111111111111?smcid=psapp"
        letter = "U"
    elif(userinput[9] == "h"):
        userinput = HK + "product/NP1111-" + userinput[0:9] + "_00-1111111111111111?smcid=psapp"
        letter = "H"
    elif(userinput[9] == "r"):
        userinput = RU + "product/NP1111-" + userinput[0:9] + "_00-1111111111111111?smcid=psapp"
        letter = "R"
    else:
        userinput = EU + "product/NP1111-" + userinput[0:9] + "_00-1111111111111111?smcid=psapp"
        letter = "E"
    r = requests.get(userinput)
    userinput = r.url
    packageName = userinput[44:80]
elif len(userinput) == 36:
    packageName = userinput
    letter = packageName[0]
else:
    packageName = userinput[44:]
    URL = userinput[0:36] + "grid/"
    ProductURL = userinput[0:44]

if URL == 0:
    if(letter == "U"):
        URL = US + "grid/"
        ProductURL = US + "product/"
    elif(letter == "E"):
        URL = EU + "grid/"
        ProductURL = EU + "product/"
    elif(letter == "R"):
        URL = RU + "grid/"
        ProductURL = RU + "product/"
    elif(letter == "H"):
        URL = HK + "grid/"
        ProductURL = HK + "product/"
    else:
        URL = JP + "grid/"
        ProductURL = JP + "product/"

URLfull = URL + packageName + addons
print("Looks like your game is located here:\n" + ProductURL + packageName)
regexp = "\"Product\",\"name\":\"(.*?)\".*?sku\":\"(.*?)\""
r = requests.get(URLfull)
c = r.content
print("Looks like your DLCs are located here:\n" + URLfull)

soup = BeautifulSoup(c, 'lxml')

try:
    pages = str(soup.find('a', {'class': 'paginator-control__end paginator-control__arrow-navigation internal-app-link ember-view'}))
    relationship = pages.index('gameContentType')
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
        r = requests.get(URL+packageName+"/"+str(pageIter)+"?gameContentType=addons&smcid=psapp")
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
