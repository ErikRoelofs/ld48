from consts import *
import random
from oned import Point

class World:
    def __init__(self):
        self.next_check = 100
        self.biomes = [
        ]
        self.biome_types = [
            ThermalVentsBiome,
            FloatingRocksBiome,
            CryonicVentsBiome,
            StaticDisturbance,
            StrangeNoisy1,
            StrangeNoisy2,
            SonarVisible1,
            SonarVisible2,
            DragonBiome,
            CrabBiome,
            CowBiome
        ]

    def list_biomes(self):
        return self.biome_types

    def update_world(self, depth, sub, dt):
        if depth > self.next_check:
            self.maybe_new_biome(depth)
            self.next_check += random.randint(75, 275)
        for biome in self.biomes:
            biome.update(sub, dt)
            if not biome.is_relevant(depth):
                self.biomes.remove(biome)

    def maybe_new_biome(self, depth):
        # new biome must be out of sonar range
        if random.randint(0, 100) < 50:
            new_type = self.get_new_biome_type(depth)
            if new_type is None:
                return
            size = random.randint(new_type.min_size(), new_type.max_size())
            biome = new_type(depth + 600, depth + 600 + size)
            if self.can_place_biome(biome):
                self.biomes.append(biome)

    def can_place_biome(self, biome):
        for existing in self.biomes:
            if str(existing) == str(biome):
                if existing.start < biome.start < existing.end:
                    return False
                if existing.start < biome.end < existing.end:
                    return False
                if existing.start > biome.start and existing.end < biome.end:
                    return False
        return True

    def get_new_biome_type(self, depth):
        sum_weight = 0
        for biome_type in self.biome_types:
            if biome_type.min_depth_required() < depth:
                sum_weight += biome_type.prevalence()
        if sum_weight == 0:
            return None
        picked = random.randint(0, sum_weight)
        for biome_type in self.biome_types:
            if biome_type.min_depth_required() < depth:
                picked -= biome_type.prevalence()
                if picked < 0:
                    return biome_type

    def get_temperature(self, depth):
        if depth < SPACE_TO_SURFACE_DEPTH:
            return MIN_TEMPERATURE

        base_temperature = 150 + (depth / 3)
        for biome in self.biomes:
            base_temperature += (biome.temperature_flat_change() * biome.strength(depth))
        for biome in self.biomes:
            base_temperature *= ((biome.temperature_modifier() - 1) * biome.strength(depth)) + 1

        if base_temperature > MAX_TEMPERATURE:
            return MAX_TEMPERATURE
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

    def get_nearby_object_speed(self, depth):
        base_objects_speed = 0
        for biome in self.biomes:
            base_objects_speed += biome.nearby_objects_speed_flat_change()
        return base_objects_speed

    def get_new_sounds_at(self, depth):
        sounds = {}
        for biome in self.biomes:
            if biome.strength(depth) > 0 and biome.get_sound():
                sound = biome.get_sound()
                if sound not in sounds: # only add once - further out biomes can't be heard
                    sounds[sound] = biome.volume(depth)
        return sounds

    def get_sonar_color(self, depth, strength):
        for biome in self.biomes:
            if biome.start < depth < biome.end and biome.shows_on_sonar():
                return biome.get_sonar_color(strength)
        return None

    def get_biomes(self, depth):
        active = []
        for biome in self.biomes:
            if biome.start < depth < biome.end:
                active.append(biome)
        return active

class Biome:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def prevalence():
        return 150

    @staticmethod
    def min_size():
        return 100

    @staticmethod
    def max_size():
        return 500

    @staticmethod
    def min_depth_required():
        return SPACE_TO_SURFACE_DEPTH

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

    def nearby_objects_speed_flat_change(self):
        return 0

    def is_relevant(self, depth):
        return depth < self.end + BIOME_EFFECT_DISTANCE

    def shows_on_sonar(self):
        return False

    def get_sonar_color(self, strength):
        return Point((255 * strength, 255 * strength, 255 * strength))

    def volume(self, depth):
        return self.strength(depth)

    def update(self, sub, dt):
        pass

    @staticmethod
    def science_color():
        return Point((255, 255, 255))

    @staticmethod
    def name():
        return 'name'

    def __str__(self):
        return self.name()

class ThermalVentsBiome(Biome):
    def temperature_flat_change(self):
        return MAX_TEMPERATURE

    def get_sound(self):
        return SOUND_HOTSPOT

    @staticmethod
    def name():
        return 'thermal vents'

    @staticmethod
    def science_color():
        return Point((128, 0, 0))

