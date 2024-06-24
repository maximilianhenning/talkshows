import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from os import path
from glob import glob
import re

dir = path.dirname(__file__)
base = path.join(dir, "..")

def get_episode_details(sendung, episode_file):
    with open(episode_file, "r", encoding = "utf-8") as file:
        html = file.read()
    doc = BeautifulSoup(html, "html.parser")

    date = np.nan
    title = np.nan
    teaser = np.nan
    guests = np.nan

    if sendung == "anne_will":
        # Date
        date_div = doc.find("h2")
        date = date_div.contents[0]
        date = date.split("|")[2].strip()
        # Title
        title_div = doc.find("meta", {"name": "title"})
        title = title_div.get("content")
        # Teaser
        teaser_div = doc.find("p", {"class": "text small"})
        teaser = teaser_div.contents[1]
        # Guests
        guests_div = doc.find("meta", {"name": "description"})
        guests = guests_div.get("content")
        guests = re.sub("Das Thema diskutieren |\.", "", guests)
        guests = re.split(", | und ", guests)
        guests = ",".join(guests)

    if sendung == "hart_aber_fair":
        # Date
        date_div = doc.find("meta", {"name": "Keywords"})
        date = date_div.get("content")
        date = date.split(",")[1]
        # Title
        title_div = doc.find("meta", {"name": "Keywords"})
        title = title_div.get("content")
        title = title.split("Louis Klamroth, ")[1].strip()
        # Teaser
        teaser_divs = doc.find_all("p", {"class": "teasertext"})
        teaser_div = teaser_divs[1]
        teaser = teaser_div.contents[0].strip()
        # Guests
        guest_list = []
        guest_master_divs = doc.find_all("picture", {"data-resp-img-id": "TeaserImageStageSectionAModA"})
        for guest_master_div in guest_master_divs:
            guest_div = guest_master_div.find("img")
            guest = guest_div.get("title")
            guest = guest.split(" | ")[0]
            if "," in guest:
                guest = guest.split(",")[0]
            guest_list.append(guest)
            guest_list = list(set(guest_list))
        guests = ",".join(guest_list)

    if sendung == "maischberger":
        # Date
        date_div = doc.find("title")
        date = date_div.contents[0]
        date = date.strip("maischberger am ")
        date = date.split("- maischberger")[0]
        # Title
        # Teaser
        teaser_list = []
        teaser_divs = doc.find_all("p", {"class": "text small"})
        for teaser_div in teaser_divs:
            teaser_list.append(str(teaser_div.contents[0]))
        teaser = ", ".join(teaser_list)
        # Guests
        guests_div = doc.find("meta", {"name": "description"})
        guests_raw = guests_div.get("content")
        guests_raw = re.sub("Zu Gast: |\.|", "", guests_raw)
        guests_raw = re.split(', | und ', guests_raw)
        guest_list = []
        for guest in guests_raw:
            if " (" in guest:
                guest_list.append(guest.split(" (")[0])
            elif not ")" in guest:
                guest_list.append(guest)
        guests = ",".join(guest_list)

    if sendung == "markus_lanz":
        # Date
        date_div = doc.find("title")
        date = date_div.contents[0].strip()
        date = re.sub("Markus Lanz vom | - ZDFmediathek", "", date)
        # Title
        # Teaser
        teaser_list = []
        teaser_master_divs = doc.find_all("div", {"class": "grid-container grid-x"})
        for teaser_master_div in teaser_master_divs:
            try:
                teaser_div = teaser_master_div.find("div", {"class": "cell large-8 large-offset-2"})
                teaser_raw = teaser_div.contents[1]
                teaser_list_raw = teaser_raw.split("<br/>")[1:]
                for teaser in teaser_list_raw:
                    try:
                        if teaser[0] != "<":
                            teaser = teaser.split("<")[0]
                            teaser_list.append(teaser)
                    except:
                        pass
            except:
                pass
        teaser = ",".join(teaser_list)
        # Guests
        guests_div = doc.find("meta", {"name": "description"})
        guests = guests_div.get("content")
        guests = guests.strip("Zu Gast: ")
        guest_list_raw = re.split(', | und ', guests)
        guest_list = [" ".join(guest.split(" ")[1:]) if " " in guest else guest for guest in guest_list_raw]
        guests = ",".join(guest_list)

    if sendung == "maybrit_illner":
        # Date
        date_div = doc.find("div", {"class": "teaser-extended-info"})
        try:
            date = date_div.contents[0]
        except:
            pass
        # Title
        title_div = doc.find("title")
        title = title_div.contents[0].strip()
        # Teaser
        teaser_overlord_divs = doc.find_all("div", {"class": "grid-container grid-x"})
        teaser_list = []
        for teaser_overlord_div in teaser_overlord_divs[:2]:
            try:
                teaser_master_div = teaser_overlord_div.find("div", {"class": "cell large-8 large-offset-2"})
                teaser_div = teaser_master_div.find("p")
                teaser_part = teaser_div.contents[0]
                teaser_list.append(str(teaser_part))
            except:
                pass
        teaser = ", ".join(teaser_list)
        # Guests
        guest_list = []
        guest_master_divs = doc.find_all("h3", {"class": "guest-name"})
        for guest_master_div in guest_master_divs:
            guest_div = guest_master_div.find("button")
            guest = guest_div.contents[0]
            guest = guest.strip()
            if " (" in guest:
                guest = guest.split(" (")[0]
            guest_list.append(guest)
        guests = ",".join(guest_list)

    return ([date, title, teaser, guests])

episode_details_dict = {}
sendungen_dir_list = glob(path.join(base, "episode_htmls", "*"))
for sendung_dir in sendungen_dir_list:
    sendung = path.basename(sendung_dir).split(".")[0]
    episode_file_list = glob(path.join(sendung_dir, "*"))
    for episode_file in episode_file_list:
        episode_index = path.basename(episode_file).split(".")[0]
        episode_details_dict[episode_index] = [sendung]
        episode_details_dict[episode_index] += (get_episode_details(sendung, episode_file))
episode_details_df = pd.DataFrame.from_dict(episode_details_dict, orient = "index")
episode_details_df = episode_details_df.rename(columns = {0: "sendung", 1: "date", 2: "title", 3: "teaser", 4: "guests"})
episode_details_df.to_csv(path.join(base, "data", "episode_details.csv"), sep = ";", index = False, encoding = "utf-8")