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
    background = GradientLine(BACKGROUND_SEA_START, BACKGROUND_SEA_END)
    altimeter = Altimeter(onedI)
    spaceship = GradientLine(SPACESHIP_COLOR_START, SPACESHIP_COLOR_END)
    sub = Sub(onedI)

    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
            if events.type == KEYDOWN:
                if sub.is_held() and events.key == K_SPACE:
                    sub.drop()

        dt = clock.get_time() / 1000

        # updating
        sub.update(dt)

        # drawing
        onedI.draw(spaceship, 0, 20)
        altimeter.draw()
        sub.draw(int(sub.get_depth()))
        onedI.show()
        clock.tick()

main()