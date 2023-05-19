import game
from classes import Game
import config as cfg


def create_world(current_game: Game) -> (dict, int):
    # initialize an empty dict and a counter
    rooms: dict = {}
    monsters: int = 0

    # we need to create a room for every entry on the map, so we
    # use a for loop (for y axis) with a nested for loop (x axis)
    # using values from config.py

    # for y in (5, -6, -1)
    for y in range(cfg.MAX_Y_AXIS, (cfg.MAX_Y_AXIS + 1) * -1, -1):
        for x in range(cfg.MAX_X_AXIS * -1, cfg.MAX_X_AXIS + 1):
            # we have enough info for location on grid
            room = game.generate_room(f"{x},{y}")

            if room.monster:
                monsters = monsters + 1

            # add it to the dictionary of rooms
            rooms[f"{x},{y}"] = room

    # at this point, the entire map is populated
    return rooms, monsters
