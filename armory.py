# items is a dictionary of all possible items in the game
items = {
    "longsword": {
        "name": "longsword",
        "min_damage": 5,
        "max_damage": 25,
        "to_hit": 25,
        "type": "weapon",
    },
    "dagger": {
        "name": "dagger",
        "min_damage": 1,
        "max_damage": 10,
        "to_hit": 10,
        "type": "weapon",
    },
    "flail": {
        "name": "flail",
        "min_damage": 10,
        "max_damage": 25,
        "to_hit": 15,
        "type": "weapon",
    },
    "mace": {
        "name": "mace",
        "min_damage": 10,
        "max_damage": 30,
        "to_hit": 15,
        "type": "weapon",
    },
    "broadsword": {
        "name": "broadsword",
        "min_damage": 10,
        "max_damage": 25,
        "to_hit": 20,
        "type": "weapon",
    },
    "broken sword": {
        "name": "broken sword",
        "min_damage": 2,
        "max_damage": 10,
        "to_hit": 0,
        "type": "weapon",
    },
    "longbow": {
        "name": "longbow",
        "min_damage": 5,
        "max_damage": 20,
        "to_hit": 20,
        "type": "weapon",
    },
    "glowing sword": {
        "name": "glowing sword",
        "min_damage": 20,
        "max_damage": 50,
        "to_hit": 25,
        "type": "weapon",
    },
    "battered shield": {
        "name": "battered shield",
        "defense": 5,
        "type": "shield",
    },
    "tower shield": {
        "name": "tower shield",
        "defense": 25,
        "type": "shield",
    },
    "kite shield": {
        "name": "kite shield",
        "defense": 20,
        "type": "shield",
    },
    "round shield": {
        "name": "round shield",
        "defense": 15,
        "type": "shield",
    },
    "small shield": {
        "name": "small shield",
        "defense": 10,
        "type": "shield",
    },
    "leather armor": {
        "name": "leather armor",
        "defense": 10,
        "type": "armor",
    },
    "chain mail": {
        "name": "chain mail",
        "defense": 20,
        "type": "armor",
    },
    "ring mail": {
        "name": "ring mail",
        "defense": 15,
        "type": "armor",
    },
    "water skin": {
        "name": "water skin",
        "type": "item",
    },
    "penny": {
        "name": "penny",
        "type": "item",
    },
}

# default is a dictionary of default items the player has. This is only used at game start,
# and if the player drops armor or shield
default = {
    "hands": {
        "name": "hands",
        "min_damage": 1,
        "max_damage": 5,
        "to_hit": 0,
        "type": "weapon",
    },
    "clothes": {
        "name": "clothes",
        "defense": 0,
        "type": "armor",
    },
    "no shield": {
        "name": "no shield",
        "defense": 0,
        "type": "shield",
    },
}
