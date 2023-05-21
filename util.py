import config as cfg
from classes import Game


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


def draw_ui(current_game: Game):
    # print info bar across the entire window
    with current_game.term.location(0, 0):
        for i in range(current_game.term.width):
            print(current_game.term.on_green(" "), end="")

    # write health status on top of the bar
    with current_game.term.location(5, 0):
        print(current_game.term.black_on_green(f"Health: {current_game.player.hp}/{cfg.PLAYER_HP}"))

    # monsters defeated
    with current_game.term.location(30, 0):
        print(current_game.term.black_on_green(f"Monsters defeated: "
                                               + f"{current_game.player.monsters_defeated}/"
                                               + f"{current_game.num_monsters}"))

    # experience gained
    with current_game.term.location(60, 0):
        print(current_game.term.black_on_green(f"XP: {current_game.player.xp}"))
