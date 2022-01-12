from datetime import datetime as dt
from time import sleep

import saving_system
import os
import json
import player
import threading

playing = False
loaded_file = False
has_finished_intro = False

data = {}

def menu():
    print("Welcome to the game! Type \"start\" to start a new game. Type \"continue\" to load a save file.")
    while True:
        command = input(">").lower()
        if command == "start":
            player_name = input("Your character's name: ")
            print("Which class would you like to be? (The text in parentheses will give you a boost in that ability)."
                + "\nFighter (strength)"
                + "\nRogue (agility)"
                + "\nMage (intelligence)")
            while True:
                player_class = input(">").lower()
                if player_class in ["fighter", "rogue", "mage"]:
                    break
                elif player_class == "cancel":
                    break
                else:
                    print("Invalid input.")
                    continue
            if player_class == "cancel":
                continue
            global _player
            _player = player.Player(player_name, player_class)
            if _player._class == "fighter":
                _player.strength = 5
                _player.agility = 3
                _player.intelligence = 1
            elif _player._class == "rogue":
                _player.strength = 3
                _player.agility = 5
                _player.intelligence = 3
            elif _player._class == "mage":
                _player.strength = 2
                _player.agility = 2
                _player.intelligence = 5
            while _player.ability_points > 0:
                print(f"You have {_player.ability_points} ability points to spend on the following stats:"
                    + f"\nStrength: {_player.strength}"
                    + f"\nAgility: {_player.agility}"
                    + f"\nIntelligence: {_player.intelligence}"
                    + "\nInput the ability name and how many points you want to spend in it. (Example: \"intelligence 2\")")
                input_asi = input(">").lower().split()
                if input_asi[0] == "strength":
                    if _player.ability_points - int(input_asi[1]) >= 0:
                        _player.strength += int(input_asi[1])
                        _player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
                elif input_asi[0] == "agility":
                    if _player.ability_points - int(input_asi[1]) >= 0:
                        _player.agility += int(input_asi[1])
                        _player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
                elif input_asi[0] == "intelligence":
                    if _player.ability_points - int(input_asi[1]) >= 0:
                        _player.intelligence += int(input_asi[1])
                        _player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
            print("These are your stats:"
                + f"\nStrength: {_player.strength}"
                + f"\nAgility: {_player.agility}"
                + f"\nIntelligence: {_player.intelligence}"
                )
            while True:
                confirm = input("Confirm? (Y/N): ").lower()
                if confirm == "y" or confirm == "yes":
                    print("Confirmed.")
                    save()
                    start()
                    break
                elif confirm == "n" or confirm == "no":
                    print("Canceled.")
                    break
                else:
                    print("Invalid input.")
                    continue
        elif command == "continue":
            if not "saves" in os.listdir():
                print("Save folder not found. You have probably not saved yet.")
                continue
            global data
            found_files = [i for i in os.listdir("./saves") if i.endswith(".agsave")]
            if len(found_files) == 1:
                for i in found_files:
                    data = load(i)
                    start()
            elif len(found_files) == 0:
                print("You have no save files!")
                continue
            elif len(found_files) > 1:
                print("Which save file would you like to load?")
                file_names = {}
                for i, j in enumerate(found_files):
                    print(f"[{i+1}] {j}")
                    file_names[str(i+1)] = j
                print(file_names)
                while True:
                    save_to_load = input(">").lower()
                    if file_names.get(save_to_load) in found_files:
                        data = load(file_names.get(save_to_load))
                        start()
                        break
                    elif save_to_load == "cancel":
                        break
                    else:
                        print("Invalid input.")
                        continue
        elif command == "exit" or command == "quit":
            exit()
        else:
            print("Invalid input.")
            continue

def save():
    if "saves" not in os.listdir():
        os.mkdir("saves")
    save_file_name = dt.now().strftime("%Y%m%d-%H%M%S%f")
    with open("./saves/" + save_file_name + ".agsave", "w") as save_file:
        print("Saving data...")
        data = {
            "story_progression": {
                "has_finished_intro": has_finished_intro,
            },
            "_player": _player
        }
        save_file.write(saving_system.string_to_binary(json.dumps(data, cls=player.CustomEncoder)))

    with open("./saves/" + save_file_name + ".agsave", "rb") as save_file:
        data = save_file.read()
        encrypted_data = saving_system.fernet_key.encrypt(data)

    with open("./saves/" + save_file_name + ".agsave", "wb+") as save_file:
        save_file.write(encrypted_data)
        print("Saved data.")

