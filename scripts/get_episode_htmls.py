import pandas as pd
from bs4 import BeautifulSoup
import requests
from os import path, makedirs

dir = path.dirname(__file__)
base = path.join(dir, "..")

def get_episode_html(row, sendung, link):
    index = str(row.name)
    response = requests.get(link)
    html = response.text
    if not path.exists(path.join(base, "episode_htmls", sendung)):
        makedirs(path.join(base, "episode_htmls", sendung))
    with open(path.join(base, "episode_htmls", sendung, index + ".html"), "w", encoding = "utf-8") as file:
        file.write(html)

links_df = pd.read_csv(path.join(base, "data", "episode_links.csv"), sep = ";", encoding = "utf-8")
links_df.apply(lambda row: get_episode_html(row, row["sendung"], row["link"]), axis = 1)