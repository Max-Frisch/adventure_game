import armory
import bestiary
import combat
import cursor
import random
import sys
import world
from classes import Game, Player, Room
from colorama import Fore, init, Back
from util import get_yn
from util import draw_ui
from time import sleep
import config as cfg


# welcome prints out the welcome text
def welcome(current_game: Game):
    cursor.hide()
    print(Fore.RED + "                                               D U N G E O N")
    print(Fore.GREEN + """
    The village of Honeywood has been terrorized by strange, deadly creatures for months now. Unable to endure any
    longer, the villagers pooled their wealth and hired the most skilled adventurer they could find: you. After
    listening to their tale of woe, you agree to enter the labyrinth where most of the creatures seem to originate,
    and destroy the foul beasts. Armed with a longsword and a bundle of torches, you descend into the labyrinth,
    ready to do battle....""")

    print()
    print(
        f"    According to the people of Honeywood, there are {current_game.num_monsters} creatures in this labyrinth.")
    print()
    sleep(1.5)

    print(f"{Fore.YELLOW}    Something smashes into the back of your head, and you fall down, senseless..")
    print()

    for x in range(45):
        print(" ", end="")

    for x in range(12):
        print(f"{Fore.YELLOW}.", end="")
        sys.stdout.flush()
        sleep(0.25)
    print()

    print(Fore.GREEN + """
    You awaken, some unknown time later, only to discover that nearly all of your possessions are missing. 
    You grid  your teeth, climb to your feet, and press on, determined to complete your mission.""")
    print()


# play_game prints the welcome screen and starts the game
def play_game(term):
    # init makes sure that colorama works on various platforms
    init()

    adventurer = Player()
    current_game = Game(adventurer, cfg.MAX_X_AXIS, cfg.MAX_Y_AXIS, term)

    all_rooms, num_monsters = world.create_world(current_game)
    current_game.num_monsters = num_monsters
    current_game.set_rooms(all_rooms)

    entrance = "0,0"
    current_game.set_current_room(current_game.rooms[entrance])
    current_game.set_entrance(entrance)
    current_game.room.location = entrance

    # draw the top status bar
    draw_ui(current_game)

    welcome(current_game)

    # get player input
    cursor.show()
    print(f"{Fore.CYAN}(Type help or h to get a list of the available commands.)")
    input(f"{Fore.CYAN}Press ENTER to continue")
    print()
    current_game.room.print_description()
    explore_labyrinth(current_game)


# generate a room
def generate_room(location: str) -> Room:
    items = []
    monster = {}

    # there is a 25% chance that this room has an item
    if random.randint(1, 100) < 26:
        item = random.choice(list(armory.items.values()))
        items.append(item)

    # there is a 25% chance that this room has a monster
    if random.randint(1, 100) < 26:
        monster = random.choice(bestiary.monsters)

    return Room(items, monster, location)


