import json
import os
from models import db, User, Crystal

def add_to_saves(user, crystal):
  if crystal not in user.user_saves:
    user.user_saves.append(crystal)
    db.session.commit()

def remove_from_saves(user, crystal):
  if crystal in user.user_saves:
    user.user_saves.remove(crystal)
    db.session.commit()

