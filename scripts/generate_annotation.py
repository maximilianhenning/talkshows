import pandas as pd
from os import path, makedirs
import numpy as np

dir = path.dirname(__file__)
base = path.join(dir, "..")

episodes_df = pd.read_csv(path.join(base, "data", "episode_details.csv"), sep = ";", encoding = "utf-8")

def merge_save_csv(complete_list, part):
    if path.exists(path.join(base, "data", "annotate_" + part + ".csv")):
        annotated_df = pd.read_csv(path.join(base, "data", "annotate_" + part + ".csv"), sep = ";", encoding = "utf-8")
        columns_to_check = annotated_df.columns.tolist()
        columns_to_check.remove(part)
        annotated_df = annotated_df[annotated_df[columns_to_check].notna().any(axis = 1)]
    else:
        annotated_df = pd.DataFrame()
        if part == "guests":
            annotated_df[[part, "beruf", "bereich", "partei", "geschlecht"]] = np.nan
        if part == "topics":
            annotated_df[[part, "bereich", "tags"]] = np.nan
        annotated_list = []
    annotated_list = annotated_df[part].tolist()
    unannotated_list = [item for item in complete_list if item not in annotated_list]

    unannotated_df = pd.DataFrame(unannotated_list)
    if part == "guests":
        unannotated_df[["beruf", "bereich", "partei", "geschlecht"]] = np.nan
    if part == "topics":
        unannotated_df[["bereich", "tags"]] = np.nan
    unannotated_df = unannotated_df.rename(columns = {0: part})

    complete_df = pd.concat([annotated_df, unannotated_df])
    complete_df.to_csv(path.join(base, "data", "annotate_" + part + ".csv"), index = False, sep = ";", encoding = "utf-8")

# Guests
guests_column = episodes_df["guests"].tolist()
guests_column = [guests_entry.split(",") for guests_entry in guests_column if type(guests_entry) == str]
guests_list = []
for guests_entry in guests_column:
    for guest in guests_entry:
        guests_list.append(guest)
guests_list = list(set(guests_list))
merge_save_csv(guests_list, "guests") 

# Topics
topics_list = episodes_df["teaser"].tolist()
merge_save_csv(topics_list, "topics")