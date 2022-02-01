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
        player_name = ""
        if command == "start":
            while player_name == "":
                player_name = input("Your character's name: ")
                if player_name in ["cancel", "quit"]:
                    exit()
                elif not len(player_name) > 0:
                    print("You must input a name.")
            global _player
            _player = player.Player(name=player_name, strength=5, agility=3, intelligence=1)
            _player.strength = 5
            _player.agility = 3
            _player.intelligence = 1
            while _player.ability_points > 0:
                print(f"You have {_player.ability_points} ability points to spend on the following stats:"
                    + f"\nStrength: {_player.strength}"
                    + f"\nAgility: {_player.agility}"
                    + f"\nIntelligence: {_player.intelligence}"
                    + "\nInput the ability name and how many points you want to spend in it. (Example: \"intelligence 2\" or \"int 2\")")
                input_asi = input(">").lower().split()
                if input_asi[0] in ["exit", "quit", "cancel"]:
                    exit()
                elif input_asi == []:
                    continue
                elif input_asi[0] in ["strength", "str"]:
                    if _player.ability_points - int(input_asi[1]) >= 0:
                        _player.strength += int(input_asi[1])
                        _player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
                elif input_asi[0] in ["agility", "agi"]:
                    if _player.ability_points - int(input_asi[1]) >= 0:
                        _player.agility += int(input_asi[1])
                        _player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
                elif input_asi[0] in ["intelligence", "int"]:
                    if _player.ability_points - int(input_asi[1]) >= 0:
                        _player.intelligence += int(input_asi[1])
                        _player.ability_points -= int(input_asi[1])
                    else:
                        print("You don't have enough points!")
                else:
                    print("Invalid input.")
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
        elif command == "continue":
            if "saves" not in os.listdir(saving_system.game_path):
                print("Save folder not found. You have probably not saved yet.")
                continue
            global data
            found_files = [i for i in os.listdir(saving_system.saves_path) if i.endswith(".agsave")]
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
                while True:
                    save_to_load = input(">").lower()
                    if file_names.get(save_to_load) in found_files:
                        data = load(file_names.get(save_to_load))
                        start()
                        break
                    elif save_to_load in ["exit", "quit", "cancel"]:
                        break
                    else:
                        print("Invalid input.")
        elif command in ["exit", "quit", "cancel"]:
            exit()
        else:
            print("Invalid input.")

def save():
    date_time = dt.now().strftime("%Y%m%d-%H%M%S%f")
    save_file_name = os.path.join(saving_system.saves_path, date_time + ".agsave")
    with open(save_file_name, "w") as save_file:
        print("Saving data...")
        data = {
            "story_progression": {
                "has_finished_intro": has_finished_intro,
            },
            "_player": _player
        }
        save_file.write(saving_system.string_to_binary(json.dumps(data, cls=player.CustomEncoder)))

    with open(save_file_name, "rb") as save_file:
        data = save_file.read()
        encrypted_data = saving_system.fernet_key.encrypt(data)

    with open(save_file_name, "wb+") as save_file:
        save_file.write(encrypted_data)
        print("Saved data.")

def load(data_file):
    with open(os.path.join(saving_system.saves_path, data_file), "rb") as save_file:
        print("Loading data...")
        data = save_file.read()
        decrypted_data = saving_system.fernet_key.decrypt(data)
        decoded_data = saving_system.binary_to_string(decrypted_data)
        json_data = json.loads(decoded_data)
        print("Loaded data.")
        global loaded_file
        loaded_file = True
        return json_data

def auto_save():
    if "saves" not in os.listdir():
        os.mkdir("saves")
    sleep(180)
    while auto_saving:
        print("Saving... " + dt.now().strftime("(%H:%M:%S)"))
        save()
        print("Saved game.")
        sleep(180)

