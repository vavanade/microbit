"""Snake game that is played by tilting the micro:bit.

Todo:
    * refactor drawing
    * music?
    * remove reset? it can be reset by the button on the back anyway
    * win condition
    * levels -> speeding up
"""

from microbit import *
import music
import random
import math


# helper function used for drawing a snake body that can be somewhat better distinguished
def period_switch(period):
    """returns 0s and 1s with a period given by period"""
    while True:
        for _ in range(period):
            yield 0
        for _ in range(period):
            yield 1


# this determines how fast the game is
loop_time_ms = 250

EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
NORTH = (0, -1)
DIRECTIONS = (EAST, SOUTH, WEST, NORTH)

PI_4 = math.pi / 4


EMPTY = 0
OBJECT = 6
HEAD = 8
BODY = 2

SIZE_X = SIZE_Y = 5

INITIAL_STATE = (
    (EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
    (EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
    (EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
    (EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
    (EMPTY, EMPTY, EMPTY, EMPTY, EMPTY),
)
INITIAL_DIRECTION = DIRECTIONS.index(EAST)


def get_direction():
    return get_direction_from_readings(
        accelerometer.get_x(),
        accelerometer.get_y(),
    )


def get_direction_from_readings(x, y):
    alpha = math.atan2(-y, x)
    if -PI_4 < alpha <= PI_4:
        return EAST
    elif PI_4 < alpha <= 3 * PI_4:
        return NORTH
    elif (3* PI_4 < alpha <= math.pi) or (-math.pi <= alpha <= -3 * PI_4):
        return WEST
    else:  # -3 * PI_4 < alpha <= -PI_4
        return SOUTH
    


class CollisionException(Exception):
    pass


def get_empty_coords(snake, objects):
    empty_coords = []
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            point = (x, y)
            if point not in snake and point not in objects:
                empty_coords.append(point)
    return empty_coords


def generate_new_object(snake, objects):
    objects.add(random.choice(get_empty_coords(snake, objects)))


def move(direction, snake, objects):
    """direction: tuple: e.g. (1, 0)"""
    head_x, head_y = snake[0]
    new_head_coords = new_head_x, new_head_y = (head_x + direction[0]) % SIZE_X, (head_y + direction[1]) % SIZE_Y
    if new_head_coords in snake[:-1]:
        raise CollisionException(new_head_coords)
    else:
        snake.insert(0, new_head_coords)
        if new_head_coords in objects:
            objects.remove(new_head_coords)  # remove from objects
            generate_new_object(snake, objects)
        else:
            snake.pop(-1)


def draw_snake(snake, state):
    head_x, head_y = snake[0]
    state[head_y][head_x] = HEAD
    per = period_switch(3)
    for i, (body_x, body_y) in enumerate(snake[1:]):
        #state[body_y][body_x] = max((9-i, BODY))
        #state[body_y][body_x] = (math.floor(i/2) % 2) * 3 + 3
        state[body_y][body_x] = next(per) * 3 + 3


def draw_objects(objects, state):
    for object_x, object_y in objects:
        state[object_y][object_x] = OBJECT


def redraw_state(snake, objects, state):
    reset(state)
    draw_objects(objects, state)
    draw_snake(snake, state)


def to_image(rows_of_numbers):
    """rows_of_nubmers: 5x5 grid of numbers from 0 to 9.
    output: Image made of these numbers."""
    return Image(":".join("".join(str(number) for number in row) for row in rows_of_numbers))


def reset(state, full_reset=False):
    for i, row in enumerate(state):
        for j in range(len(row)):
            state[i][j] = INITIAL_STATE[i][j]
    if full_reset:
        global direction
        direction = INITIAL_DIRECTION
        global snake
        snake = [
            (2, 2), # head
            (1, 2), # body
        ]
        global objects
        objects = set()
        generate_new_object(snake, objects)


state = [[EMPTY for x in range(SIZE_X)] for y in range(SIZE_Y)]
direction = INITIAL_DIRECTION
snake = [
    (2, 2), # head
    (1, 2), # body
]
objects = set()
generate_new_object(snake, objects)


def play_game(): # TODO detect win
    global direction
    global snake
    global objects
    global state
    while True:
        redraw_state(snake, objects, state)
        display.show(to_image(state))
        sleep(loop_time_ms)
        move(get_direction(), snake, objects)

while True:
    try:
        play_game()
    except CollisionException as collision_e:
        music.play(music.POWER_DOWN)
        while True:
            display.show(to_image(state))
            sleep(loop_time_ms)
            if pin_logo.is_touched():
                reset(state, full_reset=True)
            display.show(to_image(INITIAL_STATE))
            sleep(loop_time_ms)
            if pin_logo.is_touched():
                reset(state, full_reset=True)
                break
