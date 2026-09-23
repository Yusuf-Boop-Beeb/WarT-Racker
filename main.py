import requests
import time
from pypresence import Presence
from mode_detector import get_mode
from vehicle_detector import get_display_vehicle


rpc = Presence("1548728310979104878")
rpc.connect()

START_TIME = time.time()

def main():
    while True:
        
        raw_mode = get_mode()
        


        actual_mode = raw_mode
        vehicle_name = None

        if raw_mode in ("testDrive", "testFlight", "inAir", "inGround"):
            try:
                vehicle_codename = requests.get("http://localhost:8111/indicators", timeout=2).json().get("type")
                vehicle_name = get_display_vehicle(vehicle_codename)
            except requests.RequestException:
                vehicle_name = "Deciding"

        update_status(raw_mode, vehicle_name, START_TIME)

        time.sleep(1)

def update_status(gameStatus, current_vehicle=None, time=None):

    if gameStatus == "notInGame":
        rpc.update(
            details="Game is not launched",
            state="Warthunder is not running"
        )
    elif gameStatus == "inHangar":
        rpc.update(
            details="In Hangar",
            state="Awating doom and suffering...",
            start=time
        )    
    elif gameStatus == "inAir":
        rpc.update(
            details="In Air Battle",
            state=f"Flying: {current_vehicle}",
            start=time
        )

    elif gameStatus == "inGround":
        rpc.update(
              details="In Ground Battle",
              state=f"Using: {current_vehicle}",
              start=time
        )

    elif gameStatus == "testFlight":
        rpc.update(
            details="In Test Flight",
            state=f"Flying: {current_vehicle}",
            start=time
        )

    elif gameStatus == "testDrive":
      rpc.update(
            details="In Test Drive",
            state=f"Driving: {current_vehicle}",
            start=time
        )
      
    else:
        rpc.update(
            details="Intermission",
            state="Loading...",
            start=time
        )

if __name__ == "__main__":
    main()        