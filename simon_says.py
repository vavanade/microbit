"""A simple "Simon says" game where you have to repeat the button presses.

Todo:
    * initialize with a random major chord, not just F so the tones are less boring
    * break up the game into several functions so the code is better readable
    * bring out constants
    * fix timings
"""

from microbit import *
import music

import math
import random


PIN_LOGO = Image((
    "05550:"
    "05550:"
    "05550:"
    "00000:"
    "00000:"
))

PIN_LOGO_SOUND = ("F:4", )  # ("F:3", "r:1")

BUTTON_A = Image((
    "00000:"
    "00000:"
    "55500:"
    "55500:"
    "55500:"
))

BUTTON_A_SOUND =  ("A:4", )  # ("A:3", "r:1")

BUTTON_B = Image((
    "00000:"
    "00000:"
    "00555:"
    "00555:"
    "00555:"
))

BUTTON_B_SOUND = ("C:4", )  #("C:3", "r:1")

PIN_0 = Image((
    "05550:"
    "50005:"
    "50005:"
    "50005:"
    "05550:"
))

PIN_0_SOUND = ("G:4", )

PIN_1 = Image((
    "00000:"
    "00500:"
    "00500:"
    "00500:"
    "00000:"
))

PIN_1_SOUND = ("B:4", )

PIN_2 = Image((
    "00000:"
    "05050:"
    "05050:"
    "05050:"
    "00000:"
))

PIN_2_SOUND = ("D:4", )

# The game uses the music tempo as the tempo to display images
music.set_tempo(bpm=60)

TICKS, BPM = music.get_tempo()
SOUND_DURATION_MS = int(60000/BPM)

int_to_img_sound = {
    1: (PIN_LOGO, PIN_LOGO_SOUND),
    2: (BUTTON_A, BUTTON_A_SOUND),
    3: (BUTTON_B, BUTTON_B_SOUND),
    4: (PIN_0, PIN_0_SOUND),
    5: (PIN_1, PIN_1_SOUND),
    6: (PIN_2, PIN_2_SOUND),
}

simon_said = []
for _ in range(3):
    simon_said.append(random.randint(1, 6))

repeated = []

successful_game = True
for _ in range(5):
    for instruction in simon_said:
        img, sound = int_to_img_sound[instruction]
        display.show(img, SOUND_DURATION_MS, wait=False)
        music.play(sound)
        sleep(200)

    successful_repetition = True
    for i in range(len(simon_said)):
        while True:
            if button_a.is_pressed():
                display.show(BUTTON_A, SOUND_DURATION_MS, wait=False)
                music.play(BUTTON_A_SOUND)
                repeated.append(2)
                break
            elif button_b.is_pressed():
                display.show(BUTTON_B, SOUND_DURATION_MS, wait=False)
                music.play(BUTTON_B_SOUND)
                repeated.append(3)
                break
            elif pin_logo.is_touched():
                display.show(PIN_LOGO, SOUND_DURATION_MS, wait=False)
                music.play(PIN_LOGO_SOUND)
                repeated.append(1)
                break
        if repeated[:i+1] != simon_said[:i+1]:
            successful_repetition = False
            break
    if successful_repetition:
        repeated = []
        music.play(music.BA_DING)
        simon_said.append(random.randint(1, 3))
    else:
        successful_game = False
        break
if successful_game:
    music.set_tempo(bpm=120)
    music.play(music.POWER_UP)
    for bpm in range(120, 150+1, 10):  # speed it up!
        music.set_tempo(bpm=bpm)
        music.play(music.NYAN)
    for _ in range(2):  # play it 2 more times at the max tempo
        music.play(music.NYAN)
else:
    music.play(music.POWER_DOWN)
