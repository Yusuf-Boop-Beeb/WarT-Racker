import sys
import os
import json

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_username():
    config_path = os.path.join(get_app_dir(), "config.json")

    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        username = config["username"]
        confirm = input(f"Use saved username '{username}'? (y/n): ").strip().lower()
        if confirm == "y":
            return username

    username = input("Enter your War Thunder username: ").strip()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({"username": username}, f)
    return username