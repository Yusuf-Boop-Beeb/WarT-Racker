import requests
username = "Yusuf#59"

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