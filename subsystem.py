from oned import Point, AnimatedSolidLine, GradientLine, ArrayImage, AnimatedArrayImage
from consts import *
from soundplayer import SoundPlayer
import random

class SubSystem:

    def __init__(self, oned, panel_color, output_color, off_color, max_power_consumption):
        self.oned = oned
        self.panel_color = Point(panel_color)
        self.output_color = Point(output_color)
        self.off_color = Point(off_color)
        self.panel_size_percentage = 0.03
        self.level = 0.1
        self.max_power_consumption = max_power_consumption
        self.damage = 0
        self.scratches = []
        self.static = make_static(100, 100)
        self.engaged = False
        self.power_availability = 1

    def engage(self):
        self.engaged = True

    def draw(self, start, end):
        size = end - start
        panel_size = int(size * self.panel_size_percentage)
        output_height = size - (2*panel_size)

        # top of panel
        self.oned.draw(self.panel_color, start, start + panel_size)
        # bottom of panel
        self.oned.draw(self.panel_color, end - panel_size, end)

        if self.is_broken():
            self.oned.draw(self.static, start + panel_size, end - panel_size)
            return

        # no-output level
        self.oned.draw(self.off_color, start + panel_size,
                       start + panel_size + int(output_height * (1 - self.level)))

        # output level
        self.oned.draw(self.output_color, start + panel_size + int(output_height * (1 - self.level)),
                       end - panel_size)

        # draw damage scratches over the system
        for position in self.scratches:
            color = DAMAGE_COLORS[random.randint(0, len(DAMAGE_COLORS) - 1)]
            self.oned.draw(Point(color), int(start + (position / 100 * size)), int(start + (position / 100 * size)) + 1)

    def set_level_from_percentage_clicked(self, percentage):
        # percentage is of the full draw area, but we ignore the panels
        available_percentage = 1 - (self.panel_size_percentage * 2)
        real_percentage = (percentage - self.panel_size_percentage) * (1 / available_percentage)
        if real_percentage > 1:
            real_percentage = 1
        if real_percentage < 0:
            real_percentage = 0
        self.level = 1 - real_percentage
        self.level_changed()

    def level_changed(self):
        pass

    def set_available_power(self, available_power):
        if self.power_availability != available_power:
            self.power_availability = available_power
            self.level_changed()

    def get_strength(self):
        return self.level * self.power_availability * (1 - self.damage)

    def get_power_consumption(self):
        return self.level * self.max_power_consumption

    def apply_damage(self, damage):
        self.damage += damage
        if self.damage > 1:
            self.damage = 1
            self.level = 0

        while len(self.scratches) < self.damage * 10:
            self.scratches.append(random.randint(0, 100))
        self.level_changed()

    def is_broken(self):
        return self.damage >= 1

