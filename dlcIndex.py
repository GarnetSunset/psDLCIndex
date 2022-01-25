import sys
from datetime import datetime
from os import makedirs, system
from shutil import rmtree
from tkinter import filedialog
from urllib.request import urlretrieve

import requests as requests


def gen_gp4(content_name, full_id, pkg_location):
    gp4_template = """<?xml version="1.0"?>
        <psproject xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" fmt="gp4" version="1000">
          <volume>
            <volume_type>pkg_ps4_ac_data</volume_type>
            <volume_ts>%s</volume_ts>
            <package content_id="%s" passcode="00000000000000000000000000000000" entitlement_key="00000000000000000000000000000000" />
          </volume>
          <files img_no="0">
            <file targ_path="sce_sys/icon0.png" orig_path="sce_sys\icon0.png" />
            <file targ_path="sce_sys/param.sfo" orig_path="sce_sys\param.sfo" />
          </files>
          <rootdir>
            <dir targ_name="sce_sys" />
          </rootdir>
        </psproject>""" % (
        gen_time,
        full_id,
    )

    makedirs(f"{pkg_location}/{full_id[7:16]}", exist_ok=True)
    makedirs("fake_dlc_temp/sce_sys", exist_ok=True)

    x = open("fake_dlc_temp/fake_dlc_project.gp4", "w")
    x.write(gp4_template)
    x.close()

    urlretrieve("https://i.imgur.com/JeaTFEX.png", "fake_dlc_temp/sce_sys/icon0.png")
    system("PkgTool.exe sfo_new fake_dlc_temp\sce_sys\param.sfo")
    system(
        "PkgTool.exe sfo_setentry --value 0x00000000 --type integer --maxsize 4 fake_dlc_temp\sce_sys\param.sfo ATTRIBUTE"
    )
    system(
        "PkgTool.exe sfo_setentry --value ac --type utf8 --maxsize 4 fake_dlc_temp\sce_sys\param.sfo CATEGORY"
    )
    system(
        "PkgTool.exe sfo_setentry --value "
        + full_id
        + " --type utf8 --maxsize 48 fake_dlc_temp\sce_sys\param.sfo CONTENT_ID"
    )
    system(
        "PkgTool.exe sfo_setentry --value obs --type utf8 --maxsize 4 fake_dlc_temp\sce_sys\param.sfo FORMAT"
    )
    system(
        'PkgTool.exe sfo_setentry --value "'
        + content_name
        + '" --type utf8 --maxsize 128 fake_dlc_temp\sce_sys\param.sfo TITLE'
    )
    system(
        "PkgTool.exe sfo_setentry --value "
        + full_id[7:16]
        + " --type utf8 --maxsize 12 fake_dlc_temp\sce_sys\param.sfo TITLE_ID"
    )
    system(
        "PkgTool.exe sfo_setentry --value 01.00 --type utf8 --maxsize 8 fake_dlc_temp\sce_sys\param.sfo VERSION"
    )


URL = None
pkg_location = "fake_dlc_pkg"

store_code_mappings = {
    "de-de": "DE/de",
    "gb-de": "GB/en",
    "se-en": "SE/en",
    "en-us": "US/en",
    "ja-jp": "JP/ja",
}

if len(sys.argv) < 2:
    try:
        import tkinter as tk

        root = tk.Tk()
        root.title("DLC Indexer")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{int(screen_width / 4)}x{int(screen_height / 8)}")
        lbl = tk.Label(
            root,
            text="Input the URL of the game you want the DLC for in this "
            "format:\nhttps://store.playstation.com/**-**/product/HP0700-CUSA00000_00"
            "-0000ENDOFTHEURL0",
        )
        lbl.pack()

        def get_url():
            global URL
            URL = text_input_field.get(1.0, "end-1c")
            root.destroy()

        text_input_field = tk.Text(root, height=1, width=20)
        text_input_field.pack()
        printButton = tk.Button(root, text="Next", command=get_url)
        printButton.pack()
        root.mainloop()
        root = tk.Tk()
        root.withdraw()
        root.update()
        pkg_location = filedialog.askdirectory(
            title="Select the directory where you want the DLCs to be stored"
        )
        root.destroy()

    except ModuleNotFoundError:
        print("No tkinter found, proceeding in text only mode")


if len(sys.argv) == 1 and URL is None:
    URL = input(
        "Input the URL of the game you want the DLC for in this "
        "format:\nhttps://store.playstation.com/**-**/product/HP0700-CUSA00000_00-0000ENDOFTHEURL0\n> "
    )
elif len(sys.argv) > 1:
    URL = sys.argv[1]
elif URL is not None:
    pass
else:
    exit("No URL provided")

gen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
region = URL.split("/")[3]
content_id = URL.split("/")[5]

chihiro_base_url = f"https://store.playstation.com/store/api/chihiro/00_09_000/container/{store_code_mappings[region]}/999/{content_id}?relationship=ADD-ONS%27"
response = requests.get(chihiro_base_url)
item = response.json()

dlcList = {}
for link in item["links"]:
    if "default_sku" in link:
        for entitlement in link["default_sku"]["entitlements"]:
            try:
                if entitlement["packages"]["size"] < 5000000:
                    dlcList[link["name"]] = link["id"]
            except TypeError:
                pass
            try:
                if entitlement["packages"][0]["size"] < 5000000:
                    dlcList[link["name"]] = link["id"]
            except IndexError:
                pass

if dlcList == {}:
    exit("No DLC found")

for name, content_id in dlcList.items():
    gen_gp4(name, content_id, pkg_location)
    system(
        f"PkgTool.exe pkg_build fake_dlc_temp\\fake_dlc_project.gp4 {pkg_location}/{content_id[7:16]}"
    )
    rmtree("fake_dlc_temp")
    print(f"Created DLC for {name} with contentID {content_id}")
