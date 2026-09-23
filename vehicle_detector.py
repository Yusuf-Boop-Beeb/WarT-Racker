import csv

with open("units.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    units = {row["<ID|readonly|noverify>"]: row["<English>"] for row in reader}

def get_display_vehicle(codename):
    codename = codename.split("/")[-1]
    try:
       display_vehicle = units[codename]

    except KeyError:
       display_vehicle = units[codename + "_shop"]
    return display_vehicle