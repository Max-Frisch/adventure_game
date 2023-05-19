import armory
import bestiary
import random
from classes import Game, Player, Room
from colorama import Fore, init


# welcome prints out the welcome text
def welcome():
    print(Fore.RED + "                                               D U N G E O N")
    print(Fore.GREEN + """
    The village of Honeywood has been terrorized by strange, deadly creatures for months now. Unable to endure any
    longer, the villagers pooled their wealth and hired the most skilled adventurer they could find: you. After
    listening to their tale of woe, you agree to enter the labyrinth where most of the creatures seem to originate,
    and destroy the foul beasts. Armed with a longsword and a bundle of torches, you descend into the labyrinth,
    ready to do battle....
    
    """)


# play_game prints the welcome screen and starts the game
def play_game():
    # init makes sure that colorama works on various platforms
    init()

    adventurer = Player()
    current_game = Game(adventurer)
    current_game.room = generate_room()
    welcome()

    # get player input
    input(f"{Fore.CYAN}Press ENTER to continue")
    current_game.room.print_description()
    explore_labyrinth(current_game)


# generate a room
def generate_room() -> Room:
    items = []
    monster = {}

    # there is a 25% chance that this room has an item
    if random.randint(1, 100) < 26:
        item = random.choice(list(armory.items.values()))
        items.append(item)

    # there is a 25% chance that this room has a monster
    if random.randint(1, 100) < 26:
        monster = random.choice(bestiary.monsters)

    return Room(items, monster)


# explore_labyrinth is the main game loop, which takes user input and then performs specific actions based
# on that input
def explore_labyrinth(current_game: Game):
    while True:
        # TODO: add logic to not print out the item and monster after every "get", "drop", "inventory"
        for item in current_game.room.items:
            print(f"{Fore.YELLOW}You see a {item['name']}")

        if current_game.room.monster:
            print(f"{Fore.RED}There is a {current_game.room.monster['name']} here!")
            fight_or_flee = get_input("Do you want to fight or flee?", ["fight", "flee"])

            while True:
                if fight_or_flee == "flee":
                    # user runs away
                    print(f"{Fore.CYAN}You turn around and run, coward that you are..")
                    break
                else:
                    # user wants to fight!

                    # call a function fight() and get a result  in a variable called winner
                    # winner = combat.fight()
                    # if winner is player, player wins; if it's monster, monster wins and if its flee,
                    # the player runs away
                    pass

        player_input = input(f"{Fore.YELLOW}-> ").lower().strip()

        # do something with that input
        if player_input in ["help", "h"]:
            show_help()

        elif player_input in ["look", "l"]:
            current_game.room.print_description()
            continue


        # picking up an item
        elif player_input.startswith("get"):
            if not current_game.room.items:
                print("There is nothing to pick up..")
                continue
            else:
                get_an_item(current_game, player_input)
                continue


        elif player_input in ["inventory", "inv"]:
            show_inventory(current_game)
            continue

        elif player_input.startswith("drop"):
            # TODO: add message "What do you want to drop?" if no item is specified after "drop"
            drop_an_item(current_game, player_input)
            continue

        elif player_input.startswith("equip"):
            use_item(current_game.player, player_input[6:])
            continue

        elif player_input.startswith("use"):
            use_item(current_game.player, player_input[4:])
            continue

        elif player_input.startswith("wear"):
            use_item(current_game.player, player_input[5:])
            continue

        elif player_input.startswith("unequip"):
            unequip_item(current_game.player, player_input[8:])
            continue

        elif player_input.startswith("remove"):
            unequip_item(current_game.player, player_input[7:])
            continue


        # moving around the map
        elif player_input in ["n", "s", "e", "w"]:
            print(f"{Fore.GREEN}You move deeper into the dungeon.")

        elif player_input == "status":
            print_status(current_game)
            continue

        # quit the game
        elif player_input in ["quit", "q"]:
            print(f"{Fore.GREEN}Overcome with terror, you flee the dungeon, and are forever branded a coward.")
            # TODO: print out final score
            play_again()

        elif player_input == "":
            continue

        # default case - The player entered a not recognized command
        else:
            print(f"{Fore.GREEN}I'm not sure what you mean.. Type 'help' for help.")

        current_game.room = generate_room()
        current_game.room.print_description()


def print_status(current_game: Game):
    print(Fore.CYAN)
    print(f"You have played the game for {current_game.player.turns} turns, "
          + f"defeated {current_game.player.monsters_defeated} monsters, "
          + f"and found {current_game.player.treasure} gold pieces.")
    print(f"You have earned {current_game.player.xp} xp.")
    print(f"You have {current_game.player.hp} hit points remaining, out of 100.")
    print(f"Currently equipped weapon: {current_game.player.current_weapon['name']}.")
    print(f"Currently equipped shield: {current_game.player.current_shield['name']}.")
    print(f"Currently equipped armor: {current_game.player.current_armor['name']}.")


def unequip_item(player: Player, item: str):
    if item in player.inventory:
        # is the item actually equipped?
        if player.current_weapon["name"] == item:
            player.current_weapon = armory.default["hands"]
            print(f"{Fore.CYAN}You stop using the {item}")
        elif player.current_armor["name"] == item:
            player.current_weapon = armory.default["clothes"]
            print(f"{Fore.CYAN}You stop using the {item}")
        elif player.current_shield["name"] == item:
            player.current_weapon = armory.default["no shield"]
            print(f"{Fore.CYAN}You stop using the {item}")
        else:
            print(f"{Fore.RED}You don't have a {item} equipped!")
    else:
        print(f"{Fore.RED}You don't have a {item}!")


