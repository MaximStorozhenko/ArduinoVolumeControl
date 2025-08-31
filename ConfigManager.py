import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG_INFO = {
    "port": "COM55",
    "baudrate": 9600
}

def LoadConfig():
    if not os.path.exists(CONFIG_FILE):
        SaveConfig(DEFAULT_CONFIG_INFO)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def SaveConfig(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)