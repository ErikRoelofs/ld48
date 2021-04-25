from oned import Point
from consts import *
from subsystem import SubSystem, PowerPlant, Battery, Heat, Audio, Engine, Antenna
import random

class Sub:
    def __init__(self, oned, world):
        self.oned = oned
        self.graphic = Point((200, 200, 200))
        self.held = True
        self.depth = 10
        self.speed = 0
        self.target_speed = 0
        audio_sys = Audio(oned, (0, 255, 255), (0, 150, 150), (0, 0, 0), 200)
        self.system = [
            Engine(oned, (255, 0, 0), (150, 0, 0), (0, 0, 0), 200, audio_sys),
            SubSystem(oned, (0, 255, 0), (0, 150, 0), (0, 0, 0), 200),
            SubSystem(oned, (0, 0, 255), (0, 0, 150), (0, 0, 0), 200),
            SubSystem(oned, (255, 255, 0), (150, 150, 0), (0, 0, 0), 200),
            audio_sys,
            Antenna(oned, (255, 0, 255), (150, 0, 150), (0, 0, 0), 200),
            SubSystem(oned, (255, 255, 255), (150, 150, 150), (0, 0, 0), 200),
        ]
        self.power_plant = PowerPlant(oned)
        self.battery = Battery(oned)
        self.powered_up = False
        self.power_use = 0
        self.battery_energy = 0
        self.temperature = -150
        self.heat = Heat(oned)
        self.world = world
        self.overheat_damage_counter = 0
        self.has_impacted = False

    def draw(self, position):
        self.oned.draw(self.graphic, position - 4, position + 4)

    def is_held(self):
        return self.held

    def drop(self):
        self.held = False
        self.audio().play(SOUND_RELEASE, 1)

    def get_depth(self):
        return self.depth

    def update(self, dt):
        if self.held:
            return

        # power
        power_usage = 0
        for system in self.system:
            power_usage += system.get_power_consumption()
        power_availability = self.power_plant.update_power(power_usage, self.heat.get(), self.battery, dt)
        for system in self.system:
            system.set_available_power(power_availability)

        # speed
        if not self.powered_up:
            if self.depth < SPACE_TO_SURFACE_DEPTH:
                # free-falling
                self.speed += FREEFALL_SPEED * dt
            else:
                # impact splash
                if not self.has_impacted:
                    self.has_impacted = True
                    self.audio().play(SOUND_SPLASH, 1)

                # waterbreaking before the power goes on
                self.speed -= WATERBRAKE_SPEED * dt
                if self.speed < POWER_ON_SPEED:
                    self.speed = POWER_ON_SPEED
                    for system in self.system:
                        system.engage()
                    self.powered_up = True
        else:
            self.speed = self.engine().update_speed(dt)

        # depth
        self.depth = self.depth + (self.speed * dt)

        # temperature
        self.get_heat().update_heat(self, self.world, dt)

        # audio
        self.audio().update_audio(self.depth, dt)

        # connection
        self.antenna().update_connection(self.world, self.depth, dt)

    def systems(self):
        return self.system

    def engine(self):
        return self.system[0]

    def climate_control(self):
        return self.system[6]

    def audio(self):
        return self.system[4]

    def get_power_plant(self):
        return self.power_plant

    def get_battery(self):
        return self.battery

    def antenna(self):
        return self.system[5]

    def get_max_power(self):
        if self.temperature > SUB_FREEZING_TRESHOLD:
            return MAX_POWER_PRODUCTION
        max_power_loss = abs(MIN_TEMPERATURE - SUB_FREEZING_TRESHOLD)
        below_treshold = SUB_FREEZING_TRESHOLD - self.temperature
        percentage = below_treshold / max_power_loss
        power_cut = percentage * MAX_POWER_PRODUCTION_LOSS_PERCENTAGE
        return MAX_POWER_PRODUCTION * (1 - power_cut)

    def get_normal_max_power(self):
        return MAX_POWER_PRODUCTION

    def get_max_battery(self):
        return MAX_BATTERY_CAPACITY

    def get_heat(self):
        return self.heat

    def get_rand_sys(self):
        return self.system[random.randint(0, len(self.system) - 1)]

