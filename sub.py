from oned import Point
from consts import *
from subsystem import SubSystem, PowerPlant, Battery, Heat

class Sub:
    def __init__(self, oned, world):
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
        self.temperature = -150
        self.heat = Heat(oned)
        self.world = world

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

        # power
        power_availability = 1
        power_usage = 0
        for system in self.systems():
            power_usage += system.get_power_consumption()

        if power_usage > self.get_max_power():
            # drain batteries if possible
            energy_used = (power_usage - self.get_max_power()) * dt
            if energy_used < self.battery_energy:
                self.battery_energy -= energy_used
            else:
                # power issues! reduce availability allround
                self.battery_energy = 0
                power_availability = self.get_max_power() / power_usage
                pass
        else:
            energy_gained = (self.get_max_power() - power_usage) * dt
            self.battery_energy += energy_gained
            if self.battery_energy > self.get_max_battery():
                self.battery_energy = self.get_max_battery()

        self.power_plant.set(power_usage, self.get_max_power(), self.get_normal_max_power())
        self.battery.set(self.battery_energy, self.get_max_battery())

        # speed
        self.target_speed = self.engine().get_level(power_availability) * MAX_ENGINE_THRUST

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

        # temperature
        correct = self.climate_control().get_level(power_availability) * MAX_CLIMATE_CONTROL_CORRECT * dt
        if self.temperature > IDEAL_TEMPERATURE:
            self.temperature -= correct
        elif self.temperature < IDEAL_TEMPERATURE:
            self.temperature += correct

        outside_temp = self.world.get_temperature(self.depth)
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

        self.heat.set(self.temperature)


    def systems(self):
        return self.system

    def engine(self):
        return self.system[0]

    def climate_control(self):
        return self.system[6]

    def get_power_plant(self):
        return self.power_plant

    def get_battery(self):
        return self.battery

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