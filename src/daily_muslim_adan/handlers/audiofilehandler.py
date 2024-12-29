import playsound
import time
import pygame


def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Wait until the music stops
        time.sleep(1)