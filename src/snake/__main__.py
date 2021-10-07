#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""

import math
from typing_extensions import TypeAlias
import pygame as pg
from enum import IntEnum
import random

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


class Food(object):
    def __init(self) -> None:
        self.__min_size = 25
        self.__max_size = 100
        self.__steps = 3
        self.__current_step = 0

    def __get_current_size(self) -> int:
        return self.__

    def step_food_animation(self) -> None:
        self.__current_step = 0


class Snake(object):
    def __init__(self, starting_position: Coordinate, starting_direction: Direction):
        self.__positions = list()
        self.__positions.extend([starting_position])
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

    def __first_position(self) -> Coordinate:
        return self.__positions[0]

    def __test_direction_is_good(self, new_direction: Direction) -> bool:
        if self.__get_length() == 1:
            return True

        prev_position = self.__positions[1]
        next_position = get_new_coordinate(self.__first_position(), new_direction)
        return prev_position != next_position

    def __contains_coordinate(self, position: Coordinate):
        return position in self.__positions

    def grow(self) -> None:
        self.__positions.append(self.__positions[-1])

    def update_positions(self) -> bool:
        first_pos: Coordinate = self.__first_position()
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


def move_snake(stage: Stage, snake: Snake) -> bool:
    return snake.update_positions()


def snake_check_food(stage: Stage, snake: Snake) -> bool:
    food_pos = stage.food_coordinate
    snake_pos = snake.positions[0]

    if food_pos == snake_pos:
        return True


def draw_snake(screen, snake: Snake) -> None:
    print("Snake is length: %s" % snake.length)
    print("Snake has positions at: ", end="")
    print(*snake.positions, sep=", ")

    for coordinate in snake.positions:
        snake_square = pg.Rect(
            coordinate[0] * WINSIZE[0] / GRID_SIZE,
            coordinate[1] * WINSIZE[1] / GRID_SIZE,
            WINSIZE[0] / GRID_SIZE,
            WINSIZE[1] / GRID_SIZE,
        )
        pg.draw.rect(screen, GREEN, snake_square)


def draw_food(screen, stage: Stage, food: Food) -> None:
    food_square = pg.Rect(0, 0, WINSIZE[0] / GRID_SIZE, WINSIZE[1] / GRID_SIZE)
    coordinate = stage.food_coordinate
    food_square.x = coordinate[0] * food_square.width
    food_square.y = coordinate[1] * food_square.height
    pg.draw.rect(screen, RED, food_square)


def update_fps(clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pg.Color("coral"))
    return fps_text


def main():
    "This is the starfield code"

    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("Snake")
    screen.fill(BLACK)

    clock = pg.time.Clock()
    font = pg.font.SysFont("Arial", 18)

    state: State = State.RESTART

    tick_length: int = 750

    accumulated_time: int = 0
    should_redraw: bool = True
    done: bool = False
    while not done:

        # Input
        direction: Direction = Direction.NONE
        for event in pg.event.get():
            if event.type == pg.QUIT:  # Usually wise to be able to close your program.
                raise SystemExit
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    direction = Direction.UP
                elif event.key == pg.K_a:
                    direction = Direction.LEFT
                elif event.key == pg.K_s:
                    direction = Direction.DOWN
                elif event.key == pg.K_d:
                    direction = Direction.RIGHT

        # Timer
        dt = clock.tick(120)
        accumulated_time += dt

        # State
        if state == State.RESTART:
            snake: Snake = Snake((5, 5), random.choice(list(Direction)))
            stage: Stage = Stage(GRID_SIZE, snake)
            state = State.START
            food: Food = Food()
        elif state == State.START:
            if direction != Direction.NONE:
                snake.direction = direction
                accumulated_time = tick_length
                state = State.PLAY
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
                else:
                    state = State.RESTART
        else:  # state == State.QUIT
            done = 1
            break

        # Draw
        if state == State.START:
            # Draw some text to inform the user what to do.
            screen.fill(BLACK)
            screen.blit(update_fps(clock, font), (10, 0))
            pg.display.flip()
            pg.display.update()
            pass
        elif state == State.PLAY:
            if should_redraw:
                should_redraw = False
                screen.fill(BLACK)
                draw_snake(screen, snake)
                draw_food(screen, stage, food)
                screen.blit(update_fps(clock, font), (10, 0))
                pg.display.flip()
                pg.display.update()
        else:
            # Do not draw.
            pass

    pg.quit()


if __name__ == "__main__":
    main()
