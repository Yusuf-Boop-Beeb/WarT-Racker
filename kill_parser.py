username = 'Yusuf#59'
kill, death = 0, 0
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

def track_kd(input):
    global kill, death
    kill += 1 if input == "kill" else 0
    death += 1 if input == "death" else 0
    k/d = float(kill/death)
    if input == "other" or "ignore":
        pass