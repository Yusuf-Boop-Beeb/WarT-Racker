import requests
import time
from pypresence import Presence

rpc = Presence("1548728310979104878")
rpc.connect()

    try:
        info = requests.get("http://localhost:8111")
    except requests.exceptions.ConnectionError:
        rpc.update(
                    state="WarThunder is not launched",
                    details="Game is not running"
                    )
    else:

        try:
            obj_valid = requests.get("http://localhost:8111/mission.json").json()["objectives"]
        except requests.exceptions.JSONDecodeError:
            rpc.update(
                            details="In Hanger",
                            state="Awaiting Match, I fucking hate this shit"
                            )

        try:
            map_valid = requests.get("http://localhost:8111/map_info.json").json()["valid"]
        except requests.exceptions.JSONDecodeError:
            rpc.update(
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

                

                    rpc.update(
                        start=start_time,
                        details="Test Flying", 
                        state=f"Test Flying: {get_display_vehicle(indicators['type'])} || Current Speed = {state['TAS, km/h']} KM/H"
                        )
                else:

                    rpc.update(
                        start=start_time,
                        details="Test Driving",
                        state=f"Driving: {get_display_vehicle(indicators['type'])}"
                    )
                #Set status to in test drive and update it cosntatly
                #fetch indicators to check vehicle I'm test driving

            else:
                # In a real match
                if state["valid"] == True:

                    rpc.update(
                        start=start_time,
                        details="In Air Battle", 
                        state=f"Using: {get_display_vehicle(indicators['type'])} || Current Speed = {state['TAS, km/h']} KM/H"
                        )
                    #Set status to air battles
                    #fetch indicators to indicate which plane
                    #Count kills maybe indicate altitutde and speed

                else:

                    rpc.update(
                        start=start_time,
                        details="In Ground Battle",
                        state=f"Using: {get_display_vehicle(indicators['type'])}"
                                )
                    #Set status to ground battles
                    #fetch indicators to indicate which tank
                    #Count kills and deaths 


        else:
            rpc.update(
                start=start_time,
                details="In Hanger",
                state="Awaiting Match, I fucking hate this shit"
                )
            #Update status to in hanger and not in a match


    time.sleep(14)