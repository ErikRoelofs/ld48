from oned import Point, AnimatedSolidLine
from consts import *

class SubSystem:

    def __init__(self, oned, panel_color, output_color, off_color, max_power_consumption):
        self.oned = oned
        self.panel_color = Point(panel_color)
        self.output_color = Point(output_color)
        self.off_color = Point(off_color)
        self.panel_size_percentage = 0.03
        self.level = 0.1
        self.max_power_consumption = max_power_consumption

    def draw(self, start, end):
        size = end - start
        panel_size = int(size * self.panel_size_percentage)
        output_height = size - (2*panel_size)

        # top of panel
        self.oned.draw(self.panel_color, start, start + panel_size)

        # no-output level
        self.oned.draw(self.off_color, start + panel_size, start + panel_size + int(output_height * (1 - self.level)))

        # output level
        self.oned.draw(self.output_color, start + panel_size + int(output_height * (1 - self.level)), end - panel_size)

        # bottom of panel
        self.oned.draw(self.panel_color, end - panel_size, end)

    def set_level_from_percentage_clicked(self, percentage):
        # percentage is of the full draw area, but we ignore the panels
        available_percentage = 1 - (self.panel_size_percentage * 2)
        real_percentage = (percentage - self.panel_size_percentage) * (1 / available_percentage)
        if real_percentage > 1:
            real_percentage = 1
        if real_percentage < 0:
            real_percentage = 0
        self.level = 1 - real_percentage

    def get_level(self):
        return self.level

    def get_power_consumption(self):
        return self.level * self.max_power_consumption


class PowerPlant:
    def __init__(self, oned):
        self.color = Point(POWER_PLANT_COLOR)
        self.unused_color = Point(POWER_PLANT_UNUSED)
        self.charging_color = Point(POWER_PLANT_CHARGING)
        self.overload_color = Point(POWER_PLANT_OVERLOAD)
        self.excessive_load = AnimatedSolidLine(POWER_PLANT_UNUSED, POWER_PLANT_OVERLOAD, 1)
        self.center_marker = Point(NOTCH_COLOR)
        self.oned = oned
        self.current = 0
        self.max = 1

    def draw(self, start, end):
        percentage = self.current / self.max
        length = (end - start) / 2
        if self.current < self.max:
            self.oned.draw(self.unused_color, start, int(start + length))
            self.oned.draw(self.charging_color, int(start + length), int(start + length + (1 - percentage) * length))
            self.oned.draw(self.color, int(start + length + (1 - percentage) * length), end)
        else:
            overload = percentage - 1
            if overload > 1:
                self.oned.draw(self.excessive_load, start, int(start + length))
                pass
            else:
                self.oned.draw(self.unused_color, int(start), int(start + (1 - overload) * length))
                self.oned.draw(self.overload_color, int(start + (1 - overload) * length), int(end))
            self.oned.draw(self.color, int(start + length), int(end))

        # center marker
        self.oned.draw(self.center_marker, int(start + length) - 1, int(start + length) + 1)

    def set(self, current, max):
        self.current = current
        self.max = max

class Battery:
    def __init__(self, oned):
        self.fill_color = Point(BATTERY_COLOR)
        self.empty_color = Point(BATTERY_EMPTY)
        self.flashing = AnimatedSolidLine(BATTERY_EMPTY, BATTERY_FLASH, 1)
        self.oned = oned
        self.current = 0
        self.max = 1


    def draw(self, start, end):
        if self.current > 0:
            percentage = self.current / self.max
            length = end - start
            self.oned.draw(self.empty_color, start, int(start + (1 - percentage) * length))
            self.oned.draw(self.fill_color, int(start + (1 - percentage) * length), end)
        else:
            # drained; flash warnings
            self.oned.draw(self.flashing, start, end)

    def set(self, current, max):
        self.current = current
        self.max = max
