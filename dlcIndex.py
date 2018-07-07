from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re, os, time

DLCList = []
locationString = 'chromedriver.exe'
JP = "https://store.playstation.com/ja-jp/grid/"
EU = "https://store.playstation.com/en-gb/grid/"
US = "https://store.playstation.com/en-us/grid/"
addons = "/1?relationship=add-ons"

##UP is for US, EP is for EU, JP is for Japan##

titleID = raw_input("Input your title ID\nIn the example format of:\nJP0700-CUSA*****_00-0000000000000000\n>")

CUSA = titleID[7:16]

letter = titleID[0]

if(letter == "U"):
    URL = US
elif(letter == "E"):
    URL = EU
else:
    URL = JP

URLfull = URL + titleID + addons

driver = webdriver.Chrome()
driver.get(URLfull)

requestRec = driver.page_source

soup = BeautifulSoup(requestRec, 'lxml')

for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
    if "product" in link.get('href') and CUSA in link.get('href'):
        DLCList.append(link.get('href'))

text_file = open(titleID + ".txt", "w")

for i in DLCList:
    productLocation = i.index('product')
    DLCID = i[productLocation+8:]
    text_file.write(DLCID + "\n")

text_file.close()

driver.close()

if os.name == 'nt':
    os.system('taskkill /f /im chromedriver.exe')
