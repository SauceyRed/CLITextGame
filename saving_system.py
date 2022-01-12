from cryptography.fernet import Fernet
from datetime import datetime as dt

import asyncio

# Add so it generates a key if key file not in secure folder or path

with open("key.fkey", "rb") as skey:
    key = skey.read()
fernet_key = Fernet(key)

def string_to_binary(string):
    return bin(int.from_bytes(string.encode(), "big"))

def binary_to_string(string):
    int_string = int(string, 2)
    return int_string.to_bytes((int_string.bit_length() + 7) // 8, "big").decode()
