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
        self.engine_sound = pygame.mixer.Sound("sounds/engine.wav")

        self.impact1 = pygame.mixer.Sound("sounds/impacts/impact1.wav")
        self.impact2 = pygame.mixer.Sound("sounds/impacts/impact2.wav")
        self.impact3 = pygame.mixer.Sound("sounds/impacts/impact3.wav")
        self.impact4 = pygame.mixer.Sound("sounds/impacts/impact4.wav")

        self.ambiant = pygame.mixer.Sound("sounds/ambiance/ambiance.wav")

        self.coldspot = pygame.mixer.Sound("sounds/coldspot.wav")
        self.hotspot = pygame.mixer.Sound("sounds/boiling.wav")
        self.weird1 = pygame.mixer.Sound("sounds/weirdness1.wav")
        self.weird2 = pygame.mixer.Sound("sounds/weirdness2.wav")
        self.dragon = pygame.mixer.Sound("sounds/creatures/dragon.wav")
        self.crab = pygame.mixer.Sound("sounds/creatures/crab.wav")
        self.cow = pygame.mixer.Sound("sounds/creatures/seacow-monster.wav")
        self.sonar = pygame.mixer.Sound("sounds/sonar.wav")

        self.all_sounds = [
            self.release_sound,
            self.splash_sound,
            self.engine_sound,
            self.impact1,
            self.impact2,
            self.impact3,
            self.impact4,
            self.ambiant,
            self.hotspot,
            self.coldspot,
            self.sonar,
            self.weird1,
            self.weird2,
            self.dragon,
            self.crab,
            self.cow,
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
            self.coldspot: 1,
            self.hotspot: 1,
            self.sonar: 1,
            self.weird1: 1,
            self.weird2: 1,
            self.dragon: 1,
            self.crab: 1,
            self.cow: 1,
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
        if command == SOUND_HOTSPOT:
            return self.hotspot
        if command == SOUND_COLDSPOT:
            return self.coldspot
        if command == SOUND_SONAR:
            return self.sonar
        if command == SOUND_WEIRD1:
            return self.weird1
        if command == SOUND_WEIRD2:
            return self.weird2
        if command == SOUND_DRAGON:
            return self.dragon
        if command == SOUND_CRAB:
            return self.crab
        if command == SOUND_COW:
            return self.cow

        raise ValueError("No sound for: " + str(command))

    def play_sound(self, command, volume):
        to_play = self.get_sound(command)
        self.sound_volumes[to_play] = volume
        to_play.set_volume(volume * self.global_volume)
        if to_play.get_num_channels() == 0:
            to_play.play()
            if command == SOUND_SPLASH:
                to_play.fadeout(1500)

    def play_repeating(self, command, volume):
        to_play = self.get_sound(command)
        self.sound_volumes[to_play] = volume
        to_play.set_volume(volume * self.global_volume)
        if to_play.get_num_channels() == 0:
            to_play.play(-1)

    def stop_repeating_sound(self, command):
        to_play = self.get_sound(command)
        to_play.stop()

    def play_ambiant_sound(self, volume):
        self.play_repeating(SOUND_AMBIENT, volume)

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

