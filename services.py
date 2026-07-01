import json
import os
from Crystal import Crystal

def load_crystals():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "crystals.json")

    with open(file_path) as f:
        data = json.load(f)

    crystals = []
    for item in data:
        crystals.append(
            Crystal(
                item["id"],
                item["name"],
                item["props"],
                item["desc"]
            )
        )
    return crystals