class CryonicVentsBiome(Biome):
    def temperature_flat_change(self):
        return MIN_TEMPERATURE

    def get_sound(self):
        return SOUND_COLDSPOT

    @staticmethod
    def name():
        return 'cryonic vents'

    @staticmethod
    def science_color():
        return Point((150, 200, 255))

class FloatingRocksBiome(Biome):
    def nearby_objects_flat_change(self):
        return 0.6

    def nearby_objects_mass_flat_change(self):
        return 0.5

    def shows_on_sonar(self):
        return True

    def get_sonar_color(self, strength):
        return Point((0 * ((1 + strength) / 2), 255 * ((1 + strength) / 2), 0 * ((1 + strength) / 2)))

    @staticmethod
    def name():
        return 'floating rocks'

    @staticmethod
    def science_color():
        return Point((125, 125, 125))

class StaticDisturbance(Biome):
    def static_base_flat_change(self):
        return 0.3

    def shows_on_sonar(self):
        return True

    def get_sonar_color(self, strength):
        return Point((0, 0, 255 * ((1 + strength) / 2)))

    @staticmethod
    def name():
        return 'static disturbance'

    @staticmethod
    def science_color():
        return Point((255, 255, 255))


class StrangeNoisy1(Biome):
    def get_sound(self):
        return SOUND_WEIRD1

    @staticmethod
    def name():
        return 'strange noise 1'

    def volume(self, depth):
        return self.strength(depth) / 3

    @staticmethod
    def prevalence():
        return 25

    @staticmethod
    def min_depth_required():
        return 1500

    @staticmethod
    def science_color():
        return Point((100, 255, 125))


class StrangeNoisy2(Biome):
    def get_sound(self):
        return SOUND_WEIRD2

    @staticmethod
    def name():
        return 'strange noise 2'

    def volume(self, depth):
        return self.strength(depth) / 2

    @staticmethod
    def prevalence():
        return 50

    @staticmethod
    def min_depth_required():
        return 1000

    @staticmethod
    def science_color():
        return Point((255, 100, 125))


class SonarVisible1(Biome):
    def shows_on_sonar(self):
        return True

    def get_sonar_color(self, strength):
        return Point((255 * ((1 + strength) / 2), 0, 255 * ((1 + strength) / 2)))

    @staticmethod
    def name():
        return 'sonar visible 1'

    @staticmethod
    def prevalence():
        return 50

    @staticmethod
    def min_depth_required():
        return 800

    @staticmethod
    def science_color():
        return Point((255, 0, 255))


class SonarVisible2(Biome):
    def shows_on_sonar(self):
        return True

    def get_sonar_color(self, strength):
        return Point((255 * ((1 + strength) / 2), 128 * ((1 + strength) / 2), 128 * ((1 + strength) / 2)))

    @staticmethod
    def name():
        return 'sonar visible 2'

    @staticmethod
    def prevalence():
        return 30

    @staticmethod
    def min_depth_required():
        return 1400

    @staticmethod
    def science_color():
        return Point((255, 128, 128))

class DragonBiome(Biome):

    def __init__(self, start, end):
        super().__init__(start, end)
        self.monster_distance = random.randint(40, 80)
        self.scan = 0
        self.approaching = False
        self.waiting = True
        self.leaving = False
        self.lost_interest = False
        self.speed = 10
        self.last_heard = 0

    @staticmethod
    def name():
        return 'dragon'

    @staticmethod
    def prevalence():
        return 30

    @staticmethod
    def min_depth_required():
        return 1700

    def get_sound(self):
        return SOUND_DRAGON

    def volume(self, depth):
        return 1 - (pow(self.monster_distance, 2) / 10000)

    def nearby_objects_flat_change(self):
        if self.monster_distance > 20:
            return 0
        self.lost_interest = True
        return 10  # near certain hit

    def nearby_objects_mass_flat_change(self):
        return 10  # probably instant death

    def nearby_objects_speed_flat_change(self):
        return 1

    def update(self, sub, dt):
        if self.lost_interest:
            self.monster_distance += dt * self.speed
            return

        self.scan += dt
        self.last_heard += dt
        if self.last_heard > 10:
            self.lost_interest = True

        if self.scan > 0.5:
            self.scan -= 0.5
            # listen for the sub
            if random.randint(0, 50) < sub.noise() * 100:
                # heard it
                self.last_heard = 0
                self.approaching = True
                self.waiting = False
                self.leaving = False
            else:
                behavior = random.randint(0, 100)
                if behavior < 60:
                    # wait
                    self.approaching = False
                    self.waiting = True
                    self.leaving = False
                elif behavior < 85:
                    # leave
                    self.approaching = False
                    self.waiting = False
                    self.leaving = True
                else:
                    # approach
                    self.approaching = True
                    self.waiting = False
                    self.leaving = False

        if self.approaching:
            self.monster_distance -= dt * self.speed
        if self.leaving:
            self.monster_distance += dt * self.speed

    def is_relevant(self, depth):
        if self.monster_distance > 100:
            return False
        return depth < self.end + BIOME_EFFECT_DISTANCE

    @staticmethod
    def science_color():
        return Point((255, 0, 0))


