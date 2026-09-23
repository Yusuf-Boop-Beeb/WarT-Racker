username = 'Yusuf#59'

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