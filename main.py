import requests
import time
from pypresence import Presence
from mode_detector import get_mode
from vehicle_detector import get_display_vehicle

rpc = Presence("1548728310979104878")
rpc.connect()

def main():
    while True:

        mode = get_mode()
        vehicle_name = None

        if mode in ("testDrive", "testFlight", "inAir", "inGround"):

            vehicle_codename = requests.get("http://localhost:8111/indicators", timeout=2).json().get("type")

            if vehicle_codename is not None:
                vehicle_name = get_display_vehicle(vehicle_codename)
            else:
                vehicle_name = "Deciding"


        update_status(mode, vehicle_name)

        time.sleep(15)

def update_status(gameStatus, current_vehicle=None):

    if gameStatus == "notInGame":
        rpc.update(
            details="Game is not launched",
            state="Warthunder is not running"
        )
        
    elif gameStatus == "inAir":
        rpc.update(
            details="In Air Battle",
            state=f"Flying: {current_vehicle}"
        )

    elif gameStatus == "inGround":
        rpc.update(
              details="In Ground Battle",
              state=f"Using: {current_vehicle}"
        )

    elif gameStatus == "testFlight":
        rpc.update(
            details="In Test Flight",
            state=f"Flying: {current_vehicle}"
        )

    elif gameStatus == "testDrive":
      rpc.update(
            details="In Test Drive",
            state=f"Driving: {current_vehicle}"
        )
      
    else:
        rpc.update(
            details="Loading"
        )

if __name__ == "__main__":
    main()        