import requests
from config import get_username

from config import get_username

username = get_username()

kill, death, kd_ratio = 0, 0, 0

    
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

def track_kd(classification):
    global kill, death, kd_ratio
    kill += 1 if classification == "kill" else 0
    death += 1 if classification == "death" else 0
    if death > 0:
        kd_ratio = float(kill/death)
    else:
        kd_ratio = kill

def get_id_and_process_messages(id, process=True):
    try:

        messages = requests.get(
            "http://localhost:8111/hudmsg",
            params={"lastEvt": 0, "lastDmg": id},
            timeout=5
        ).json().get("damage", [])

    except requests.exceptions.RequestException:
        return id

    for msg in messages:
        id = max(id, msg["id"])
        if process:
            classification = classify_msg(msg["msg"])
            track_kd(classification)

    return id