def load(data_file):
    with open("./saves/" + data_file, "rb") as save_file:
        print("Loading data...")
        data = save_file.read()
        decrypted_data = saving_system.fernet_key.decrypt(data)
        decoded_data = saving_system.binary_to_string(decrypted_data)
        json_data = json.loads(decoded_data)
        print("Loaded data.")
        print(json_data)
        print(json_data.get("_player"))
        global loaded_file
        loaded_file = True
        return json_data

def auto_save():
    if "saves" not in os.listdir():
        os.mkdir("saves")
    while playing:
        sleep(180)
        print("Saving... " + dt.now().strftime("(%H:%M:%S)"))
        save()
        print("Saved game.")

def start():
    global playing
    global _player
    global has_finished_intro

    playing = True
    if not loaded_file:
        has_finished_intro = False
    else:
        story_progression = data.get("story_progression")
        has_finished_intro = story_progression.get("has_finished_intro")
        _player = data.get("_player")
        _player = player.Player(_player.get("name"), _player.get("_class"), _player.get("ability_points"), _player.get("strength"), _player.get("agility"), _player.get("intelligence"))
        # For some reason it can't get "_class" from the data variable unless I do it like I did above
        # _player = player.Player(data.get("_player"))
        print(_player._class)

    t = threading.Thread(target=auto_save)
    t.daemon = True
    t.start()
    if not has_finished_intro:
        print("You find yourself in a battlefield. In front of you are thousands of soldiers fighting each other. While behind you are hundreds of mages casting all kinds of spells, "
            + "either attacking the enemies or aiding their allies.\n"
            + "You are part of the Nishdar Alliance, three nations who came together to defeat the evil nation of Lerkor. The battle you are currently in is a battle for the "
            + "Aleria mines, where most of the Alliance's ores come from.\n"
            + "As you come back to your senses you notice two enemy soldiers running towards you; how do you respond?\n")
        if _player._class == "fighter":
            print("[1] Wait for them to come close and then use your shield to block the left one's attack while using your sword to parry the right one's attack.\n"
                + "[2] Run towards the left one, kick them and knock them unconscious, then block the other's attack with your shield and stab them.\n"
                + "[3] Dodge both of their attacks.")
            while True:
                response = input(">").lower()
                if response in ["1", "2", "3"]:
                    if response == "1":
                        if _player.agility >= 5:
                            print("Your speed allows you to quickly block the left one's attack with your shield and the right one's attack with your sword.")
                            if _player.strength > 5:
                                print("What do you do now?")
                            else:
                                print("Unfortunately, you're not strong enough to hold your position and are quickly out of position, giving them an opening and allowing them to kill you.\n"
                                    + "You are dead.")
                                menu()
                        else:
                            print("You attempt to block both of them, but you only manage to block one of them and the other immediately strikes.\n"
                                + "You are dead.")
                            menu()
                    elif response == "2":
                        if _player.agility >= 5:
                            print("You run towards the left one and kick, ", end="")
                            if _player.strength >= 7:
                                print("and you land a powerful kick on them, knocking them unconscious!")
                                if _player.agility >= 7:
                                    print("With your quick reaction time, you masterfully block the other one's attack with your shield, giving you an opening. "
                                        + "You take a strike at them with your sword and land a killing blow!\n"
                                        + "You win!")
                                    exit()
                            else:
                                print("but your kick isn't strong enough to knock them unconscious")
                                # TODO: I AM HERE
                        else:
                            print("You run towards the left one and kick, but they are quicker and manage to block your kick, and immediately follow up with striking you.\n"
                                + "You are dead.")
                            exit()

                    elif response == "3":
                        third_option_fighter = True
                    break
                elif response == "save":
                    save()
                else:
                    print("Invalid input.")
                    continue
        elif _player._class == "rogue":
            print("[1] Disarm them."
                + "[2] Dodge both of their attacks.")
            while True:
                response = input(">").lower()
                if response in ["1", "2", "3"]:
                    if response == "1":
                        first_option_rogue = True
                    elif response == "2":
                        second_option_rogue = True
                    elif response == "3":
                        third_option_rogue = True
                    break
                elif response == "save":
                    save()
                else:
                    print("Invalid input.")
                    continue
        elif _player._class == "mage":
            print("[1] Cast a spell that shields you from a few of their attacks.\n"
                + "[2] Cast a spell that can teleport you short distances.\n"
                + "[3] Dodge both of their attacks.")
            while True:
                response = input(">").lower()
                if response in ["1", "2", "3"]:
                    if response == "1":
                        first_option_mage = True
                    elif response == "2":
                        second_option_mage = True
                    elif response == "3":
                        third_option_mage = True
                    break
                elif response == "save":
                    save()
                else:
                    print("Invalid input.")
                    continue
        has_finished_intro = True
    else:
        print("You finished the intro! This is all there is to the game at the moment!")

menu()
