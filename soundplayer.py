import pygame
from consts import *


class SoundPlayer:
    def __init__(self):
        self.global_volume = 1

        self.release_sound = pygame.mixer.Sound("sounds/release.wav")
        self.splash_sound = pygame.mixer.Sound("sounds/splash.wav")
        self.splash_sound.fadeout(1500)
        self.engine_sound = pygame.mixer.Sound("sounds/engine.wav")

        self.all_sounds = [
            self.release_sound, self.splash_sound, self.engine_sound
        ]

    def get_sound(self, command):
        if command == SOUND_SPLASH:
            return self.splash_sound
        if command == SOUND_RELEASE:
            return self.release_sound
        if command == SOUND_ENGINE:
            return self.engine_sound
        raise ValueError("No sound for: " + str(command))

    def play_sound(self, command, volume):
        to_play = self.get_sound(command)
        to_play.set_volume(volume)
        to_play.play()

    def play_repeating(self, command, volume):
        to_play = self.get_sound(command)
        to_play.set_volume(volume)
        to_play.play(-1)

    def update_volume(self, command, new_volume):
        to_play = None
        if command == SOUND_ENGINE:
            to_play = self.engine_sound

        if not to_play:
            raise ValueError("No sound for: " + str(command))

        to_play.set_volume(new_volume)

    def update_global_volume(self, new_global_volume):
        self.global_volume = new_global_volume
        for sound in self.all_sounds:
            sound.set_volume(sound.get_volume() * new_global_volume)