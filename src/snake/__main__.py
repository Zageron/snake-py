#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""

import math
import os
import random
from enum import IntEnum

import pygame as pg
import pygame_gui
from pygame_gui.elements.ui_text_box import UITextBox
from typing_extensions import TypeAlias

from snake.score import Score

WINSIZE = [880, 880]
CENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]
GRID_SIZE = 11
CELL_SIZE = WINSIZE[0] / GRID_SIZE
GRID_LIST = [iter for iter in range(GRID_SIZE * GRID_SIZE)]

BLACK: pg.Color = pg.Color(20, 20, 40)
RED: pg.Color = pg.Color(200, 50, 50)
GREEN: pg.Color = pg.Color(50, 200, 50)

Coordinate: TypeAlias = tuple[int, int]


class Direction(IntEnum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    NONE = 5


class State(IntEnum):
    RESTART = 1
    START = 2
    PLAY = 3
    QUIT = 4


class Snake(object):
    def __init__(self, starting_position: Coordinate, starting_direction: Direction):
        self.__positions = list([starting_position] * 3)
        self.__direction = starting_direction

    def __get_direction(self) -> Direction:
        return self.__direction

    def __set_direction(self, new_direction) -> None:
        if self.__test_direction_is_good(new_direction):
            self.__direction = new_direction

    def __get_length(self) -> int:
        return len(self.__positions)

    def __get_positions(self) -> list[Coordinate]:
        return self.__positions

    length: int = property(__get_length)
    positions: list[Coordinate] = property(__get_positions)
    direction: Direction = property(__get_direction, __set_direction)

    def first_position(self) -> Coordinate:
        return self.__positions[0]

    def __test_direction_is_good(self, new_direction: Direction) -> bool:
        if self.__get_length() == 1:
            return True

        prev_position = self.__positions[1]
        next_position = get_new_coordinate(self.first_position(), new_direction)
        return prev_position != next_position

    def __contains_coordinate(self, position: Coordinate):
        return position in self.__positions

    def grow(self) -> None:
        self.__positions.append(self.__positions[-1])

    def update_positions(self) -> bool:
        first_pos: Coordinate = self.first_position()
        new_position: Coordinate = get_new_coordinate(first_pos, self.direction)

        if self.__contains_coordinate(new_position):
            return False
        else:
            self.__positions = self.__positions[:-1]
            self.__positions.insert(0, get_new_coordinate(first_pos, self.direction))
            return True


class Stage(object):
    def __init__(self, size: int, snake: Snake) -> None:
        self.__cells_wide = size
        self.__cells_high = size
        self.reset_food(snake)

    def reset_food(self, snake) -> None:
        snake_list = set([pos[0] * pos[1] for pos in snake.positions])
        choices_for_food: list(int) = list(
            set(GRID_LIST).symmetric_difference(snake_list)
        )

        selection = random.choice(choices_for_food)
        rand_x: int = selection % 11
        rand_y: int = math.floor(selection / GRID_SIZE)

        self.__food_coordinate = Coordinate([rand_x, rand_y])

    def __get_cells_wide(self) -> int:
        return self.__cells_wide

    def __get_cells_high(self) -> int:
        return self.__cells_high

    def __get_food_coordinate(self) -> Coordinate:
        return self.__food_coordinate

    cells_wide: int = property(__get_cells_wide)
    cells_high: int = property(__get_cells_high)
    food_coordinate: int = property(__get_food_coordinate)


def get_new_coordinate(coordinate: Coordinate, direction: Direction) -> Coordinate:
    if direction == Direction.UP:
        return (coordinate[0], coordinate[1] - 1)
    elif direction == Direction.LEFT:
        return (coordinate[0] - 1, coordinate[1])
    elif direction == Direction.DOWN:
        return (coordinate[0], coordinate[1] + 1)
    elif direction == Direction.RIGHT:
        return (coordinate[0] + 1, coordinate[1])


def check_out_of_bounds(stage: Stage, snake: Snake) -> bool:
    front_of_snake: Coordinate = snake.first_position()
    return not (
        front_of_snake[0] < 0
        or front_of_snake[0] >= stage.cells_wide
        or front_of_snake[1] < 0
        or front_of_snake[1] >= stage.cells_high
    )


def move_snake(stage: Stage, snake: Snake) -> bool:
    return snake.update_positions() and check_out_of_bounds(stage, snake)


def snake_check_food(stage: Stage, snake: Snake) -> bool:
    food_pos = stage.food_coordinate
    snake_pos = snake.positions[0]

    if food_pos == snake_pos:
        return True


def draw_snake(screen, snake: Snake) -> None:
    for coordinate in snake.positions:
        snake_square = pg.Rect(
            coordinate[0] * WINSIZE[0] / GRID_SIZE,
            coordinate[1] * WINSIZE[1] / GRID_SIZE,
            WINSIZE[0] / GRID_SIZE,
            WINSIZE[1] / GRID_SIZE,
        )
        pg.draw.rect(screen, GREEN, snake_square)


def draw_food(screen, stage: Stage) -> None:
    food_square = pg.Rect(0, 0, WINSIZE[0] / GRID_SIZE, WINSIZE[1] / GRID_SIZE)
    coordinate = stage.food_coordinate
    food_square.x = coordinate[0] * food_square.width
    food_square.y = coordinate[1] * food_square.height
    pg.draw.rect(screen, RED, food_square)


def update_score_box(
    score_box: UITextBox, hiscore: int, currentScore: int
) -> UITextBox:
    score_box.html_text = (
        "<font face=fira_mono color=#A784E2 size=4>"
        f"High Score: {hiscore}"
        "<br>"
        f"Current Score: {currentScore}"
        "</font>"
    )
    score_box.rebuild()


def main():
    "This is the starfield code"

    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("Snake")
    screen.fill(BLACK)

    clock = pg.time.Clock()

    print(f" get cwd: {os.getcwd()}")
    print(f" get cwd: {os.getcwd()}/data/theme.json")

    # PyGame GUI
    manager = pygame_gui.UIManager(
        (WINSIZE[0], WINSIZE[1]),
        theme_path="./data/theme.json",
    )

    manager.preload_fonts(
        [
            {"name": "fira_code", "point_size": 16, "style": "regular"},
        ]
    )

    how_to_play_info_box = UITextBox(
        "<font face=fira_code color=#E784A2 size=4.5>Welcome to PYTHON</font>"
        "<font face=fira_code>"
        "<br> <br>"
        "Use WASD or the arrow keys to control the snake."
        "<br> <br>"
        "If the snake hits the edge or itself it will die. Collect apples!"
        "<br> <br>"
        "Press any movement key to start moving in that direction!"
        "</font>",
        pg.Rect((75, 75), (300, 300)),
        manager=manager,
        object_id="#play_box",
    )

    score_box = UITextBox(
        "",
        pg.Rect((WINSIZE[1] - 250 - 25, 25), (250, 70)),
        manager=manager,
        object_id="#score_box",
        visible=False,
    )
    update_score_box(score_box, 0, 0)

    state: State = State.RESTART

    score: Score = Score()

    tick_length: int = 250

    accumulated_time: int = 0
    should_redraw: bool = True
    done: bool = False
    while not done:

        # Input
        direction: Direction = Direction.NONE
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Usually wise to be able to close your program.
                raise SystemExit
            elif event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    raise SystemExit
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w or event.key == pg.K_UP:
                    direction = Direction.UP
                elif event.key == pg.K_a or event.key == pg.K_LEFT:
                    direction = Direction.LEFT
                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    direction = Direction.DOWN
                elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                    direction = Direction.RIGHT
            manager.process_events(event)

        # Timer
        dt = clock.tick(60)
        accumulated_time += dt

        # State
        if state == State.RESTART:
            score.reset_score()
            how_to_play_info_box.visible = True
            score_box.visible = False
            update_score_box(score_box, score.hiscore, score.score)
            snake = Snake((5, 5), random.choice(list(Direction)))
            stage = Stage(GRID_SIZE, snake)
            state = State.START

        elif state == State.START:
            if direction != Direction.NONE:
                snake.direction = direction
                accumulated_time = tick_length
                state = State.PLAY
                how_to_play_info_box.visible = False
                score_box.visible = True
                how_to_play_info_box.rebuild()
                score_box.rebuild()

        elif state == State.PLAY:  # Play Game
            if direction != Direction.NONE:
                snake.direction = direction

            if accumulated_time >= tick_length:
                accumulated_time -= tick_length
                should_redraw = True

                if move_snake(stage, snake):
                    got_food: bool = snake_check_food(stage, snake)
                    if got_food:
                        snake.grow()
                        stage.reset_food(snake)
                        score.increase_score()
                        update_score_box(score_box, score.hiscore, score.score)
                else:
                    state = State.RESTART
        else:  # state == State.QUIT
            done = 1
            break

        manager.update(dt)

        # Draw
        if state == State.START:
            # Draw some text to inform the user what to do.
            screen.fill(BLACK)
            draw_snake(screen, snake)
            manager.draw_ui(screen)
            pg.display.flip()
            pass
        elif state == State.PLAY:
            if should_redraw:
                should_redraw = False
                screen.fill(BLACK)
                draw_snake(screen, snake)
                draw_food(screen, stage)
                manager.draw_ui(screen)
                pg.display.flip()
        else:
            # Do not draw.
            pass

    pg.quit()


if __name__ == "__main__":
    main()
