import json
import os
from models import db, User, Crystal

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
                item["desc"],
                item["img"]
            )
        )
    return crystals

def add_to_saves(user, crystal):
    user.user_saves.append(crystal)
    db.session.commit()