class PowerPlant:
    def __init__(self, oned):
        self.color = Point(POWER_PLANT_COLOR)
        self.unused_color = Point(POWER_PLANT_UNUSED)
        self.charging_color = Point(POWER_PLANT_CHARGING)
        self.overload_color = Point(POWER_PLANT_OVERLOAD)
        self.excessive_load = AnimatedSolidLine(POWER_PLANT_UNUSED, POWER_PLANT_OVERLOAD, 1)
        self.frost_color = Point((100, 100, 255))
        self.center_marker = Point(NOTCH_COLOR)
        self.oned = oned
        self.current = 0
        self.current_max = 1
        self.max = 1

    def draw(self, start, end):
        percentage = self.current / self.current_max
        available_production = self.current_max / self.max
        half = ((end - start) / 2)
        production_length = half * available_production
        overcharge_length = half
        frost_length = (half * (1 - (available_production)))
        if frost_length > 0:
            self.oned.draw(self.frost_color, start, int(start + frost_length))
            start = int(start + frost_length)
        if self.current < self.current_max:
            self.oned.draw(self.unused_color, start, int(start + overcharge_length))
            self.oned.draw(self.charging_color, int(start + overcharge_length), int(start + overcharge_length + (1 - percentage) * production_length))
            self.oned.draw(self.color, int(start + overcharge_length + (1 - percentage) * production_length), end)
        else:
            overload = percentage - 1
            if overload > 1:
                self.oned.draw(self.excessive_load, start, int(start + overcharge_length))
                pass
            else:
                self.oned.draw(self.unused_color, int(start), int(start + (1 - overload) * overcharge_length))
                self.oned.draw(self.overload_color, int(start + (1 - overload) * overcharge_length), int(end))
            self.oned.draw(self.color, int(start + overcharge_length), int(end))

        # center marker (adjusted for low power)
        self.oned.draw(self.center_marker, int(start + overcharge_length) - 1, int(start + overcharge_length) + 1)

    def update_power(self, power_usage, temperature, battery, dt):
        power_availability = 1

        if power_usage > self.get_max_power(temperature):
            # drain batteries if possible
            energy_used = (power_usage - self.get_max_power(temperature)) * dt
            if not battery.decrease(energy_used):
                # power issues! reduce availability allround
                power_availability = self.get_max_power(temperature) / power_usage
        else:
            energy_gained = (self.get_max_power(temperature) - power_usage) * dt
            battery.increase(energy_gained)

        self.set(power_usage, self.get_max_power(temperature), self.get_normal_max_power())
        return power_availability

    def get_max_power(self, temperature):
        if temperature > SUB_FREEZING_TRESHOLD:
            return MAX_POWER_PRODUCTION
        max_power_loss = abs(MIN_TEMPERATURE - SUB_FREEZING_TRESHOLD)
        below_treshold = SUB_FREEZING_TRESHOLD - temperature
        percentage = below_treshold / max_power_loss
        power_cut = percentage * MAX_POWER_PRODUCTION_LOSS_PERCENTAGE
        return MAX_POWER_PRODUCTION * (1 - power_cut)

    def get_normal_max_power(self):
        return MAX_POWER_PRODUCTION

    def set(self, current, current_max, max):
        self.current = current
        self.current_max = current_max
        self.max = max

class Battery:
    def __init__(self, oned):
        self.fill_color = Point(BATTERY_COLOR)
        self.empty_color = Point(BATTERY_EMPTY)
        self.flashing = AnimatedSolidLine(BATTERY_EMPTY, BATTERY_FLASH, 1)
        self.oned = oned
        self.current = 0
        self.max = self.get_max_battery()

    def get_max_battery(self):
        return MAX_BATTERY_CAPACITY

    def draw(self, start, end):
        if self.current > 0:
            percentage = self.current / self.max
            length = end - start
            self.oned.draw(self.empty_color, start, int(start + (1 - percentage) * length))
            self.oned.draw(self.fill_color, int(start + (1 - percentage) * length), end)
        else:
            # drained; flash warnings
            self.oned.draw(self.flashing, start, end)

    def set(self, current):
        self.current = current

    def increase(self, amount):
        self.current += amount
        if self.current > self.max:
            self.current = self.max
            return False
        return True

    def decrease(self, amount):
        self.current -= amount
        if self.current < 0:
            self.current = 0
            return False
        return True


class Heat:
    def __init__(self, oned):
        self.too_hot_zone = Point(OVERHEAT_END_COLOR)
        self.hot_zone = GradientLine(OVERHEAT_END_COLOR, GOOD_TEMPERATURE_COLOR)
        self.green_zone = Point(GOOD_TEMPERATURE_COLOR)
        self.cold_zone = GradientLine(GOOD_TEMPERATURE_COLOR, FREEZING_END_COLOR)
        self.too_cold_zone = Point(FREEZING_END_COLOR)
        self.marker_ok = Point(NOTCH_COLOR)
        self.oned = oned
        self.temperature = 0
        self.overheat_damage_counter = 0

    def draw(self, start, end):
        each_length = (end - start) / 5
        self.oned.draw(self.too_hot_zone, start, int(start + each_length))
        self.oned.draw(self.hot_zone, int(start + each_length), int(start + each_length * 2))
        self.oned.draw(self.green_zone, int(start + each_length * 2), int(start + each_length * 3))
        self.oned.draw(self.cold_zone, int(start + each_length * 3), int(start + each_length * 4))
        self.oned.draw(self.too_cold_zone, int(start + each_length * 4), end)

        # temperature marker
        total_temp_span = MAX_TEMPERATURE - MIN_TEMPERATURE
        total_length = (end - start)
        temp_offset = self.temperature - MIN_TEMPERATURE
        draw_percentage = 1 - (temp_offset / total_temp_span)
        self.oned.draw(self.marker_ok, start + int(draw_percentage * total_length) - 2, start + int(draw_percentage * total_length) + 2)

    def get(self):
        return self.temperature

    def update_heat(self, sub, world, dt):
        correct = sub.climate_control().get_strength() * MAX_CLIMATE_CONTROL_CORRECT * dt
        if self.temperature > IDEAL_TEMPERATURE:
            self.temperature -= correct
        elif self.temperature < IDEAL_TEMPERATURE:
            self.temperature += correct

        outside_temp = world.get_temperature(sub.depth)
        diff = abs(outside_temp - self.temperature)
        modify = (diff * SUB_TEMPERATURE_CAPTURE) * dt
        if outside_temp > self.temperature:
            self.temperature += modify
        elif outside_temp < self.temperature:
            self.temperature -= modify

        if self.temperature < MIN_TEMPERATURE:
            self.temperature = MIN_TEMPERATURE
        if self.temperature > MAX_TEMPERATURE:
            self.temperature = MAX_TEMPERATURE

        if self.temperature > SUB_OVERHEAT_TRESHOLD:
            self.overheat_damage_counter += dt
        else:
            self.overheat_damage_counter -= dt

        if self.overheat_damage_counter > 1:
            sub.get_rand_sys().apply_damage(random.randint(0, 1000) / 100)
            self.overheat_damage_counter -= 1
        if self.overheat_damage_counter < 0:
            self.overheat_damage_counter = 0