def use_item(player: Player, item: str):
    if item in player.inventory:
        old_weapon = player.current_weapon

        if armory.items[item]["type"] == "weapon":
            # TODO: add case of having worn no weapon(hands), so "hands" doesnt get "removed"
            # "You arm yourself with a broadsword instead of your hands."
            player.current_weapon = armory.items[item]
            print(f"{Fore.CYAN}You arm yourself with a {player.current_weapon['name']} "
                  + f"instead of your {old_weapon['name']}.")

            if item == "longbow" and player.current_shield["name"] != "no shield":
                player.current_shield = armory.default["no shield"]
                print(f"{Fore.CYAN}Since you can't use a shield with the {item}, you sling it over your back.")

        elif armory.items[item]["type"] == "armor":
            # TODO: handle if player already wears a different armor
            player.current_armor = armory.items[item]
            print(f"{Fore.CYAN}You put on the {player.current_armor['name']}.")

        elif armory.items[item]["type"] == "shield":
            # TODO: handle if player already holds a different shield
            if player.current_weapon["name"] == "longbow":
                print(f"{Fore.RED}You can't use a shield while you are using a bow!")
            else:
                player.current_shield = armory.items[item]
                print(f"{Fore.CYAN}You equip the {player.current_shield['name']}.")

        else:
            print(f"{Fore.RED}You can't use a {item} as armor, weapon or shield.")

    else:
        print(f"{Fore.RED}You don't have a {item}.")


def drop_an_item(current_game: Game, player_input: str):
    # TODO: remove item stats from player, if worn item is dropped
    try:
        if current_game.player.current_weapon["name"] == player_input[5:] or current_game.player.current_armor[
            "name"] == player_input[5:] or current_game.player.current_shield["name"] == player_input[5:]:
            print(f"{Fore.RED}You can not drop an item that you are currently wearing!")
        else:
            current_game.player.inventory.remove(player_input[5:])
            print(f"{Fore.CYAN}You drop the {player_input[5:]}.")
            current_game.room.items.append(armory.items[player_input[5:]])
    except ValueError:
        print(f"{Fore.RED}You are not carrying a {player_input[5:]}!")


def show_inventory(current_game: Game):
    # TODO: add <worn> and <held> as prefix to item name, if item in inventory is currently used
    print(f"{Fore.CYAN}Your inventory:")
    print(f"    - {current_game.player.treasure} pieces of gold.")

    for x in current_game.player.inventory:
        if x == current_game.player.current_weapon["name"]:
            print(f"    - {x.capitalize()} (equipped).")
        elif x == current_game.player.current_armor["name"]:
            print(f"    - {x.capitalize()} (equipped).")
        elif x == current_game.player.current_shield["name"]:
            print(f"    - {x.capitalize()} (equipped).")
        else:
            print(f"    - {x.capitalize()}.")


# triggered by the player trying to pick up an item, the function checks if there IS an item in the current room
def get_an_item(current_game, player_input):
    if len(current_game.room.items) > 0 and player_input[4:] == "":
        player_input = player_input + " " + current_game.room.items[0]["name"]

    if player_input[4:] not in current_game.player.inventory:
        idx = find_in_list(player_input[4:], "name", current_game.room.items)

        if idx > -1:
            cur_item = current_game.room.items[idx]
            current_game.player.inventory.append(cur_item["name"])
            current_game.room.items.pop(idx)
            print(f"{Fore.CYAN}You pick up the {cur_item['name']}")
        else:
            print(f"{Fore.RED}There is no {player_input[4:]} here!")

    else:
        print(f"{Fore.YELLOW}You already have a {player_input[4:]}, and decide you don't need another one.")


def find_in_list(search_string: str, key: str, list_to_search: list) -> int:
    idx = -1
    count = 0
    for item in list_to_search:
        if item[key] == search_string:
            idx = count
        count = count + 1
    return idx


# play_again allows the user to stop playing, and quit or restart the game
def play_again():
    yn = get_yn(Fore.YELLOW + "Do you want to play again?")
    if yn == "yes":
        play_game()
    else:
        print("Until next time, adventurer.")
        exit(0)


# get_yn takes a question as a parameter and only accepts yes/no/y/n as possible responses.
# It returns either yes or no
def get_yn(question: str) -> str:
    while True:
        answer = input(question + " (yes / no) -> ").lower().strip()
        if answer not in ["yes", "no", "y", "n"]:
            print("Please enter yes or no.")
        else:
            if answer == "y":
                answer = "yes"
            elif answer == "n":
                answer = "no"
            return answer


# get_input prompts the user for input, and limits responses to whatever is in the list "answers"
def get_input(question: str, answers: list) -> str:
    while True:
        resp = input(f"{Fore.CYAN}{question} -> ").lower().strip()
        if resp not in answers:
            print(f"{Fore.CYAN}Please enter a valid response.")
        else:
            return resp


# show_help prints the help text
def show_help():
    print(Fore.GREEN + """Enter a command:
    - n/s/e/w: move in a direction
    - map: show a map of the labyrinth
    - look: look around and describe your environment
    - equip <item>: use an item from your inventory
    - unequip <item>: stop using an item from your inventory
    - fight: attack a foe
    - examine <object>: examine an object more closely
    - get <item>: pick up an item
    - drop <item>: drop the item
    - rest: restore some health by resting
    - inventory: show your inventory
    - status: show current player status
    - quit: end the game""")
