"""The aim of this is to make a bouncy ball that feels like it behaves like a physical object trapped inside the micro:bit LED array.

Todo:
    * sound effects?
"""

import microbit as m
import math
import utime

# ######### #
# constants #
# ######### #
# distance between the LEDs so it fits the physical dimensions of the micro:bit LED array
MIN_X = 0.0  # m
MIN_Y = 0.0  # m
MAX_X = 16.5 * 0.001  # m
MAX_Y = 16.5 * 0.001  # m

# number of LEDs in each direction
LED_CNT_X = 5
LED_CNT_Y = 5

# integer 0-9
INTENSITY = 5

# length that one LED represents in X and Y axes
DIV_X = (MAX_X - MIN_X) / LED_CNT_X  # m
DIV_Y = (MAX_Y - MIN_Y) / LED_CNT_Y  # m

# time period of one step
T_MS = 10  # period in ms
T = T_MS * 0.001  # period in s

# non-constant globals
# current position of the ball
X = (MAX_X-MIN_X) / 2
Y = (MAX_Y-MIN_Y) / 2

# current velocity of the ball
V_X = 0.0
V_Y = 0.0

# factor that makes the ball lose energy on collisions. DO NOT put it > 1.
V_BOUNCE_FACTOR = 0.95

def pos_to_cnt(x: float, y: float) -> "Tuple[int, int]":
    """
    Returns:
        LED position that needs to be lit to represent the ball position.
    Raises:
        ValueError if position is out of bounds given by MIN_X, MIN_Y, MAX_X, MAX_Y.
    """
    if not (MIN_X <= x <= MAX_X) or not (MIN_Y <= y <= MAX_Y):
        raise ValueError("Position (x=%.2f, y=%.2f) out of bounds!" % (x, y))
    return (math.floor(x/DIV_X), math.floor(y/DIV_Y))


def step(t: float):
    """Read the x and y acceleration from the accelerometer and "integrate" the next position with the time step t.
    Handle collisions if the position turns out to be outside the boundaries given by MIN_X, MIN_Y, MAX_X, MAX_Y.
    """
    global X, Y, V_X, V_Y
    # get accelerations directly from the accelerometer module
    # *0.001 is to convert them from mm/s**2 to m/s**2
    a_x = m.accelerometer.get_x()*0.001
    a_y = m.accelerometer.get_y()*0.001
    
    # v_new = v + a * t
    V_X += a_x*t
    V_Y += a_y*t
    
    # x_new = x + v*t + a*t**2/2
    X = X + V_X*t + a_x*t**2/2
    Y = Y + V_Y*t + a_y*t**2/2
    
    # ################# #
    # handle collisions #
    # ################# #
    # reverse velocity on collision and reduce it by the V_BOUNCE_FACTOR
    # Could still fail to put the ball inside the designated area when T is too large.
    # Fails if the ball sits in one place near the edge for a long time with "ValueError("Index too large")". I don't know why.
    if X < MIN_X:
        X += 2*(MIN_X-X)
        V_X *= -V_BOUNCE_FACTOR
    if Y < MIN_Y:
        Y += 2*(MIN_Y-Y)
        V_Y *= -V_BOUNCE_FACTOR
    if X > MAX_X:
        X += 2*(MAX_X-X)
        V_X *= -V_BOUNCE_FACTOR
    if Y > MAX_Y:
        Y += 2*(MAX_Y-Y)
        V_Y *= -V_BOUNCE_FACTOR

# main loop
while True:
    start = utime.ticks_ms()  # get the time of the start of evaluation in ms
    im = m.Image(LED_CNT_X, LED_CNT_Y)  # create an empty image
    x, y = pos_to_cnt(X, Y)  # convert the position to the appropriate LED
    im.set_pixel(x, y, INTENSITY)  # set the LED position in the image
    m.display.show(im)  # show the image
    step(T)  # make the physics happen
    to_sleep_ms = T_MS - utime.ticks_diff(utime.ticks_ms(), start)  # calculate how much time we have left in the alloted time period
    if to_sleep_ms >= 0:
        utime.sleep_ms(to_sleep_ms)  # sleep for the rest of the time period
    else:
        raise TimeoutError()
