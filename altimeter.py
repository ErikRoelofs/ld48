from oned import GradientLine, Point
from consts import *

class Altimeter:

    def __init__(self, oned):
        self.oned = oned
        self.background = GradientLine(BACKGROUND_SEA_START, BACKGROUND_SEA_END)
        self.notch = Point(NOTCH_COLOR)

    def draw(self):
        self.oned.draw(self.background, SPACE_TO_SURFACE_DEPTH, HEIGHT)
        # draw depth notches
        for i in range(SPACE_TO_SURFACE_DEPTH, HEIGHT, NOTCH_STEP):
            self.oned.draw(self.notch, i, i+1)
