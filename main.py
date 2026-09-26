import requests
import time
from pypresence import Presence
from mode_detector import get_mode
import vehicle_detector
import kill_parser

rpc = Presence("1548728310979104878")
rpc.connect()

def main():

    START_TIME = time.time()
    vehicle_name = None
    last_id = 0
    previous_get_mode_call = None #This checks wheather or not this is the first time I join a gamemode or if it's subsequent calls

    IN_MATCH_MODES = ("inAir", "inGround")
    MODES_WITH_VEHICLES = ("inAir", "inGround", "testFlight", "testDrive")

    while True:
        
        mode = get_mode()

        if mode in IN_MATCH_MODES and previous_get_mode_call not in IN_MATCH_MODES:
            last_id = kill_parser.get_id_and_process_messages(0, False)
            kill_parser.kill = 0
            kill_parser.death = 0

        if mode in IN_MATCH_MODES:
            last_id = kill_parser.get_id_and_process_messages(last_id)

        previous_get_mode_call = mode

        if mode in MODES_WITH_VEHICLES:
            vehicle_name = vehicle_detector.get_display_vehicle(vehicle_detector.get_codename())
        

        update_status(mode, vehicle_name, START_TIME, kill_parser.kill, kill_parser.death)

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