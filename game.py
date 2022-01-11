from player import Player
from datetime import datetime as dt

import asyncio
import saving_system
import os

playing = False
read_intro = False

async def menu():
    print("Welcome to the game! Type \"start\" to start a new game. Type \"continue\" to load a save file.")
    while True:
        command = input(">").lower()
        if command == "start":
            player_name = input("Your character's name: ")
            player = Player(player_name)
            while player.ability_points > 0:
                print(f"You have {player.ability_points} ability points to spend on the following stats:"
                    + f"\nStrength: {player.strength}"
                    + f"\nAgility: {player.agility}"
                    + f"\nIntelligence: {player.intelligence}"
                    + "\nInput the ability name and how many points you want to spend in it. (Example: \"intelligence 2\")"
                    )
                input_asi = input(">").lower().split()
                if input_asi[0] == "strength":
                    if player.ability_points - int(input_asi[1]) >= 0:
                        player.strength = int(input_asi[1])
                        player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
                elif input_asi[0] == "agility":
                    if player.ability_points - int(input_asi[1]) >= 0:
                        player.agility = int(input_asi[1])
                        player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
                elif input_asi[0] == "intelligence":
                    if player.ability_points - int(input_asi[1]) >= 0:
                        player.intelligence = int(input_asi[1])
                        player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
            print("These are your stats:"
                + f"\nStrength: {player.strength}"
                + f"\nAgility: {player.agility}"
                + f"\nIntelligence: {player.intelligence}"
                )
            while True:
                confirm = input("Confirm? (Y/N): ").lower()
                if confirm == "y" or confirm == "yes":
                    print("Confirmed.")
                    await start()
                    break
                elif confirm == "n" or confirm == "no":
                    print("Canceled.")
                    break
                else:
                    print("Invalid input.")
                    continue
        elif command == "continue":
            found_files = [i for i in os.listdir("./saves") if i.endswith(".agsave")]
            if len(found_files) == 1:
                for i in found_files:
                    await load("./saves/" + i)
            elif len(found_files) == 0:
                print("You have no save files!")
                continue
            elif len(found_files) > 1:
                print("Which save file would you like to load?")
                for i, j in enumerate(found_files):
                    print(f"[{i}] {j}")
                while True:
                    save_to_load = input()
                    if save_to_load in found_files:
                        await load(save_to_load)
                        break
                    else:
                        print("Invalid input.")
                        continue
        else:
            print("Invalid input.")
            continue

async def save():
    save_file_name = dt.now().strftime("%Y%m%d-%H%M%S%f")
    with open("./saves/" + save_file_name + ".agsave", "w") as player_char:
        print("Saving data...")
        data = None
        player_char.write(saving_system.string_to_binary(data))

    with open("./saves/" + save_file_name + ".agsave", "rb") as player_char:
        data = player_char.read()
        encrypted_data = saving_system.fernet_key.encrypt(data)

    with open("./saves/" + save_file_name + ".agsave", "wb+") as player_char:
        player_char.write(encrypted_data)
        print("Saved data.")

async def load(data_file):
    with open(data_file, "rb") as player_char:
        print("Loading data...")
        data = player_char.read()
        decrypted_data = saving_system.fernet_key.decrypt(data)
        decoded_data = saving_system.binary_to_string(decrypted_data)
        print("Loaded data.")
        return decoded_data

async def auto_save():
    while playing:
        asyncio.sleep(180)
        print("Saving... " + dt.now().strftime("(%H:%M:%S)"))
        await save()
        print("Saved game.")

async def start():
    playing = True
    await auto_save()
    print("You find yourself in a battlefield. In front of you are thousands of soldiers fighting each other. While behind you are hundreds of mages casting all kinds of spells, "
        + "either attacking the enemies or aiding their allies.\n"
        + "You are part of the Nishdar Alliance, three nations who came together to defeat the evil nation of Lerkor. The battle you are currently in is a battle for the "
        + "Aleria mines, where most of the Alliance's ores come from.\n"
        + "")

asyncio.run(menu())