class CrabBiome(Biome):

    def __init__(self, start, end):
        super().__init__(start, end)
        self.monster_distance = random.randint(40, 80)
        self.scan = 0
        self.approaching = False
        self.waiting = True
        self.leaving = False
        self.lost_interest = False
        self.speed = 15
        self.last_heard = 0

    @staticmethod
    def name():
        return 'crab'

    @staticmethod
    def prevalence():
        return 30

    @staticmethod
    def min_depth_required():
        return 1700

    def get_sound(self):
        return SOUND_CRAB

    def volume(self, depth):
        return 1 - (pow(self.monster_distance, 2) / 10000)

    def nearby_objects_flat_change(self):
        if self.monster_distance > 20:
            return 0
        self.lost_interest = True
        return 1

    def nearby_objects_mass_flat_change(self):
        return 0.5

    def nearby_objects_speed_flat_change(self):
        return 1

    def update(self, sub, dt):
        if self.lost_interest:
            self.monster_distance += dt * self.speed
            return

        self.scan += dt
        self.last_heard += dt
        if self.last_heard > 10:
            self.lost_interest = True

        if self.scan > 0.5:
            self.scan -= 0.5
            # listen for the sub
            if random.randint(0, 90) < sub.noise() * 100:
                # heard it
                self.last_heard = 0
                self.approaching = True
                self.waiting = False
                self.leaving = False
            else:
                behavior = random.randint(0, 100)
                if behavior < 30:
                    # wait
                    self.approaching = False
                    self.waiting = True
                    self.leaving = False
                elif behavior < 65:
                    # leave
                    self.approaching = False
                    self.waiting = False
                    self.leaving = True
                else:
                    # approach
                    self.approaching = True
                    self.waiting = False
                    self.leaving = False

        if self.approaching:
            self.monster_distance -= dt * self.speed
        if self.leaving:
            self.monster_distance += dt * self.speed

    def is_relevant(self, depth):
        if self.monster_distance > 100:
            return False
        return depth < self.end + BIOME_EFFECT_DISTANCE

    @staticmethod
    def science_color():
        return Point((255, 50, 180))


class CowBiome(Biome):

    def __init__(self, start, end):
        super().__init__(start, end)
        self.monster_distance = random.randint(40, 80)
        self.scan = 0
        self.approaching = False
        self.waiting = True
        self.leaving = False
        self.lost_interest = False
        self.speed = 10
        self.last_heard = 0

    @staticmethod
    def name():
        return 'cow'

    @staticmethod
    def prevalence():
        return 30

    @staticmethod
    def min_depth_required():
        return 1700

    def get_sound(self):
        return SOUND_COW

    def volume(self, depth):
        return 1 - (pow(self.monster_distance, 2) / 10000)

    def nearby_objects_flat_change(self):
        if self.monster_distance > 20:
            return 0
        self.lost_interest = True
        return 1

    def nearby_objects_mass_flat_change(self):
        return 0.6

    def nearby_objects_speed_flat_change(self):
        return 1

    def update(self, sub, dt):
        if self.lost_interest:
            self.monster_distance += dt * self.speed
            return

        self.scan += dt
        self.last_heard += dt
        if self.last_heard > 20:
            self.lost_interest = True

        if self.scan > 0.5:
            self.scan -= 0.5
            behavior = random.randint(0, 100)
            if behavior < 40:
                # wait
                self.approaching = False
                self.waiting = True
                self.leaving = False
            elif behavior < 80:
                # leave
                self.approaching = False
                self.waiting = False
                self.leaving = True
            else:
                # approach
                self.approaching = True
                self.waiting = False
                self.leaving = False

        if self.approaching:
            self.monster_distance -= dt * self.speed
        if self.leaving:
            self.monster_distance += dt * self.speed

    def is_relevant(self, depth):
        if self.monster_distance > 100:
            return False
        return depth < self.end + BIOME_EFFECT_DISTANCE

    @staticmethod
    def science_color():
        return Point((120, 178, 130))
