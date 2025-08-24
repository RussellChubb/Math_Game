import pygame, time

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

sound = pygame.mixer.Sound("correct.wav")
sound.set_volume(1.0)

print("Playing sound...")
sound.play()
time.sleep(2)  # keep script alive long enough to hear it
