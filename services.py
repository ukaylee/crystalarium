import json
from Crystal import Crystal

def load_crystals():
  with open("crystals.json") as f:
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