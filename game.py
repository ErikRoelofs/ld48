import sys, pygame, random
from oned import *
from consts import *
from sub import Sub
from altimeter import Altimeter

from pygame.locals import*

pygame.init()
clock = pygame.time.Clock()


def main():
    onedI = Oned(WIDTH, HEIGHT, VERTICAL)
    altimeter = Altimeter(onedI)
    spaceship = GradientLine(SPACESHIP_COLOR_START, SPACESHIP_COLOR_END)
    sub = Sub(onedI)

    panel_background = SolidLine(PANEL_COLOR)

    active_screen = ALTIMETER_SCREEN

    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
            if events.type == KEYDOWN:
                if events.key == K_SPACE and sub.is_held():
                    sub.drop()
                if events.key == K_1:
                    active_screen = ALTIMETER_SCREEN
                if events.key == K_2:
                    active_screen = SYSTEM_CONTROLS_SCREEN
                if events.key == K_3:
                    active_screen = POWER_CONTROLS_SCREEN

        dt = clock.get_time() / 1000

        # updating
        sub.update(dt)

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
            pass

        onedI.show()
        clock.tick()

main()