import csv
import requests

import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_codename():
   try:
      codename = requests.get("http://localhost:8111/indicators", timeout=5).json().get("type", None)
   except requests.RequestException:
      return None
   return codename

with open(resource_path("units.csv"), "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    units = {row["<ID|readonly|noverify>"]: row["<English>"] for row in reader}

def get_display_vehicle(codename):
    if codename is None:
        return "Unknown Vehicle"
    codename = codename.split("/")[-1]
    try:
       display_vehicle = units[codename]

    except KeyError:
       display_vehicle = units[codename + "_shop"]
    return display_vehicle