def start():
    global auto_saving
    global _player
    global has_finished_intro

    auto_saving = True
    if not loaded_file:
        has_finished_intro = False
    else:
        story_progression = data.get("story_progression")
        has_finished_intro = story_progression.get("has_finished_intro")
        # _player = data.get("_player")
        # _player = player.Player(_player.get("name"), _player.get("_class"), _player.get("ability_points"), _player.get("strength"), _player.get("agility"), _player.get("intelligence"))
        # For some reason it can't get "_class" from the data variable unless I do it like I did above
        _player = player.Player(data.get("_player"))

    t = threading.Thread(target=auto_save)
    t.daemon = True
    t.start()
    if not has_finished_intro:
        print("You find yourself in a battlefield. In front of you are thousands of soldiers fighting each other. While behind you are hundreds of mages casting all kinds of spells, "
            + "either attacking the enemies or aiding their allies.\n"
            + "You are part of the Nishdar Alliance, three nations who came together to defeat the evil nation of Lerkor. The battle you are currently in is a battle for the "
            + "Aleria mines, where most of the Alliance's ores come from.\n"
            + "As you come back to your senses you notice two enemy soldiers, a man and a woman, running towards you; how do you respond?\n"
            + "[1] Wait for them to come close and then use your shield to block the man's attack while using your sword to parry the woman's attack.\n"
            + "[2] Run towards the man one, kick him and knock him unconscious, then block the woman's attack with your shield and stab her.\n"
            + "[3] Dodge both of their attacks and attempt to knock one of them down.")
        while True:
            response = input(">").lower()
            if response in ["1", "2", "3"]:
                if response == "1":
                    if _player.agility >= 5:
                        print("Your speed allows you to quickly block the man's attack with your shield and the woman's attack with your sword.")
                        if _player.strength > 5:
                            print("What do you do now?")
                            # TODO: Next choices
                        else:
                            print("Unfortunately, you're not strong enough to hold your position and are quickly out of position, giving them an opening and allowing them to kill you.\n"
                                + "You are dead.\n")
                            auto_saving = False
                            menu()
                    else:
                        print("You attempt to block both of them, but you only manage to block one of them and the other immediately strikes.\n"
                            + "You are dead.\n")
                        auto_saving = False
                        menu()
                elif response == "2":
                    if _player.agility >= 5:
                        print("You run towards the man, ", end="")
                        if _player.strength >= 7:
                            print("and you land a powerful kick on him, knocking him unconscious!")
                            if _player.agility >= 7:
                                print("With your quick reaction time, you masterfully block the woman's attack with your shield, giving you an opening. "
                                    + "You take a strike at her with your sword and land a killing blow!\n"
                                    + "You win!")
                                exit()
                            else:
                                print("However, as you turn around, you see the woman about to strike you. You're not fast enough and are hit.\n"
                                    + "You are dead.\n")
                                auto_saving = False
                                menu()
                        else:
                            print("and attempt to kick him. Unfortunately, your kick isn't strong enough to knock him unconscious, alowwing him to grab you "
                                + "and hold you in place, as the woman stabs you.\n"
                                + "You are dead.\n")
                            auto_saving = False
                            menu()
                    else:
                        print("You run towards the man and kick, but he is quicker and manages to block your kick, and immediately follows up with striking you.\n"
                            + "You are dead.\n")
                        auto_saving = False
                        menu()

                elif response == "3":
                    if _player.agility >= 4:
                        print("As you dodge the first attack, ", end="")
                        if _player.strength >= 5:
                            print("you manage to sweep his leg and knock him down. You get up and prepare to respond to the woman's attack.")
                        else:
                            print("you attempt to sweep his leg, but fail. You are about to get hit but manage to jump back a bit. What do you do now?\n")
                            # TODO: More choices
                    else:
                        print("You attempt to focus on their attacks and try to dodge them, but you accidentally slip and fall. They immediately take the opportunity to kill you.\n"
                            + "You are dead.\n")
                        auto_saving = False
                        menu()
                break
            elif response == "save":
                save()
            elif response == "menu":
                menu()
            elif response in ["exit", "quit", "cancel"]:
                exit()
            else:
                print("Invalid input.")
        has_finished_intro = True
    print("\nYou finished the intro! This is all there is to the game at the moment!\n")
    auto_saving = False
    menu()

if __name__ == "__main__":
    menu()
