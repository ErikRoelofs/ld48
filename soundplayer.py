import pygame
from consts import *
import random


class SoundPlayer:
    def __init__(self):
        self.global_volume = 1
        self.static = None
        self.play_static()

        self.release_sound = pygame.mixer.Sound("sounds/release.wav")
        self.splash_sound = pygame.mixer.Sound("sounds/splash.wav")
        self.splash_sound.fadeout(1500)
        self.engine_sound = pygame.mixer.Sound("sounds/engine.wav")

        self.impact1 = pygame.mixer.Sound("sounds/impacts/impact1.wav")
        self.impact2 = pygame.mixer.Sound("sounds/impacts/impact2.wav")
        self.impact3 = pygame.mixer.Sound("sounds/impacts/impact3.wav")
        self.impact4 = pygame.mixer.Sound("sounds/impacts/impact4.wav")

        self.ambiant = pygame.mixer.Sound("sounds/ambiance/ambiance.wav")

        self.all_sounds = [
            self.release_sound, self.splash_sound, self.engine_sound, self.impact1, self.impact2, self.impact3, self.impact4,self.ambiant
        ]
        self.sound_volumes = {
            self.release_sound: 1,
            self.splash_sound: 1,
            self.engine_sound: 1,
            self.impact1: 1,
            self.impact2: 1,
            self.impact3: 1,
            self.impact4: 1,
            self.ambiant: 1,
        }

    def play_static(self):
        # static is a special case, so it's not in "all sounds"
        self.static = pygame.mixer.Sound("sounds/static.wav")
        # initially, not audible
        self.static.set_volume(0)
        self.static.play(-1)


    def get_sound(self, command):
        if command == SOUND_SPLASH:
            return self.splash_sound
        if command == SOUND_RELEASE:
            return self.release_sound
        if command == SOUND_ENGINE:
            return self.engine_sound
        if command == SOUND_IMPACT_RANDOM:
            sound = random.randint(1, 4)
            if sound == 1:
                return self.impact1
            if sound == 2:
                return self.impact2
            if sound == 3:
                return self.impact3
            if sound == 4:
                return self.impact4
        if command == SOUND_AMBIENT:
            return self.ambiant

        raise ValueError("No sound for: " + str(command))

    def play_sound(self, command, volume):
        to_play = self.get_sound(command)
        self.sound_volumes[to_play] = volume
        to_play.set_volume(volume * self.global_volume)
        to_play.play()

    def play_repeating(self, command, volume):
        to_play = self.get_sound(command)
        self.sound_volumes[to_play] = volume
        to_play.set_volume(volume * self.global_volume)
        to_play.play(-1)

    def play_ambiant_sound(self, volume):
        self.play_sound(SOUND_AMBIENT, volume)

    def update_volume(self, command, new_volume):
        to_play = self.get_sound(command)
        self.sound_volumes[to_play] = new_volume
        to_play.set_volume(new_volume * self.global_volume)

    def update_global_volume(self, new_global_volume):
        self.global_volume = new_global_volume
        for sound in self.all_sounds:
            sound.set_volume(self.sound_volumes[sound] * new_global_volume)

    def set_static_volume(self, volume):
        self.static.set_volume(volume)
