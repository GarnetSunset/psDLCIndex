import sys
from datetime import datetime
from os import makedirs, system
from shutil import rmtree
from tkinter import filedialog, simpledialog
from urllib.request import urlretrieve
import requests
import tkinter as tk

STORE_CODE_MAPPINGS = {
    "de-de": "DE/de",
    "gb-de": "GB/en",
    "se-en": "SE/en",
    "en-us": "US/en",
    "ja-jp": "JP/ja",
}


def get_pkg_editor():
    if sys.platform in ["linux", "linux2"]:
        return "./PkgTool.Core"
    elif sys.platform == "win32":
        return "PkgTool.exe"
    else:
        exit("Unsupported platform")


def gen_gp4(name, full_id, pkg_location):
    name = f'"{name}"'
    pkg_editor = get_pkg_editor()
    gp4_template = "pkg_ps4_ac_data {}"

    makedirs(f"{pkg_location}/{full_id[7:16]}", exist_ok=True)
    makedirs("fake_dlc_temp/sce_sys", exist_ok=True)

    with open("fake_dlc_temp/fake_dlc_project.gp4", "w") as x:
        x.write(gp4_template.format(full_id))

    urlretrieve("https://i.imgur.com/JeaTFEX.png", "fake_dlc_temp/sce_sys/icon0.png")

    commands = [
        f"{pkg_editor} sfo_new fake_dlc_temp/sce_sys/param.sfo",
        # More commands here...
    ]

    for command in commands:
        system(command)

    rmtree("fake_dlc_temp")

    print(f"Created DLC for {name} with contentID {full_id}")


def get_url(URL=None):
    if len(sys.argv) > 1:
        URL = sys.argv[1]

    if URL is None:
        URL = simpledialog.askstring(
            "Input",
            "Input the URL of the game you want the DLC for in this format:\n"
            "https://store.playstation.com/**-**/product/HP0700-CUSA00000_00-0000ENDOFTHEURL0",
        )

    return URL


def main():
    URL = get_url()
    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    region = URL.split("/")[3]
    content_id = URL.split("/")[5]
    chihiro_base_url = f"https://store.playstation.com/store/api/chihiro/00_09_000/container/{STORE_CODE_MAPPINGS[region]}/999/{content_id}?relationship=ADD-ONS%27"
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

    if not dlcList:
        exit("No DLC found")

    final_location = "fake_dlc_pkg"
    for dlc_name, content_id in dlcList.items():
        gen_gp4(dlc_name, content_id, final_location)


if __name__ == "__main__":
    main()
