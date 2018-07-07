from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, re, sys, time

DLCList = []
locationString = 'chromedriver.exe'
JP = "https://store.playstation.com/ja-jp/"
EU = "https://store.playstation.com/en-gb/"
US = "https://store.playstation.com/en-us/"
addons = "/1?relationship=add-ons"

reload(sys)
sys.getdefaultencoding()

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

driver = webdriver.Chrome()
driver.get(URLfull)
requestRec = driver.page_source

soup = BeautifulSoup(requestRec, 'lxml')

for link in soup.findAll('a', attrs={'href': re.compile("^https://")}):
    if "product" in link.get('href') and CUSA in link.get('href'):
        DLCList.append(link.get('href'))

rights = soup.findAll('div', {'class': 'grid-cell__title'})

text_file = open(titleID + ".txt", "w")

for i in DLCList:
    for j in rights:
        productLocation = i.index('product')
        DLCID = i[productLocation+8:]
        string = str(j)
        text_file.write(DLCID + "\n" + string.strip() + "\n")
        time.sleep(5)

text_file.close()

driver.close()

if os.name == 'nt':
    os.system('taskkill /f /im chromedriver.exe')
