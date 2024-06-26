from os import path, makedirs
import subprocess

dir = path.dirname(__file__)
base = path.join(dir, "..")

print("Scraping overview HTMLs...")
subprocess.call(["python", path.join(dir, "scripts", "get_overview_htmls.py")])
print("Finding episode links...")
subprocess.call(["python", path.join(dir, "scripts", "get_episode_links.py")])
print("Scraping episode HTMLs...")
subprocess.call(["python", path.join(dir, "scripts", "get_episode_htmls.py")])
print("Finding episode details...")
subprocess.call(["python", path.join(dir, "scripts", "get_episode_details.py")])
print("Annotating...")
subprocess.call(["python", path.join(dir, "scripts", "annotate.py")])