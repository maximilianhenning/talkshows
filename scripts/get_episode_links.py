import pandas as pd
from bs4 import BeautifulSoup
from os import path, makedirs
from glob import glob

dir = path.dirname(__file__)
base = path.join(dir, "..")

def get_episode_links(sendung_dir, episoden_dict):
    sendung = sendung_dir.split("\\")[-1]
    if sendung not in episoden_dict.keys():
        episoden_dict[sendung] = []

    sendung_files = glob(path.join(sendung_dir, "*"))
    for sendung_file in sendung_files:
        with open(sendung_file, "r") as file:
            html = file.read()
        doc = BeautifulSoup(html, "html.parser")

        if sendung in ["anne_will", "maischberger", "hart_aber_fair"]:
            if sendung in ["anne_will", "maischberger"]:
                divs = doc.find_all("div", {"class": "media mediaA"})
            elif sendung == "hart_aber_fair":
                divs = doc.find_all("div", {"class": "teaser"})
            for div in divs:
                try:
                    a = div.find("a")
                    link = a.get("href")
                    if sendung == "anne_will":
                        link = "https://daserste.ndr.de" + link
                    elif sendung == "maischberger":
                        link = "https://daserste.de" + link
                    elif sendung == "hart_aber_fair":
                        link = "https://www1.wdr.de" + link
                    if sendung == "maischberger":
                        if "maischberger-" in link:
                            episoden_dict[sendung].append(link)
                    else:
                        episoden_dict[sendung].append(link)
                except:
                    pass
        elif sendung in ["markus_lanz", "maybrit_illner"]:
            divs = doc.find_all("div", {"class": "b-plus-button js-rb-click"})
            for div in divs:
                link = div.get("data-plusbar-url")
                if "-vom-" in link:
                    episoden_dict[sendung].append(link)
    return episoden_dict

sendungen_list = glob(path.join(base, "overview_htmls", "*"))
episoden_dict = {}
for sendung_file in sendungen_list:
    episoden_dict = get_episode_links(sendung_file, episoden_dict)
data = [(sendung, link) for sendung, links in episoden_dict.items() for link in links]
episoden_df = pd.DataFrame(data, columns = ["sendung", "link"])
episoden_df.to_csv(path.join(base, "data", "episode_links.csv"), sep = ";", index = False, encoding = "utf-8")