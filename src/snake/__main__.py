#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""

from typing_extensions import TypeAlias
import pygame as pg
from enum import Enum
import random

WINSIZE = [880, 880]
CENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]
GRID_SIZE = 11
CELL_SIZE = WINSIZE[0] / GRID_SIZE
GRID_LIST = [iter for iter in range(GRID_SIZE * GRID_SIZE)]

Coordinate: TypeAlias = tuple[int, int]


class Direction(Enum):
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    NONE = 5


class State(Enum):
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


class Stage(object):
    def __init__(self, size: int, first_food: Coordinate) -> None:
        self.__cells_wide = size
        self.__cells_high = size
        self.__food_coordinate = first_food

    def reset_food(self, snake) -> None:
        choices_for_food: list(int) = list(
            set(GRID_LIST).symmetric_difference(set(snake.positions))
        )

        rand_x: int = choices_for_food / GRID_SIZE
        rand_y: int = choices_for_food % 11

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


class Snake(object):
    def __init__(self, starting_position: Coordinate, starting_direction: Direction):
        self.__positions = list()
        self.__positions.extend([starting_position])
        self.__direction = starting_direction
        self.__length = 1

    def grow(self) -> None:
        self.length += 1

    def __get_direction(self) -> Direction:
        return self.__direction

    def __set_direction(self, new_direction) -> None:
        self.__direction = new_direction

    def __get_length(self) -> int:
        return self.__length

    def __get_positions(self) -> list[Coordinate]:
        return self.__positions

    length: int = property(__get_length)
    positions: list[Coordinate] = property(__get_positions)
    direction: Direction = property(__get_direction, __set_direction)


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
    snake.positions[0] = get_new_coordinate(snake.positions[0], snake.direction)
    if snake.length < len(snake.positions):
        print("The snake should grow now...")

    return True


def snake_check_food(stage: Stage, snake: Snake) -> bool:
    # Check
    pass


def draw_snake(screen, snake: Snake) -> None:
    print("Snake is length: %s" % snake.length)
    print("Snake has positions at: ", end="")
    print(*snake.positions, sep=", ")

    snake_square = pg.Rect(0, 0, WINSIZE[0] / GRID_SIZE, WINSIZE[1] / GRID_SIZE)
    coordinate = snake.positions[0]
    snake_square.x = coordinate[0] * snake_square.width
    snake_square.y = coordinate[1] * snake_square.height
    pg.draw.rect(screen, (150, 200, 20), snake_square)


def draw_food(stage: Stage, food: Food) -> None:
    # Stage for position
    # Food for animation state
    print("Food is at %s" % (stage.food_coordinate,))
    pass


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

    state: State = State.RESTART

    tick_length: int = 1000

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
            stage: Stage = Stage(GRID_SIZE, (5, 5))
            snake: Snake = Snake((5, 5), random.choice(list(Direction)))
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
            screen.fill(black)
            screen.blit(update_fps(clock, font), (10, 0))
            pg.display.flip()
            pg.display.update()
            pass
        elif state == State.PLAY:
            if should_redraw:
                should_redraw = False
                screen.fill(black)
                draw_snake(screen, snake)
                draw_food(stage, food)
                screen.blit(update_fps(clock, font), (10, 0))
                pg.display.flip()
                pg.display.update()
        else:
            # Do not draw.
            pass

    pg.quit()


if __name__ == "__main__":
    main()
