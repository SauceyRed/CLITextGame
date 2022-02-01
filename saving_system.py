from cryptography.fernet import Fernet
from datetime import datetime as dt
from sys import platform

import asyncio
import os

# Add so it generates a key if key file not in secure folder or path

game_path = os.getcwd()
saves_path = os.path.join(game_path, "saves")

if platform == "win32":
    game_appdata_path = os.path.join(os.environ.get("APPDATA"), "The Amazing Text Adventure")
    key_path = os.path.join(game_appdata_path, "key.agkey")
    if "The Amazing Text Adventure" not in os.listdir(os.environ.get("APPDATA")):
        try:
            os.mkdir(game_appdata_path)
        except Exception as e:
            print("Could not create AppData folder!\nException: " + str(e))
else:
    game_appdata_path = os.path.join(os.getcwd(), "AppData")
    key_path = os.path.join(game_appdata_path, "key.agkey")
    if "AppData" not in os.listdir(game_path):
        try:
            os.mkdir(game_appdata_path)
        except Exception as e:
            print("Could not create AppData folder!\nException: " + str(e))

if "saves" not in os.listdir(game_path):
    os.mkdir(saves_path)

# if "The Amazing Text Adventure" not in os.listdir(documents_folder):
#     os.mkdir(game_path)
#     os.mkdir(saves_path)

if "key.agkey" not in os.listdir(game_appdata_path):
    with open(key_path, "wb") as skey:
        key = Fernet.generate_key()
        skey.write(key) 

with open(key_path, "rb") as skey:
    key = skey.read()
fernet_key = Fernet(key)

def string_to_binary(string):
    return bin(int.from_bytes(string.encode(), "big"))

def binary_to_string(string):
    int_string = int(string, 2)
    return int_string.to_bytes((int_string.bit_length() + 7) // 8, "big").decode()
