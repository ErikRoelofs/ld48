from oned import Point
from consts import *
from subsystem import SubSystem

class Sub:
    def __init__(self, oned):
        self.oned = oned
        self.graphic = Point((200, 200, 200))
        self.held = True
        self.depth = 10
        self.speed = 0
        self.system = [
            SubSystem(oned, (255, 0, 0), (150, 0, 0), (0, 0, 0)),
            SubSystem(oned, (0, 255, 0), (0, 150, 0), (0, 0, 0)),
            SubSystem(oned, (0, 0, 255), (0, 0, 150), (0, 0, 0)),
            SubSystem(oned, (255, 255, 0), (150, 150, 0), (0, 0, 0)),
            SubSystem(oned, (0, 255, 255), (0, 150, 150), (0, 0, 0)),
            SubSystem(oned, (255, 0, 255), (150, 0, 150), (0, 0, 0)),
            SubSystem(oned, (255, 255, 255), (150, 150, 150), (0, 0, 0)),
        ]

    def draw(self, position):
        self.oned.draw(self.graphic, position - 4, position + 4)

    def is_held(self):
        return self.held

    def drop(self):
        self.held = False

    def get_depth(self):
        return self.depth

    def update(self, dt):
        if self.held:
            return

        if self.depth < SPACE_TO_SURFACE_DEPTH:
            # free-falling
            self.speed += FREEFALL_SPEED * dt
        else:
            self.speed -= WATERBRAKE_SPEED * dt
            if self.speed < DEFAULT_SINK_SPEED:
                self.speed = DEFAULT_SINK_SPEED

        self.depth = self.depth + (self.speed * dt)

    def systems(self):
        return self.system
