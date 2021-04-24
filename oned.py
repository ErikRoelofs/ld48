import pygame, math

HORIZONTAL = 1
VERTICAL = 2

class Oned:
    items = []
    screen = None
    Color_screen = (0, 0, 0)
    direction = 0

    def __init__(self, width, height, direction):
        self.width = width
        self.height = height
        if direction not in (HORIZONTAL, VERTICAL):
            raise ValueError("Direction must be HORIZONTAL or VERTICAL")
        self.direction = direction
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def show(self):
        self.screen.fill(self.Color_screen)
        for item in self.items:
            drawable = item[0]
            position_start = item[1]
            position_end = item[2]
            length = position_end - position_start

            for i in range(position_start, position_end):
                color = drawable.colorAt((i - position_start) / length, pygame.time.get_ticks() / 1000)
                # no alpha support :(
                if len(color) == 3 or color[3] == 255:
                    if self.direction == HORIZONTAL:
                        pygame.draw.line(self.screen, color, (i, 0), (i, self.height))
                    elif self.direction == VERTICAL:
                        pygame.draw.line(self.screen, color, (0, i), (self.width, i))

        pygame.display.flip()
        self.items = []

    def draw(self, drawable, position_start, position_end=None):
        if position_end is None:
            position_end = position_start + 1
        self.items.append((drawable, position_start, position_end))

    def get_mouse_position(self):
        (x, y) = pygame.mouse.get_pos()
        if self.direction == HORIZONTAL:
            return x
        if self.direction == VERTICAL:
            return y

class Drawable:
    # get the color at a percentage of the drawable's length
    def colorAt(self, percentage, time):
        pass


# a line with a solid color
class SolidLine(Drawable):
    color = None

    def __init__(self, color):
        self.color = color

    # a solid line's color is static
    def colorAt(self, percentage, time):
        return self.color


# a point is really no different from a line
class Point(SolidLine):
    pass


# a gradient line changes color over its length
class GradientLine(Drawable):
    color_start = None
    color_end = None
    distances = None

    def __init__(self, color_start, color_end):
        self.color_start = color_start
        self.color_end = color_end
        self.distances = (color_end[0] - color_start[0], color_end[1] - color_start[1], color_end[2] - color_start[2])

    # a solid line's color is static
    def colorAt(self, percentage, time):
        return (
            min(255, max(0, self.color_start[0] + (self.distances[0] * percentage))),
            min(255, max(0, self.color_start[1] + (self.distances[1] * percentage))),
            min(255, max(0, self.color_start[2] + (self.distances[2] * percentage))),
        )


# an animated line has a solid color that changes over time
class AnimatedSolidLine(Drawable):
    color_start = None
    color_end = None
    distances = None
    forward = True
    last = 0

    def __init__(self, color_start, color_end, duration):
        self.color_start = color_start
        self.color_end = color_end
        self.distances = (color_end[0] - color_start[0], color_end[1] - color_start[1], color_end[2] - color_start[2])
        self.duration = duration

    # an animated solid line's color fluctuates over time
    def colorAt(self, percentage, time):
        place = (time % self.duration) / self.duration
        if place < self.last:
            # we cycled; change direction
            self.forward = not self.forward
        self.last = place
        if self.forward:
            real_place = place
        else:
            real_place = 1 - place
        return (
            min(255, max(0, self.color_start[0] + (self.distances[0] * real_place))),
            min(255, max(0, self.color_start[1] + (self.distances[1] * real_place))),
            min(255, max(0, self.color_start[2] + (self.distances[2] * real_place))),
        )


class ArrayImage(Drawable):
    colors = []

    def __init__(self, colors):
        self.colors = colors
        self.item_length = 1 / len(self.colors)

    def colorAt(self, percentage, time):
        # prevent overflow at exactly 1
        if percentage > 0.9999:
            return self.colors[len(self.colors) - 1]
        return self.colors[math.floor(percentage / self.item_length)]


class PNGImage(Drawable):
    img = None
    width = 0

    def __init__(self, path):
        my_image = pygame.image.load(path)
        width = my_image.get_width()
        self.img = my_image
        self.width = width

    def colorAt(self, percentage, time):
        x = math.ceil(percentage * self.width)
        if x == 0:
            x = 1
        if x == self.width:
            x = self.width - 1
        color = self.img.get_at((x, 1))
        return color

class Spinner(Drawable):
    color_band = None
    color_main = None
    distances = None

    def __init__(self, color_main, color_band, duration):
        self.color_main = color_main
        self.color_band = color_band
        self.distances = (self.color_main[0] - self.color_band[0], self.color_main[1] - self.color_band[1], self.color_main[2] - self.color_band[2])
        self.duration = duration

    # a spinner's color is primarily the start color with a band of the end color cycling past it
    def colorAt(self, percentage, time):
        center = (time % self.duration) / self.duration
        distance = min(math.fabs(center - percentage), 1 - math.fabs(center - percentage))
        distance = math.sin(distance * math.pi / 2) * 4
        return (
            min(255, max(0, self.color_band[0] + (self.distances[0] * distance))),
            min(255, max(0, self.color_band[1] + (self.distances[1] * distance))),
            min(255, max(0, self.color_band[2] + (self.distances[2] * distance))),
        )

class AnimatedArrayImage(Drawable):
    images = []

    def __init__(self, colors, duration):
        self.images = colors
        self.num_images = len(self.images)
        self.duration = duration

    def colorAt(self, percentage, time):
        print(percentage)
        print(time)
        print('--')
        place = (time % self.duration) / self.duration
        use_img = math.floor(place * self.num_images)
        return self.images[use_img].colorAt(percentage, time)
