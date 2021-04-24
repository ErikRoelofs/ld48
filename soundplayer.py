import pygame
from consts import *

release_sound = pygame.mixer.Sound("sounds/release.wav")
splash_sound = pygame.mixer.Sound("sounds/splash.wav")
engine_sound = pygame.mixer.Sound("sounds/engine.wav")

def play_sound(command, volume):
    to_play = None
    if command == SOUND_SPLASH:
        splash_sound.fadeout(1500)
        to_play = splash_sound
    if command == SOUND_RELEASE:
        to_play = release_sound

    if not to_play:
        raise ValueError("No sound for: " + str(command))

    to_play.set_volume(volume)
    to_play.play()


def play_repeating(command, volume):
    to_play = None
    if command == SOUND_ENGINE:
        print("playing engine sound at " + str(volume))
        to_play = engine_sound

    if not to_play:
        raise ValueError("No sound for: " + str(command))

    to_play.set_volume(volume)
    to_play.play(-1)


def update_volume(command, new_volume):
    to_play = None
    if command == SOUND_ENGINE:
        to_play = engine_sound

    if not to_play:
        raise ValueError("No sound for: " + str(command))

    to_play.set_volume(new_volume)
