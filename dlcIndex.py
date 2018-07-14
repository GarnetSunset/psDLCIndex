from bs4 import BeautifulSoup
import os, re, requests, time

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
JP = "https://store.playstation.com/ja-jp/"
EU = "https://store.playstation.com/en-gb/"
US = "https://store.playstation.com/en-us/"
addons = "/1?relationship=add-ons"

##UP is for US, EP is for EU, JP is for Japan##

try: input = raw_input
except NameError: pass

titleID = input("Input your title ID\nIn the example format of:\nJP0700-CUSA*****_00-0000000000000000\n>")

CUSA = titleID[7:16]

letter = titleID[0]

if(letter == "U"):
    URL = US + "grid/"
    ProductURL = US + "product/"
elif(letter == "E"):
    URL = EU + "grid/"
    ProductURL = EU + "product/"
else:
    URL = JP + "grid/"
    ProductURL = JP + "product/"

URLfull = URL + titleID + addons

regexp = "\"Product\",\"name\":\"(.*?)\".*?sku\":\"(.*?)\""
r = requests.get(URLfull)
c = r.content

soup = BeautifulSoup(c, 'lxml')

try:
    pages = str(soup.find('a', {'class': 'paginator-control__end paginator-control__arrow-navigation internal-app-link ember-view'}))
    relationship = pages.index('relationship')
    titleURL = pages.index(titleID)
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
        r = requests.get(URL+titleID+"/"+str(pageIter)+"?relationship=add-ons")
        c = r.content
        soup = BeautifulSoup(c, 'lxml')
        time.sleep(2)

DLCList = Remove(DLCList)

text_file = open(titleID + ".txt", "w")

for item in DLCList:
    for small in item:
        if DLCIter == 0:
            Name = small
            DLCIter += 1
            NameID = Name.encode('utf-8').strip()
        else:
            DLCID = small
            DLCIter = 0
            DLCID = DLCID.encode('utf-8').strip()
        if DLCIter == 0:
            text_file.write(DLCID + " | " + NameID + "\n")

text_file.close()
