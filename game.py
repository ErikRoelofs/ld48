import sys, pygame, random

pygame.init()
clock = pygame.time.Clock()

from oned import *
from consts import *
from functions import *
from sub import Sub
from altimeter import Altimeter
from world import World

from pygame.locals import*


def main():
    onedI = Oned(WIDTH, HEIGHT, VERTICAL)
    altimeter = Altimeter(onedI)
    spaceship = GradientLine(SPACESHIP_COLOR_START, SPACESHIP_COLOR_END)
    world = World()
    sub = Sub(onedI, world)

    panel_background = SolidLine(PANEL_COLOR)

    active_screen = ALTIMETER_SCREEN
    dragging_power = False
    dragging_system = None

    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
            if events.type == KEYDOWN:
                if events.key == K_SPACE and sub.is_held():
                    sub.drop()
                if events.key == K_1 and not sub.is_held():
                    active_screen = ALTIMETER_SCREEN
                if events.key == K_2 and not sub.is_held():
                    active_screen = SYSTEM_CONTROLS_SCREEN
                if events.key == K_3 and not sub.is_held():
                    active_screen = POWER_CONTROLS_SCREEN
            if events.type == MOUSEBUTTONDOWN:
                if not dragging_power:
                    pos = onedI.get_mouse_position()
                    got = get_system_from_position(sub, pos)
                    if got is not None:
                        (system, position) = got
                        dragging_system = system
                        dragging_power = True
            if events.type == MOUSEBUTTONUP:
                dragging_power = False
                dragging_system = None

        dt = clock.get_time() / 1000

        if dragging_power:
            if active_screen == SYSTEM_CONTROLS_SCREEN:
                pos = onedI.get_mouse_position()
                got = get_system_from_position(sub, pos)
                if got is not None:
                    (system, position) = got
                    if system and system == dragging_system:
                        system.set_level_from_percentage_clicked(position)

        # updating
        if not sub.update(dt):
            # game over.
            print("game over")
            return

        # drawing
        if active_screen == ALTIMETER_SCREEN:
            onedI.draw(spaceship, 0, 20)
            altimeter.draw()
            sub.draw(int(sub.get_depth()))

        if active_screen == SYSTEM_CONTROLS_SCREEN:
            onedI.draw(panel_background, 0, HEIGHT)
            for index, system in enumerate(sub.systems()):
                system.draw(
                    (SYSTEM_PANEL_GAP + index * (SYSTEM_SIZE + SYSTEM_PANEL_GAP)),
                    (SYSTEM_PANEL_GAP + index * (SYSTEM_SIZE + SYSTEM_PANEL_GAP)) + SYSTEM_SIZE
                )

        if active_screen == POWER_CONTROLS_SCREEN:
            onedI.draw(panel_background, 0, HEIGHT)
            sub.get_power_plant().draw(25, 300)
            sub.get_battery().draw(325, 700)
            sub.get_heat().draw(725, HEIGHT - 25)
            pass

        sub.draw_static_interference()

        onedI.show()
        clock.tick(40)

main()