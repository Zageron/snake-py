#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""

from typing_extensions import TypeAlias
import pygame as pg
from enum import Enum
import random

WINSIZE = [320, 320]
CENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]

Coordinate: TypeAlias = tuple[int, int]


class Direction(Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4


class Stage(object):
    width: int
    height: int
    food: Coordinate


class Snake(object):
    def __init__(self, starting_position: Coordinate, starting_direction: Direction):
        self.__positions = list()
        self.__positions += starting_position
        self.__direction = starting_direction
        self.__length = 1

    def get_direction(self) -> Direction:
        return self.__direction

    def set_direction(self, new_direction) -> None:
        self.__direction = new_direction

    def get_length(self) -> int:
        return self.__length

    def get_positions(self) -> list[Coordinate]:
        return self.__positions

    length: int = property(get_length)
    positions: list[Coordinate] = property(get_positions)
    direction: Direction = property(get_direction, set_direction)


def move_snake(stage: Stage, snake: Snake) -> None:
    pass


def draw_snake(snake: Snake) -> None:
    print("Snake is length: %s", snake.length)
    print("Snake has positions at: ", end="")
    print(*snake.position, sep=", ")


def update_fps(clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pg.Color("coral"))
    return fps_text


def main():
    "This is the starfield code"

    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("Snake")

    black: tuple[int, int, int] = (20, 20, 40)
    screen.fill(black)

    clock = pg.time.Clock()
    font = pg.font.SysFont("Arial", 18)

    stage = Stage()
    snake = Snake(CENTER, random.choice(list(Direction)))

    accumulated_time = 0
    done = 0
    while not done:
        dt = clock.tick(120)
        accumulated_time += dt
        screen.fill(black)
        screen.blit(update_fps(clock, font), (10, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:  # Usually wise to be able to close your program.
                raise SystemExit
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    print("Player moving up!")
                elif event.key == pg.K_a:
                    print("Player moving left!")
                elif event.key == pg.K_s:
                    print("Player moving down!")
                elif event.key == pg.K_d:
                    print("Player moving right!")

        move_snake(stage, snake)
        draw_snake(snake)

        pg.display.update()
    pg.quit()


if __name__ == "__main__":
    main()
