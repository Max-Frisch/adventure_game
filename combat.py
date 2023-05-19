import random

from classes import Game
from colorama import Fore


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
