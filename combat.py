import random
import config as cfg

from classes import Game
from colorama import Fore
from time import sleep
from util import get_yn


def fight(current_game: Game) -> str:
    room = current_game.room
    player = current_game.player

    # assume the player goes first
    players_turn = True

    # roll for initiative or flip a coin
    if random.randint(1, 2) == 2:
        players_turn = False

    if players_turn:
        print(f"{Fore.CYAN}You brace yourself and attack the {room.monster['name']}.")
    else:
        print(f"{Fore.CYAN}The {room.monster['name']} moves quickly and attacks first!")

    # get the monsters hit points
    monster_hp = random.randint(room.monster["min_hp"], room.monster["max_hp"])
    monster_original_hp = monster_hp

    # TODO: adjust attacks rolls for player and monster based on the stats of the weapons, armor, etc.

    winner = ""

    while True:
        if players_turn:
            my_roll = random.randint(1, 100)
            modified_roll = my_roll + player.current_weapon["to_hit"] - room.monster["armor_modifier"]

            # given a base 50% chance to hit
            if modified_roll > 50:
                print(f"{Fore.GREEN}You hit the {room.monster['name']} with your {player.current_weapon['name']}!")
                monster_hp = monster_hp - random.randint(player.current_weapon["min_damage"],
                                                         player.current_weapon["max_damage"])
            else:
                print(f"{Fore.GREEN}You hit the {room.monster['name']} and miss!")

            if monster_hp <= 0:
                print(f"{Fore.GREEN}The {room.monster['name']} falls to the floor, dead.")
                winner = "player"
        else:
            # monster's turn
            monster_roll = random.randint(1, 100)
            modified_monster_roll = monster_roll - (player.current_shield["defense"] + player.current_armor["defense"])

            if modified_monster_roll > 50:
                print(f"{Fore.RED}The {room.monster['name']} attacks and hits")
                player.hp = player.hp - random.randint(room.monster["min_damage"], room.monster["max_damage"])
            else:
                print(f"{Fore.RED}The {room.monster['name']} attacks and misses!")

            if player.hp <= 0:
                print(f"{Fore.RED}The {room.monster['name']} kills you, and you fall to the floor, dead.")
                winner = "monster"

        # check to see if someone died; if so, the battle is over
        if player.hp <= 0 or monster_hp <= 0:
            break

        # let the player know how the monster is doing
        if monster_hp < monster_original_hp / 2:
            print(f"{Fore.YELLOW}The {room.monster['name']} is bleeding profusely.")
        elif monster_hp < monster_original_hp / 3:
            print(f"{Fore.YELLOW}The {room.monster['name']} is bleeding profusely, and looks to be nearly dead.")

        # give the player a warning and a chance to run away if they are badly wounded
        if player.hp <= int(0.2 * cfg.PLAYER_HP):
            answer = get_yn(f"{Fore.RED}You are near death. Do you want to continue?")
            if answer == "no":
                return "flee"

        elif player.hp <= int(0.3 * cfg.PLAYER_HP):
            answer = get_yn(f"{Fore.RED}You are badly wounded. Do you want to continue?")
            if answer == "no":
                return "flee"

        # elif player.hp <= int(0.5 * cfg.PLAYER_HP):
        #     answer = get_yn(f"{Fore.RED}You are lightly wounded. Do you want to continue?")
        #     if answer == "no":
        #         return "flee"

        elif player.hp < cfg.PLAYER_HP:
            print(f"{Fore.GREEN}You are only lightly wounded. 'This but a scratch.")

        sleep(1)
        print(f"{Fore.GREEN}")

        players_turn = not players_turn

    return winner
