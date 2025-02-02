import pygame
import time

# Initialize the mixer
pygame.mixer.init()

# Load and play the audio file
pygame.mixer.music.load("../adan2.mp3")
pygame.mixer.music.play()

# Perform other tasks while the audio plays
for i in range(5):
    print(f"Task {i+1}: Doing something else...")
    time.sleep(1)

# Wait until the audio finishes before exiting
while pygame.mixer.music.get_busy():
    print("now waiting")
    time.sleep(0.1)