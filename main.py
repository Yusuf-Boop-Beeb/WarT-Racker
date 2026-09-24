import requests
import time
from pypresence import Presence
from mode_detector import get_mode
from vehicle_detector import get_display_vehicle
import kill_parser


rpc = Presence("1548728310979104878")
rpc.connect()

START_TIME = time.time()
kill, death, kd_ratio = 0, 0, 0

def main():
    while True:
        
        mode = get_mode()
        
        vehicle_name = None

        messege = requests.get("http://localhost:8111/hudmsg?lastEvt=0&lastDmg=0")
        kill_parser.track_kd(kill_parser.classify_msg(messege))

        if mode in ("testDrive", "testFlight", "inAir", "inGround"):
            vehicle_codename = requests.get("http://localhost:8111/indicators", timeout=2).json().get("type")
            vehicle_name = get_display_vehicle(vehicle_codename)

        update_status(mode, vehicle_name, START_TIME, kill, death)

        time.sleep(1)

def update_status(gameStatus, current_vehicle=None, time=None, kills=0, deaths=0):

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
            state=f"Flying: {current_vehicle}, Kills:{kills}, Deaths:{deaths}",
            start=time
        )

    elif gameStatus == "inGround":
        rpc.update(
              details="In Ground Battle",
              state=f"Using: {current_vehicle}, Kills:{kills}, Deaths:{deaths}",
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