class Audio(SubSystem):
    def __init__(self, oned, panel_color, output_color, off_color, max_power_consumption):
        super().__init__(oned, panel_color, output_color, off_color, max_power_consumption)
        self.player = SoundPlayer()
        self.depth = 0

    def play(self, command, external_volume):
        self.player.play_sound(command, external_volume)

    def play_repeating(self, command, external_volume):
        self.player.play_repeating(command, external_volume)

    def update_volume(self, command, new_volume):
        self.player.update_volume(command, new_volume)

    def get_volume(self):
        strength_need = (self.depth * AUDIO_QUALITY_DROPOFF)
        if strength_need < self.get_strength():
            return 1
        return self.get_strength() / strength_need

    def level_changed(self):
        self.player.update_global_volume(self.get_volume())

    def update_audio(self, depth, dt):
        self.depth = depth
        self.level_changed()


class Antenna(SubSystem):
    def __init__(self, oned, panel_color, output_color, off_color, max_power_consumption):
        super().__init__(oned, panel_color, output_color, off_color, max_power_consumption)

        self.player = SoundPlayer()
        self.depth = 0

    def get_static_volume(self, world, depth):
        strength_need = (self.depth * AUDIO_QUALITY_DROPOFF) + world.get_static_interference(depth)
        if strength_need == 0:
            return 0
        if strength_need < self.get_strength():
            return 0
        return 1 - (self.get_strength() / strength_need)

    def update_connection(self, world, depth, dt):
        self.player.set_static_volume(self.get_static_volume(world, depth))

class Engine(SubSystem):

    def __init__(self, oned, panel_color, output_color, off_color, max_power_consumption, audio):
        super().__init__(oned, panel_color, output_color, off_color, max_power_consumption)
        self.audio = audio
        self.target_speed = 0
        self.speed = POWER_ON_SPEED

    def update_speed(self, dt):
        self.target_speed = self.get_strength() * MAX_ENGINE_THRUST

        if self.speed < self.target_speed:
            self.speed += ENGINE_SPEED_CHANGE * dt
        elif self.speed > self.target_speed:
            self.speed -= ENGINE_SPEED_CHANGE * dt

        return self.speed

    def engage(self):
        super().engage()
        self.audio.play_repeating(SOUND_ENGINE, self.get_strength())

    def level_changed(self):
        super().level_changed()
        self.audio.update_volume(SOUND_ENGINE, self.get_strength())


def make_static(amount = 100, static_depth = 100):
    images = []
    for i in range(0, amount):
        image = make_static_image(static_depth)
        images.append(image)
    return AnimatedArrayImage(images, 1)


def make_static_image(amount = 100):
    colors = []
    for i in range(0, amount):
        color = DAMAGE_COLORS[random.randint(0, len(DAMAGE_COLORS) - 1)]
        colors.append(color)
    return ArrayImage(colors)
