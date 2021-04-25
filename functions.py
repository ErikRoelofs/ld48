from consts import *
import math
from oned import SolidLine, AnimatedArrayImage, ArrayImage
import random

def get_system_from_position(sub, pos):
    for index, system in enumerate(sub.systems()):
        system_start = (SYSTEM_PANEL_GAP + index * (SYSTEM_SIZE + SYSTEM_PANEL_GAP))
        system_end = (SYSTEM_PANEL_GAP + index * (SYSTEM_SIZE + SYSTEM_PANEL_GAP)) + SYSTEM_SIZE
        if system_start <= pos <= system_end:
            length = system_end - system_start
            offset = pos - system_start
            percentage = offset / length
            return system, percentage


win_colors = [
    SolidLine((0, 0, 255)),
    SolidLine((0, 0, 225)),
    SolidLine((0, 0, 195)),
    SolidLine((0, 0, 165)),
    SolidLine((0, 0, 135)),
    SolidLine((0, 0, 105)),
    SolidLine((0, 0, 85)),
    SolidLine((0, 0, 65)),
    SolidLine((0, 0, 45)),
    SolidLine((0, 0, 25)),
]

def score_drawer(oned, score):
    block_height = 30  # each block is 10px high
    block_value = 1000  # each block is worth 1000 points
    blocks = math.floor(score / block_value)
    # draw full blocks
    for i in range(0, blocks):
        oned.draw(win_colors[i], i * block_height, (i+1)*block_height)

    # draw remainder
    screen_left = HEIGHT - (block_height * blocks)
    score_left = score - (blocks * block_value)
    percentage_draw = score_left / screen_left
    color = win_colors[blocks]  # 2 blocks use up 0, 1 so slot 2 is the remainder color.

    oned.draw(color, int(blocks * block_height), int((blocks * block_height) + (percentage_draw * screen_left)))

def make_static(amount = 100, static_depth = 100):
    images = []
    for i in range(0, amount):
        image = make_static_image(static_depth)
        images.append(image)
    return AnimatedArrayImage(images, 1)


def make_static_image(amount = 100):
    colors = []
    for i in range(0, amount):
        color = DAMAGE_COLORS[random.randint(0, len(DAMAGE_COLORS) - 1)]
        colors.append(color)
    return ArrayImage(colors)


def get_color(biome, biome_types):
    for other_biome in biome_types:
        if biome == other_biome.name():
            return other_biome.science_color()
    return None
