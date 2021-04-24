from consts import *


def get_system_from_position(sub, pos):
    for index, system in enumerate(sub.systems()):
        system_start = (SYSTEM_PANEL_GAP + index * (SYSTEM_SIZE + SYSTEM_PANEL_GAP))
        system_end = (SYSTEM_PANEL_GAP + index * (SYSTEM_SIZE + SYSTEM_PANEL_GAP)) + SYSTEM_SIZE
        if system_start <= pos <= system_end:
            length = system_end - system_start
            offset = pos - system_start
            percentage = offset / length
            return system, percentage