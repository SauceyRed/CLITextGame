import saving_system
import json
from cryptography.fernet import Fernet
import time
from pprint import pprint

class Player:
    def __init__(self, name: str, ability_points: int = 10, strength: int = 0, agility: int = 0, intelligence: int = 0):
        self.name = name
        self.ability_points = ability_points
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

    def to_json(self):
        return {
            "name": self.name,
            "ability_points": self.ability_points,
            "strength": self.strength,
            "agility": self.agility,
            "intelligence": self.intelligence
        }

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if "to_json" in dir(o):
            return o.to_json()
        return json.JSONEncoder.default(self, o)
