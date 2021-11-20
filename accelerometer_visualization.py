"""Visualization of the accelerometer readings. Helps with development because you can see which axis is which.

1st row represents the X axis, 3rd row Y axis and 5th row Z axis.
When around 0, the middle LED shines, for < 0 LEDs to the left, for > 0 LEDs to the right.

Todo:
    * replace the log_transform_reading with something simpler like a simple 3 step mapping, e.g. <250, <1000, <2000 -> 0, 1, 2
    * comments -> education
"""

import microbit as m
import math


AXIS_MAX = 2000


def log_transform_reading(reading, max_output_val=2, max_input_val=AXIS_MAX):
    sign = int(math.copysign(1.0, reading))
    if abs(reading) <= 1:
        return 0
    return sign * round(math.log(abs(reading), max_input_val**(1/max_output_val)))


def reading_to_row(reading):
    transformed_reading = log_transform_reading(reading)
    if transformed_reading == 0:
        return (0,0,1,0,0)
    elif transformed_reading == -1:
        return (0,1,0,0,0)
    elif transformed_reading == -2:
        return (1,1,0,0,0)
    elif transformed_reading == 1:
        return (0,0,0,1,0)
    elif transformed_reading == 2:
        return (0,0,0,1,1)
    else:
        return ValueError("Value not expected")


def readings_to_image(x, y, z):
    return to_image(change_intensity((
        reading_to_row(x),
        (0,0,0,0,0),
        reading_to_row(y),
        (0,0,0,0,0),
        reading_to_row(z),
    ), 5))


def change_intensity(image_matrix, factor):
    return tuple(tuple(min(9, max(0, round(cell*factor))) for cell in row) for row in image_matrix)


def to_image(rows_of_numbers):
    """rows_of_nubmers: 5x5 grid of numbers from 0 to 9.
    output: Image made of these numbers."""
    return m.Image(":".join("".join(str(number) for number in row) for row in rows_of_numbers))


TIMEOUT = 50

while True:
    m.display.show(readings_to_image(
        m.accelerometer.get_x(),
        m.accelerometer.get_y(),
        m.accelerometer.get_z(),
    ))
    m.sleep(TIMEOUT)

