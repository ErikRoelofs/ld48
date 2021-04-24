from oned import Point

class SubSystem:

    def __init__(self, oned, panel_color, output_color, off_color):
        self.oned = oned
        self.panel_color = Point(panel_color)
        self.output_color = Point(output_color)
        self.off_color = Point(off_color)
        self.level = 0.5

    def draw(self, start, end):
        size = end - start
        panel_size = int(size * 0.03)
        output_height = size - (2*panel_size)

        # top of panel
        self.oned.draw(self.panel_color, start, start + panel_size)

        # no-output level
        self.oned.draw(self.off_color, start + panel_size, start + panel_size + int(output_height * (1 - self.level)))

        # output level
        self.oned.draw(self.output_color, start + panel_size + int(output_height * (1 - self.level)), end - panel_size)

        # bottom of panel
        self.oned.draw(self.panel_color, end - panel_size, end)