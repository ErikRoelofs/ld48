from oned import GradientLine, Point
from consts import *

class Altimeter:

    def __init__(self, oned, sonar, world):
        self.oned = oned
        self.background = GradientLine(BACKGROUND_SEA_START, BACKGROUND_SEA_END)
        self.notch = Point(NOTCH_COLOR)
        self.real_height = HEIGHT * 10
        self.sonar = sonar
        self.reveals = {}
        self.world = world

    def draw(self, depth):
        if depth < 500:
            self.oned.draw(self.background, SPACE_TO_SURFACE_DEPTH, SPACE_TO_SURFACE_DEPTH + self.real_height)
            # draw depth notches
            for i in range(SPACE_TO_SURFACE_DEPTH, HEIGHT, NOTCH_STEP):
                self.oned.draw(self.notch, i, i+1)

        else:
            if int(SPACE_TO_SURFACE_DEPTH - depth) > 0:
                self.oned.draw(self.background, 0, int(SPACE_TO_SURFACE_DEPTH - depth))
            self.oned.draw(self.background, int(SPACE_TO_SURFACE_DEPTH - depth + (HEIGHT / 2)), int(SPACE_TO_SURFACE_DEPTH + self.real_height - depth + (HEIGHT / 2)))
            # draw depth notches
            for i in range(0, HEIGHT + NOTCH_STEP, NOTCH_STEP):
                self.oned.draw(self.notch, int(i - (depth % NOTCH_STEP)), int(i - (depth % NOTCH_STEP) + 1))

        # draw things revealed by sonar
        for reveal, timer in self.reveals.items():
            color = self.world.get_sonar_color(reveal, timer)
            if color:
                self.oned.draw(color, self.depth_to_pos(depth, reveal))

        # draw sonar
        for ping in self.sonar:
            ping.draw(self.depth_to_pos(depth, ping.get_depth()))

    def depth_to_pos(self, sub_depth, other_depth):
        if sub_depth < 500:
            return int(other_depth)
        else:
            return int(other_depth - (sub_depth - (HEIGHT / 2)))


    def reveal(self, depth):
        self.reveals[int(depth)] = SONAR_REVEAL_TIME

    def update(self, dt):
        to_remove = []
        for depth in self.reveals:
            self.reveals[depth] -= dt
            if self.reveals[depth] < 0:
                to_remove.append(depth)
        for depth in to_remove:
            del self.reveals[depth]
