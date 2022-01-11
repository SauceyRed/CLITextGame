import saving_system
import json
from cryptography.fernet import Fernet
import time
from pprint import pprint

class Player:
    def __init__(self, name: str, _class: str):
        self.name = name
        self._class = _class
        self.ability_points = 10
        self.strength = 0
        self.agility = 0
        self.intelligence = 0

    def add_to_inv(self, item):
        with open("inventory.json", "a") as inv:
            json.dump(item, inv, indent=4)

    def get_inv(self):
        with open("inventory.json", "r") as inv:
            data = json.load(inv)
            print(data["Sword"])

# player = Player("Lucy", "female")
# player.add_to_inv({"Weapons": {"Sword": {"Quantity": 1, "Durability": 8, "Attack": 3}}})
# player.get_inv()
# player.add_to_inv({"Potions": {"Healing Potion": {"Quantity": 1, "Uses": 1, "Healing": 10}}})
