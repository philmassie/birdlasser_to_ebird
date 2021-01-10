import pandas as pd
import numpy as np
import sys
import os
import pathlib
import datetime as dt
import re

try:
    wd = pathlib.Path(sys.argv[1])
except:
    wd = pathlib.Path("D:\\My Folders\\My Cloud\\Dropbox\\bird lists\\2019\\birdlasser_02\\")

print(wd)

files = os.listdir(wd)
print(files)

# fname =  files[0]
# lasser = pd.read_csv(str(wd) + "\\" + files[0])

def ebird_maker(lasser, fname):
    # Date
    lasser['Date']= pd.to_datetime(lasser['Date'])
    list_date_min = min(lasser["Date"])
    list_date_max = max(lasser["Date"])
    lasser.groupby("Date").count()
    date_freq = lasser["Date"].value_counts()
    list_date_frequent = date_freq.index[0].date()

    # Location name guess
    m = re.search(r"\d", fname).start()
    loc_guess = fname[:m].replace("BirdLasser_", "").strip()

    # inputs
    print("\n" + fname)
    print("=" * len(fname))

    loc_name = input("Location name (" + loc_guess + "): ") or loc_guess

    print("List date range: " + str(list_date_min) + " - " +  str(list_date_max))
    list_date = dt.datetime.strptime(input("Select a list date (" + str(list_date_frequent) + "): ") or str(list_date_frequent), "%Y-%m-%d").date()

    # Species Comments
    lasser["Seen/Heard"] = lasser["Seen/Heard"].replace(np.nan, "", regex=True).replace("\n", "", regex=True)
    lasser["Notes"] = lasser["Notes"].replace(np.nan, "", regex=True).replace("\n", "", regex=True)

    species_comments = []
    for _, row in lasser.iterrows():
        comment = row["Seen/Heard"]
        if len(row["Notes"]) > 0:
            comment = comment + " - " + row["Notes"]
        species_comments.append(comment)
    
    lat = round(lasser["Latitude"].mean(),7)
    lon = round(lasser["Longitude"].mean(),7)
    province = input("Province (WC,KZN,NC...): ")
    country_code = input("Country code (ZA): ") or "ZA"
    protocol = input("Protocol (Historical): ") or "Historical"
    obs_count = input("Number of Observers (2): ") or "2"
    list_comments = input("Any list comments (None)? ") or ""

    # build ebird table
    ebird_cols = ["Common Name", "Genus", "Species", "Number", "Species Comments", "Location Name", "Latitude", "Longitude", "Date", "Start Time", "State/Province", "Country Code", "Protocol", "Number of Observers", "Duration", "All observations reported?", "Effort", "Distance Miles", "Effort", "area", "acres", "Submission Comments"]
    ebird = pd.DataFrame(columns=ebird_cols)

    ebird["Common Name"] = lasser["Species primary name"]
    ebird["Genus"] = [s.split(sep = " ")[0] for s in lasser["Species tertiary name"]]
    ebird["Species"] = [s.split(sep = " ")[1] for s in lasser["Species tertiary name"]]
    ebird["Number"] = 1
    ebird["Species Comments"] = species_comments
    ebird["Location Name"] = loc_name
    ebird["Latitude"] = lat
    ebird["Longitude"] = lon
    ebird["Date"] = list_date.strftime("%m/%d/%Y")
    ebird["State/Province"] = province
    ebird["Country Code"] = country_code
    ebird["Protocol"] = protocol
    ebird["Number of Observers"] = obs_count
    ebird["Submission Comments"] = list_comments
    ebird = ebird.replace(np.nan, "", regex=True)

    print(ebird.head())

    happy = input("Happy (Y)? ").lower() or "y"
    if happy == "n":
        ebird = happy

    return(ebird)

f = files [0]
ebird_full = []

for f in files:
    success = False
    while success == False:
        ebird = ebird_maker(pd.read_csv(str(wd) + "\\" + f), f)
        if str(type(ebird)) == "<class 'pandas.core.frame.DataFrame'>":
            success = True
            ebird_full = ebird_full + [ebird]

ebird_pdf = pd.concat(ebird_full)

input("Pausing: ")


upload_file = str(wd.parent.joinpath("ebird_" + str(dt.datetime.now()).replace(":", ".").replace(" ", "_") + ".csv"))

input("Pausing: ")
ebird_pdf.to_csv(upload_file, header=False, index=False)

