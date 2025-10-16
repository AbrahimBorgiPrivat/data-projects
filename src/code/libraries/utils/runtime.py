import json

def load_runtime_vars(JSON_PATH: str):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)