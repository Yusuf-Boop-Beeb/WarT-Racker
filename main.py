import requests
import time
from pypresence import Presence
import csv

app_id = Presence("1548728310979104878")
app_id.connect()

start_time = time.time()
username = 'Yusuf#59'

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

def classify_msg(msg):
    for verb in (" shot down "," destroyed "):
        if verb in msg:
            attacker, victim = msg.split(verb, 1)
            if f"{username} (" in attacker:
                return "kill"
            if f"{username} (" in victim:
                return "death"
        return "other"
    return "ignore"

while True:
    try:
        info = requests.get("http://localhost:8111")
    except requests.exceptions.ConnectionError:
        app_id.update(
                    state="We might be saved 🥹",
                    details="Game is not running"
                    )
    else:

        try:
            obj_valid = requests.get("http://localhost:8111/mission.json").json()["objectives"]
        except requests.exceptions.JSONDecodeError:
            app_id.update(
                            details="In Hanger",
                            state="Awaiting Match, I fucking hate this shit"
                            )

        try:
            map_valid = requests.get("http://localhost:8111/map_info.json").json()["valid"]
        except requests.exceptions.JSONDecodeError:
            app_id.update(
                            details="In Hanger",
                            state="Awaiting Match, I fucking hate this shit"
                            )

        state = requests.get("http://localhost:8111/state").json()
        indicators = requests.get("http://localhost:8111/indicators").json()

        # Map == False when in hanger only
        # objectives == False when not in a real match (In test drive and hanger)
        # state == True only in air battles
        # I can say if objectives == true and state == false then its groub battles 100%

        if map_valid == True:

            if obj_valid is None:

                if state["valid"] == True:

                

                    app_id.update(
                        start=start_time,
                        details="Test Flying", 
                        state=f"Test Flying: {get_display_vehicle(indicators['type'])} || Current Speed = {state['TAS, km/h']} KM/H"
                        )
                else:

                    app_id.update(
                        start=start_time,
                        details="Test Driving",
                        state=f"Driving: {get_display_vehicle(indicators['type'])}"
                    )
                #Set status to in test drive and update it cosntatly
                #fetch indicators to check vehicle I'm test driving

            else:
                # In a real match
                if state["valid"] == True:

                    app_id.update(
                        start=start_time,
                        details="In Air Battle", 
                        state=f"Using: {get_display_vehicle(indicators['type'])} || Current Speed = {state['TAS, km/h']} KM/H"
                        )
                    #Set status to air battles
                    #fetch indicators to indicate which plane
                    #Count kills maybe indicate altitutde and speed

                else:

                    app_id.update(
                        start=start_time,
                        details="In Ground Battle",
                        state=f"Using: {get_display_vehicle(indicators['type'])}"
                                )
                    #Set status to ground battles
                    #fetch indicators to indicate which tank
                    #Count kills and deaths 


        else:
            app_id.update(
                start=start_time,
                details="In Hanger",
                state="Awaiting Match, I fucking hate this shit"
                )
            #Update status to in hanger and not in a match


    time.sleep(14)