# explore_labyrinth is the main game loop, which takes user input and then performs specific actions based
# on that input
def explore_labyrinth(current_game: Game):
    while True:
        # TODO: add some kind of animated text, after the player has defeated all monsters.
        for item in current_game.room.items:
            print(f"{Fore.YELLOW}You see a {item['name']}")

        # TODO: Consider changing logic, so that the first room the player spawns in can not
        #       contain a monster
        if current_game.room.monster:
            print(f"{Fore.RED}There is a {current_game.room.monster['name']} here!")

            # draw the top status bar
            draw_ui(current_game)

            fight_or_flee = get_input("Do you want to fight or flee?", ["fight", "flee"])

            while True:
                if fight_or_flee == "flee":
                    # user runs away
                    print(f"{Fore.CYAN}You turn around and run, coward that you are..")

                    # draw the top status bar
                    draw_ui(current_game)

                    break
                else:
                    # user wants to fight!

                    # call a function fight() and get a result  in a variable called winner
                    winner = combat.fight(current_game)

                    # draw the top status bar
                    draw_ui(current_game)

                    # if winner is player, player wins; if it's monster, monster wins and if its flee,
                    # the player runs away
                    if winner == "player":
                        gold = random.randint(1, 100)
                        print(f"You search the monster's dead body and find {gold} pieces of gold.")
                        current_game.player.treasure = current_game.player.treasure + gold
                        current_game.player.xp = current_game.player.xp + 100
                        current_game.player.monsters_defeated = current_game.player.monsters_defeated + 1
                        current_game.room.monster = {}

                        # draw the top status bar
                        draw_ui(current_game)
                        break

                    elif winner == "monster":
                        print(f"{Fore.RED}You have failed on your mission, and your body lies in the "
                              + "labyrinth forever.")

                        # draw the top status bar
                        draw_ui(current_game)

                        play_again()
                        break
                    else:
                        print(f"{Fore.CYAN}You flee in terror from the monster.")

                        # draw the top status bar
                        draw_ui(current_game)
                        break

        # draw the top status bar
        draw_ui(current_game)

        player_input = input(f"{Fore.YELLOW}-> ").lower().strip()

        # do something with that input
        if player_input in ["help", "h"]:
            show_help()
            continue

        elif player_input in ["look", "l"]:
            current_game.room.print_description()
            continue

        elif player_input.startswith("examine"):
            examine(player_input[8:])
            continue

        elif player_input in ["map", "m"]:
            show_map(current_game)
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

        elif player_input in ["rest", "r"]:
            rest(current_game)
            continue

        elif player_input.startswith("remove"):
            unequip_item(current_game.player, player_input[7:])
            continue


        # moving around the map
        elif player_input in ["n", "s", "e", "w"]:
            direction = player_input

            if current_game.room.location == current_game.entrance and direction == "s":
                yn = get_yn(f"{Fore.CYAN}You are about to leave the dungeon; are you sure?")
                if yn != "yes":
                    continue
                else:
                    play_again()

            if direction == "n":
                if current_game.player.y_coord < current_game.y:
                    current_game.player.y_coord = current_game.player.y_coord + 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            elif direction == "s":
                if current_game.player.y_coord > current_game.y * -1:
                    current_game.player.y_coord = current_game.player.y_coord - 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            elif direction == "e":
                if current_game.player.x_coord < current_game.x:
                    current_game.player.x_coord = current_game.player.x_coord + 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            elif direction == "w":
                if current_game.player.x_coord > current_game.x * -1:
                    current_game.player.x_coord = current_game.player.x_coord - 1
                else:
                    print(f"{Fore.RED}You bump into a stone wall.")
                    continue

            print(f"{Fore.GREEN}You move deeper into the dungeon.")

            # draw the top status bar
            draw_ui(current_game)


        elif player_input == "status":
            print_status(current_game)
            continue

        # quit the game
        elif player_input in ["quit", "q"]:
            print(f"{Fore.GREEN}Overcome with terror, you flee the dungeon, and are forever branded a coward.")
            print_final_score(current_game)
            play_again()

        elif player_input == "":
            continue

        # default case - The player entered a not recognized command
        else:
            print(f"{Fore.GREEN}I'm not sure what you mean.. Type 'help' for help.")

        new_location = f"{current_game.player.x_coord},{current_game.player.y_coord}"
        current_game.room = current_game.rooms[new_location]
        current_game.room.location = new_location

        if new_location in current_game.player.visited:
            print(f"{Fore.YELLOW}This place seems familiar..")
        else:
            current_game.player.visited.append(new_location)

        current_game.room.print_description()
        current_game.player.turns = current_game.player.turns + 1


# rest lets the player sit down and recover hit points periodically, until fully healed.
def rest(current_game: Game):
    # TODO: add option to interrupt resting with keypress
    if current_game.player.hp == cfg.PLAYER_HP:
        print(f"{Fore.CYAN}You are fully rested and feel great. There is no point in sitting around..")
    else:
        print(f"{Fore.CYAN}You sit down and recover from the battles you have fought..")
        cursor.hide()
        while True:
            current_game.player.hp = current_game.player.hp + random.randint(1, 10)
            if current_game.player.hp > cfg.PLAYER_HP:
                current_game.player.hp = cfg.PLAYER_HP
                print(f"{Fore.CYAN}Fully rested you stand back up, ready to continue.")
                break

            print(f"{Fore.CYAN}You feel better ({current_game.player.hp}/{cfg.PLAYER_HP} hit points).")
            sleep(2)
        cursor.show()


