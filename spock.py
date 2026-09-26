from enum import StrEnum
from random import choice
import time
import pygame as pg

pg.init()
clock = pg.time.Clock()

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

combatants = {
        c.ROCK: {
            "beats": [c.SCISSORS, c.LIZARD],
            "selected": True
        },
        c.PAPER: {
            "beats": [c.ROCK, c.SPOCK],
            "selected": False
        },
        c.SCISSORS: {
            "beats": [c.PAPER, c.LIZARD],
            "selected": False
        },
        c.LIZARD: {
            "beats": [c.PAPER, c.SPOCK],
            "selected": False
        },
        c.SPOCK: {
            "beats": [c.SCISSORS, c.ROCK],
            "selected": False
        }
}

def draw_combatants():
    print("\r\033[2K", end="")

    for i, val in enumerate(c):
        selected = combatants[val]["selected"]

        if selected:
            print(UNDERLINE, end="")

        print(f"{colors[val]}{val}{RESET}", end="")

        if i < len(c) - 1:
            print(", ", end="")

while player_choice == "":
    draw_combatants()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                break
            if event.key == pg.K_RIGHT:
                combatants[combatant_list[selected]]["selected"] = False
                selected = (selected + 1) % len(combatant_list)
                combatants[combatant_list[selected]]["selected"] = True

            if event.key == pg.K_LEFT:
                combatants[combatant_list[selected]]["selected"] = False
                selected = (selected - 1) % len(combatant_list)
                combatants[combatant_list[selected]]["selected"] = True

    clock.tick(60)