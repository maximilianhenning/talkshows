import pandas as pd
from bs4 import BeautifulSoup
import requests
from os import path, makedirs

dir = path.dirname(__file__)
base = path.join(dir, "..")

def get_overview_htmls(sendung, link):
    if sendung == "anne_will":
        link_start, link_end = link.split("-1")
        link_list = [(link_start + "-" + str(x) + link_end) for x in range(1, 8)]
    elif sendung == "maischberger":
        link_start, link_end = link.split("-0.")
        link_list = [(link_start + "-" + str(x) + "." + link_end) for x in range(0, 8)]
    else:
        link_list = [link]
    if not path.exists(path.join(base, "overview_htmls")):
        makedirs(path.join(base, "overview_htmls"))
    position_counter = 1
    for link in link_list:
        response = requests.get(link)
        html = response.text
        if not path.exists(path.join(base, "overview_htmls", sendung)):
            makedirs(path.join(base, "overview_htmls", sendung))
        with open(path.join(base, "overview_htmls", sendung, str(position_counter) + ".html"), "w", encoding = "utf-8") as file:
            file.write(html)
        position_counter += 1

links_df = pd.read_csv(path.join(base, "data", "overview_links.csv"), sep = ";", encoding = "utf-8")
links_df.apply(lambda row: get_overview_htmls(row["sendung"], row["uebersicht"]), axis = 1)