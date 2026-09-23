import requests   
import time    
# Map == False when in hanger only
# objectives == False when not in a real match (In test drive and hanger)
# state == True only in air battles
# I can say if objectives == true and state == false then its groub battles 100%
GRACE_PERIOD_SECONDS = 20

_map_valid_since = None
_was_map_valid = False

state = requests.get("http://localhost:8111/state", timeout=2).json()



def get_mode(parameters=None):

    global _map_valid_since, _was_map_valid

    try:
        requests.get("http://localhost:8111", timeout=15)
    except requests.exceptions.ConnectionError:
        _map_valid_since = None
        _was_map_valid = False
        return "notInGame"

    try:
        map_info = requests.get("http://localhost:8111/map_info.json", timeout=2).json()
    except requests.RequestException:
        _map_valid_since = None
        _was_map_valid = False
        return "inHangar"

    map_valid = map_info.get("valid", False)

    if not map_valid:
        return "inHangar"

    if map_valid and not _was_map_valid:
        _map_valid_since = time.time()

    _was_map_valid = map_valid

    try:
        mission_valid = requests.get("http://localhost:8111/mission.json", timeout=2).json()["objectives"] is not None
    except requests.RequestException:
        mission_valid = False

    state = requests.get("http://localhost:8111/state", timeout=2).json()
    state_valid = state.get("valid", False)

    if mission_valid:
        map_valid_since = None
        return "inAir" if state_valid else "inGround"
    
    if _map_valid_since is None:
        _map_valid_since = time.time()

    elapsed = time.time() - _map_valid_since

    if elapsed < GRACE_PERIOD_SECONDS:
        return "loading"
    
    return "testFlight" if state_valid else "testDrive"
    
