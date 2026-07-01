# This file should be run if you want to seed the database with crystals.
import os
import json

from main import app, db
from models import Crystal


def seed():
  base_dir = os.path.dirname(__file__)
  file_path = os.path.join(base_dir, "crystals.json")

  with open(file_path) as f:
    data = json.load(f)

  for item in data:
    exists = Crystal.query.filter_by(name=item["name"]).first()
    if exists:
        continue

    db.session.add(Crystal(
        name=item["name"],
        props=item["props"],
        desc=item["desc"],
        img=item["img"]
    ))

  db.session.commit()


if __name__ == "__main__":
  with app.app_context():
    seed()