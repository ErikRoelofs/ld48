import sys, pygame, random
from oned import Oned, GradientLine, Point, SolidLine, AnimatedSolidLine, ArrayImage, Spinner
from pygame.locals import*

width=1000
height=100
Color_screen=(0,0,0)
Color_line=(255,0,0)


def main():
    onedI = Oned(width, height)
    #d = GradientLine((255, 0, 0), (0, 255, 255))
    #d2 = AnimatedSolidLine((255, 0, 0), (0, 255, 255), 3)
    r = Spinner((255, 0, 0), (255, 255, 255), 1)
    image = ArrayImage([(255, 255, 255), (0, 0, 0), (255, 0, 255), (255, 255, 0), (255, 255, 255)])
    p = Point((0, 255, 0))
    i = 100
    while True:
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)

#        onedI.draw(d, i + 300, i + 500)
#        onedI.draw(d2, i, i+200)
        onedI.draw(r, i + 300, i + 500)
        onedI.draw(image, 0, 75)
#        for a in range(1,100):
#            onedI.draw(p, random.randint(0, 1000))
        onedI.show()

#        i = i + 1
        if i > 800:
            i = 100

main()