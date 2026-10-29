import pygame
from enum import Enum

class Sounds(Enum):
    Snore : 1
    #unimplemented sound effects
    Laugh : 2
    Sigh  : 3
    Yawn  : 4 

snore = None

def pygame_sound_innit():
    pygame.mixer.init()
    snore = pygame.mixer.Sound("sounds/snore.mp3")
    snore.set_volume(0.3)

def play_sound(play_sound):
    match play_sound:
        case Sounds.Snore:
            snore.play(loops=-1, fade_ms=2000)
        case _:
            return

def play_sound_time(play_sound,num_loops,num_fade_ms):
    match play_sound:
        case Sounds.Snore:
            snore.play(loops=num_loops, fade_ms=num_fade_ms)
        case _:
            return

def stop_sound(sound):
    match sound:
        case Sounds.Snore:
            snore.fadeout(400)
        case _: 
            return




