from consts import *
import random
from oned import Point

class World:
    def __init__(self):
        self.next_check = 100
        self.biomes = [
#            FloatingRocksBiome(300, 600),
#            ThermalVentsBiome(500, 1000),
#            StaticDisturbance(500, 900)
        ]
        self.biome_types = [
            ThermalVentsBiome,
            FloatingRocksBiome,
            CryonicVentsBiome,
            StaticDisturbance
        ]

    def update_world(self, depth, dt):
        if depth > self.next_check:
            self.maybe_new_biome(depth)
            self.next_check += random.randint(75, 275)
        for biome in self.biomes:
            if not biome.is_relevant(depth):
                self.biomes.remove(biome)

    def maybe_new_biome(self, depth):
        # new biome must be out of sonar range
        if random.randint(0, 100) < 50:
            new_type = self.get_new_biome_type()
            size = random.randint(new_type.min_size(), new_type.max_size())
            self.biomes.append(new_type(depth + 600, depth + 600 + size))

    def get_new_biome_type(self):
        sum_weight = 0
        for biome_type in self.biome_types:
            sum_weight += biome_type.prevalence()
        picked = random.randint(0, sum_weight)
        for biome_type in self.biome_types:
            picked -= biome_type.prevalence()
            if picked < 0:
                return biome_type

    def get_temperature(self, depth):
        if depth < SPACE_TO_SURFACE_DEPTH:
            return MIN_TEMPERATURE

        base_temperature = 150 + (depth / 100)
        for biome in self.biomes:
            base_temperature += (biome.temperature_flat_change() * biome.strength(depth))
        for biome in self.biomes:
            base_temperature *= ((biome.temperature_modifier() - 1) * biome.strength(depth)) + 1

        return base_temperature

    def get_static_interference(self, depth):
        base_interference = 0
        for biome in self.biomes:
            base_interference += (biome.static_base_flat_change() * biome.strength(depth))
        for biome in self.biomes:
            base_interference *= ((biome.static_modifier() - 1) * biome.strength(depth)) + 1
        return base_interference

    def get_nearby_objects(self, depth):
        base_objects = 0
        for biome in self.biomes:
            base_objects += (biome.nearby_objects_flat_change() * biome.strength(depth))
        for biome in self.biomes:
            base_objects *= ((biome.nearby_objects_modifier() - 1) * biome.strength(depth)) + 1
        return base_objects

    def get_nearby_object_mass(self, depth):
        base_objects_mass = 0
        for biome in self.biomes:
            base_objects_mass += (biome.nearby_objects_mass_flat_change() * biome.strength(depth))
        for biome in self.biomes:
            base_objects_mass *= ((biome.nearby_objects_mass_modifier() - 1) * biome.strength(depth)) + 1
        return base_objects_mass

    def get_new_sounds_at(self, depth):
        sounds = {}
        for biome in self.biomes:
            if biome.strength(depth) > 0 and biome.get_sound():
                sound = biome.get_sound()
                if sound not in sounds: # only add once - further out biomes can't be heard
                    sounds[sound] = biome.strength(depth)
        return sounds

    def get_sonar_color(self, depth):
        for biome in self.biomes:
            if biome.start < depth < biome.end and biome.shows_on_sonar():
                return biome.get_sonar_color()
        return None

class Biome:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.sound_playing = False

    @staticmethod
    def prevalence():
        return 100

    @staticmethod
    def min_size():
        return 100

    @staticmethod
    def max_size():
        return 500

    def strength(self, depth):
        # full strength between start & end
        if self.start < depth < self.end:
            return 1
        # growing for 200 units in & out
        if 0 < self.start - depth < BIOME_EFFECT_DISTANCE:
            return 1 - ((self.start - depth) / BIOME_EFFECT_DISTANCE)
        if 0 < depth - self.end < BIOME_EFFECT_DISTANCE:
            return 1 - ((depth - self.end) / BIOME_EFFECT_DISTANCE)
        return 0

    def get_sound(self):
        return None

    def temperature_modifier(self):
        return 1

    def static_modifier(self):
        return 1

    def nearby_objects_modifier(self):
        return 1

    def nearby_objects_mass_modifier(self):
        return 1

    def temperature_flat_change(self):
        return 0

    def static_base_flat_change(self):
        return 0

    def nearby_objects_flat_change(self):
        return 0

    def nearby_objects_mass_flat_change(self):
        return 0

    def is_relevant(self, depth):
        return depth < self.end + BIOME_EFFECT_DISTANCE

    def shows_on_sonar(self):
        return False

    def get_sonar_color(self):
        return (255, 255, 255)

class ThermalVentsBiome(Biome):
    def temperature_flat_change(self):
        return 400

    def get_sound(self):
        return SOUND_HOTSPOT

class CryonicVentsBiome(Biome):
    def temperature_flat_change(self):
        return -250

    def get_sound(self):
        return SOUND_COLDSPOT

class FloatingRocksBiome(Biome):
    def nearby_objects_flat_change(self):
        return 0.6

    def nearby_objects_mass_flat_change(self):
        return 0.5

    def shows_on_sonar(self):
        return True

    def get_sonar_color(self):
        return Point((100, 100, 100))


class StaticDisturbance(Biome):
    def static_base_flat_change(self):
        return 0.3

    def shows_on_sonar(self):
        return True

    def get_sonar_color(self):
        return Point((0, 0, 255))
