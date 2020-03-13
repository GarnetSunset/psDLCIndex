# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import datetime, errno, os, os.path, re, requests, shutil, subprocess, sys, time

try: input = raw_input
except NameError: pass

dragNDrop = ""

def genPKG(CID, pkgName):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    gen_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        contentid = CID
        name = pkgName
        titleid = contentid[7:16]
    except:
        print("Usage: {} {} {}".format(sys.argv[0], 'DLC_CID', '\"DLC_NAME\"'))
        sys.exit(2)

    if not os.path.exists('orbis-pub-cmd.exe'):
        print("File \'orbis-pub-cmd.exe\' is missing from current directory!!")
        sys.exit(2)
        
    if len(contentid) != 36:
        print("DLC CID IS TOO LONG OR TOO SHORT, IT HAS TO BE 36 CHARACTERS LONG, FOR EXAMPLE 'UP9000-CUSA00900_00-SPEXPANSIONDLC03'")
        sys.exit(2)

    SFX_template = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <paramsfo>
     <param key="ATTRIBUTE">0</param>
     <param key="CATEGORY">ac</param>
     <param key="CONTENT_ID">%s</param>
     <param key="FORMAT">obs</param>
     <param key="TITLE">%s</param>
     <param key="TITLE_ID">%s</param>
     <param key="VERSION">01.00</param>
    </paramsfo>)""" % (contentid, name, titleid)

    GP4_template = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
    <psproject fmt="gp4" version="1000">
      <volume>
        <volume_type>pkg_ps4_ac_nodata</volume_type>
        <volume_id>PS4VOLUME</volume_id>
        <volume_ts>%s</volume_ts>
        <package content_id="%s" passcode="00000000000000000000000000000000"/>
      </volume>
      <files img_no="0">
        <file targ_path="sce_sys/param.sfo" orig_path="%s\\fake_dlc_temp\sce_sys\param.sfo"/>
      </files>
      <rootdir>
        <dir targ_name="sce_sys"/>
      </rootdir>
    </psproject>""" % (gen_time, contentid, current_dir)

    x = safe_open_w('fake_dlc_temp/param_template.sfx')
    x.write(SFX_template)
    x.close()
    x = safe_open_w('fake_dlc_temp/fake_dlc_project.gp4')
    x.write(GP4_template)
    x.close()

    mkdir_p(os.path.dirname('fake_dlc_temp/sce_sys/'))
    if os.path.isdir("fake_dlc_pkg"):
        pass
    else:
        os.mkdir('fake_dlc_pkg')

    subprocess.check_call(['orbis-pub-cmd.exe', 'sfo_create', 'fake_dlc_temp\param_template.sfx', 'fake_dlc_temp\sce_sys\param.sfo'])

    subprocess.check_call(['orbis-pub-cmd.exe', 'img_create', '%s\\fake_dlc_temp\\fake_dlc_project.gp4' % current_dir, '%s\\fake_dlc_pkg\%s-A0000-V0100.pkg' % (current_dir, contentid)])

    shutil.rmtree('fake_dlc_temp')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

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
HK = "https://store.playstation.com/en-hk/"
addons = "/1?relationship=add-ons"

##UP is for US, EP is for EU, JP is for Japan##

try: input = raw_input
except NameError: pass

if len(sys.argv) == 1:
    titleID = input("Input the URL of the app you want\nIn the example format of:\nhttps://store.playstation.com/en-**/product/HP0700-CUSA00000_00-ENDOFTHEURL0\n>")
else:
    titleID = sys.argv[1]

CUSA = titleID[51:60]
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

soup = BeautifulSoup(c, 'lxml')

try:
    pages = str(soup.findall('a', {'class': 'internal-app-link ember-view'}))
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
    lets = open('flair.txt', 'r')
    lain = lets.read()
    print(lain)
    lets.close()
    
for item in DLCList:
    for small in item:
        if DLCIter == 0:
            Name = small
            DLCIter += 1
        else:
            DLCID = small
            DLCIter = 0
        if DLCIter == 0:
            genPKG(DLCID, Name.encode('utf-8'))