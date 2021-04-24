from oned import Point
from consts import *
from subsystem import SubSystem, PowerPlant, Battery

class Sub:
    def __init__(self, oned):
        self.oned = oned
        self.graphic = Point((200, 200, 200))
        self.held = True
        self.depth = 10
        self.speed = 0
        self.target_speed = 0
        self.system = [
            SubSystem(oned, (255, 0, 0), (150, 0, 0), (0, 0, 0), 200),
            SubSystem(oned, (0, 255, 0), (0, 150, 0), (0, 0, 0), 200),
            SubSystem(oned, (0, 0, 255), (0, 0, 150), (0, 0, 0), 200),
            SubSystem(oned, (255, 255, 0), (150, 150, 0), (0, 0, 0), 200),
            SubSystem(oned, (0, 255, 255), (0, 150, 150), (0, 0, 0), 200),
            SubSystem(oned, (255, 0, 255), (150, 0, 150), (0, 0, 0), 200),
            SubSystem(oned, (255, 255, 255), (150, 150, 150), (0, 0, 0), 200),
        ]
        self.power_plant = PowerPlant(oned)
        self.battery = Battery(oned)
        self.powered_up = False
        self.power_use = 0
        self.battery_energy = 0

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

        # speed
        self.target_speed = self.engine().get_level() * MAX_ENGINE_THRUST

        if not self.powered_up:
            if self.depth < SPACE_TO_SURFACE_DEPTH:
                # free-falling
                self.speed += FREEFALL_SPEED * dt
            else:
                self.speed -= WATERBRAKE_SPEED * dt
                if self.speed < POWER_ON_SPEED:
                    self.speed = POWER_ON_SPEED
                    self.powered_up = True
        else:
            if self.speed < self.target_speed:
                self.speed += ENGINE_SPEED_CHANGE * dt
            elif self.speed > self.target_speed:
                self.speed -= ENGINE_SPEED_CHANGE * dt

        self.depth = self.depth + (self.speed * dt)

        # power
        power_usage = 0
        for system in self.systems():
            power_usage += system.get_power_consumption()

        if power_usage > self.get_max_power():
            # drain batteries if possible
            energy_used = (power_usage - self.get_max_power()) * dt
            if energy_used < self.battery_energy:
                self.battery_energy -= energy_used
            else:
                # power issues!
                self.battery_energy = 0
                pass
        else:
            energy_gained = (self.get_max_power() - power_usage) * dt
            self.battery_energy += energy_gained
            if self.battery_energy > self.get_max_battery():
                self.battery_energy = self.get_max_battery()

        self.power_plant.set(power_usage, self.get_max_power())
        self.battery.set(self.battery_energy, self.get_max_battery())

    def systems(self):
        return self.system

    def engine(self):
        return self.system[0]

    def get_power_plant(self):
        return self.power_plant

    def get_battery(self):
        return self.battery

    def get_max_power(self):
        return MAX_POWER_PRODUCTION

    def get_max_battery(self):
        return MAX_BATTERY_CAPACITY