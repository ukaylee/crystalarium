import os
import json
from Crystal import Crystal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_crystals():
    path = os.path.join(BASE_DIR, "crystals.json")

    with open(path, "r") as f:
        data = json.load(f)

    return [
        Crystal(
            item["id"],
            item["name"],
            item["props"],
            item["desc"]
        )
        for item in data
    ]