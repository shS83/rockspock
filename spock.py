from enum import StrEnum
from random import choice
import sys

from keyboard import (
    KEY_LEFT,
    KEY_RIGHT,
    KEY_ENTER,
    KEY_ESCAPE,
    read_key,
    setup_keyboard,
    restore_keyboard,
)


class Combatants(StrEnum):
    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"
    LIZARD = "Lizard"
    SPOCK = "Spock"


c = Combatants


colors = {
    c.ROCK: "\033[33m",
    c.PAPER: "\033[37m",
    c.SCISSORS: "\033[36m",
    c.LIZARD: "\033[35m",
    c.SPOCK: "\033[34m",
}


RESET = "\033[0m"
UNDERLINE = "\033[4m"


combatant_list = list(c)

cpu_choice = choice(combatant_list)
player_choice = ""

selected = 0


combatants = {
    c.ROCK: {
        "beats": [c.SCISSORS, c.LIZARD],
    },
    c.PAPER: {
        "beats": [c.ROCK, c.SPOCK],
    },
    c.SCISSORS: {
        "beats": [c.PAPER, c.LIZARD],
    },
    c.LIZARD: {
        "beats": [c.PAPER, c.SPOCK],
    },
    c.SPOCK: {
        "beats": [c.SCISSORS, c.ROCK],
    },
}


def draw_combatants():
    print("\r\033[2K", end="")

    for i, val in enumerate(combatant_list):
        if i == selected:
            print(UNDERLINE, end="")

        print(f"{colors[val]}{val}{RESET}", end="")

        if i < len(combatant_list) - 1:
            print(", ", end="")

    sys.stdout.flush()


setup_keyboard()

try:
    draw_combatants()

    while player_choice == "":
        key = read_key()

        if key is None:
            continue

        if key == KEY_RIGHT:
            selected = (selected + 1) % len(combatant_list)
            draw_combatants()

        elif key == KEY_LEFT:
            selected = (selected - 1) % len(combatant_list)
            draw_combatants()

        elif key == KEY_ENTER:
            player_choice = combatant_list[selected]
            break

        elif key == KEY_ESCAPE:
            break

finally:
    restore_keyboard()


print()

def check_winner():
    global player_choice, cpu_choice
    print(f"You chose: {combatant_list[selected]}")
    if cpu_choice == player_choice:
        print(f"Computer: {cpu_choice}\nIT'S A TIE!")
        return
    elif cpu_choice in combatants[combatant_list[selected]]["beats"]:
        print(f"Computer: {cpu_choice}\nYOU WON!")
        return
    else:
        print(f"Computer: {cpu_choice}\nYOU LOST!")
        return
    return

check_winner()