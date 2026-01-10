import json
import os
import sys
import shutil

APP_NAME = "ANOVIX_AI"

def get_appdata_dir():
    base = os.getenv("APPDATA") or os.path.expanduser("~")
    path = os.path.join(base, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

APPDATA_CONFIG = os.path.join(get_appdata_dir(), "user_config.json")
DEFAULT_CONFIG = resource_path("config/user_config.json")

def load_config():
    if not os.path.exists(APPDATA_CONFIG):
        if not os.path.exists(DEFAULT_CONFIG):
            raise FileNotFoundError("Default user_config.json missing")
        shutil.copy(DEFAULT_CONFIG, APPDATA_CONFIG)

    with open(APPDATA_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(APPDATA_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