def examine(item: str):
    print(f"{Fore.CYAN}It's just a normal {item}. There is nothing special about it.")


# print_final_score prints out how many monsters were defeted in how many turns and how much
# gold and xp was collected.
def print_final_score(current_game: Game):
    print(f"{Fore.CYAN}In {current_game.player.turns} turns, you defeated {current_game.player.monsters_defeated} "
          + f"monsters, accumulated {current_game.player.treasure} gold, and made {current_game.player.xp} xp.")

    if current_game.player.xp > 500:
        print(f"{Fore.GREEN}Well done, adventurer.")
    elif current_game.player.xp > 250:
        print(f"{Fore.YELLOW}Not bad, adventurer.")
    else:
        print(f"{Fore.RED}I guess it's amateur night...")
    draw_ui(current_game)


# show_map prints a map grind with icons for current position, monster and exit
def show_map(current_game: Game):
    # print the top line
    for i in range(1, cfg.MAX_X_AXIS * 6 + 3):
        print(f"{Fore.YELLOW}-", end="")
    print()

    for y in range(cfg.MAX_Y_AXIS, (cfg.MAX_Y_AXIS + 1) * -1, -1):
        for x in range(cfg.MAX_X_AXIS * -1, cfg.MAX_X_AXIS + 1):
            content = ""
            if f"{x},{y}" == current_game.room.location:
                # our current location
                content = Fore.RED + Back.WHITE + " X " + Fore.YELLOW + Back.RESET
            elif f"{x},{y}" == current_game.entrance:
                content = Fore.GREEN + Back.WHITE + " E " + Fore.YELLOW + Back.RESET
            elif f"{x},{y}" in current_game.player.visited:
                # a place we've visited
                test_room = current_game.rooms[f"{x},{y}"]
                if test_room.monster:
                    content = Fore.RED + " M " + Fore.YELLOW
                else:
                    pass
            else:
                # a place we have not visited yet
                content = "?"

            print(Fore.YELLOW + f"{content.center(3)}", end="")

        print()

    # print the bottom line
    for i in range(1, cfg.MAX_X_AXIS * 6 + 3):
        print(f"{Fore.YELLOW}-", end="")
    print()

    # print the legend
    print(Fore.CYAN + "Legend: ", end="")
    print(Back.WHITE + Fore.RED + " X " + Back.RESET + ": You,", end="")
    print(Fore.RED + " M " + ": Monster, ", end="")
    print(Back.WHITE + Fore.GREEN + " E " + Back.RESET + ": Exit ", end="")
    print()


# print_status prints the current players status, as in monsters defeated, gold collected, xp gained,
# the players current hit points, as well as currently worn equipment.
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


# unequip_item unequips a currently worn item, as long the item exists in the inventory
# and the player currently wears it
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


# use_item equips an item from the players inventory, if the item exists
# and checks if this item is not already worn.
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
            player.current_armor = armory.items[item]
            print(f"{Fore.CYAN}You put on the {player.current_armor['name']}.")

        elif armory.items[item]["type"] == "shield":
            if player.current_weapon["name"] == "longbow":
                print(f"{Fore.RED}You can't use a shield while you are using a bow!")
            else:
                player.current_shield = armory.items[item]
                print(f"{Fore.CYAN}You equip the {player.current_shield['name']}.")

        else:
            print(f"{Fore.RED}You can't use a {item} as armor, weapon or shield.")

    else:
        print(f"{Fore.RED}You don't have a {item}.")


# drop_an_item drops an item from the players inventory. Can only drop an item, if it is not worn currently.
def drop_an_item(current_game: Game, player_input: str):
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


# show_inventory prints out all equipment currently in the players inventory, including gold coins.
def show_inventory(current_game: Game):
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
    - examine <object>: examine an object more closely
    - get <item>: pick up an item
    - drop <item>: drop the item (unequip first)
    - rest: restore some health by resting
    - inventory: show your inventory
    - status: show current player status
    - quit: end the game""")
