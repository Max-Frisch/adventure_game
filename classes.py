import armory
import descriptions
import random
from colorama import Fore
import config as cfg


class Player:
    def __init__(self):
        self.hp: int = cfg.PLAYER_HP
        self.treasure: int = 0
        self.monsters_defeated: int = 0
        self.xp: int = 0
        self.turns: int = 0
        self.inventory: list = []
        self.current_weapon: dict = armory.default["hands"]
        self.current_armor: dict = armory.default["clothes"]
        self.current_shield: dict = armory.default["no shield"]
        self.x_coord: int = 0
        self.y_coord: int = 0
        self.visited: list = []


class Room:
    def __init__(self, items: list, monster: dict, location: str):
        self.description: str = descriptions.descriptions[random.randrange(0, len(descriptions.descriptions) - 1)]
        self.sound: str = descriptions.sounds[random.randrange(0, len(descriptions.sounds) - 1)]
        self.smell: str = descriptions.smells[random.randrange(0, len(descriptions.smells) - 1)]
        self.items: list = items
        self.monster: dict = monster
        self.location: str = location

    def print_description(self):
        print(f"{Fore.GREEN}{self.description}")
        print(self.smell)
        print(self.sound)


class Game:
    def __init__(self, player: Player, x: int, y: int):
        self.player = player
        self.room = None
        self.num_monsters: int = 0
        self.rooms: dict = {}
        self.x: int = x
        self.y: int = y
        self.entrance: str = ""

    def set_rooms(self, rooms: dict):
        self.rooms = rooms

    def set_current_room(self, room: Room):
        self.room = room

    def set_entrance(self, entrance: str):
        self.entrance = entrance
