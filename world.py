from consts import *

class World:
    def __init__(self):
        pass

    def get_temperature(self, depth):
        return 0

    def get_static_interference(self, depth):
        return 0

    def get_nearby_objects(self, depth):
        return 1

    def get_nearby_object_mass(self, depth):
        return 1.5
