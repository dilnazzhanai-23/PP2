import pygame
import os
from clock import MickeyClock  

pygame.init()

screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Mickey Clock")

WHITE = (255, 255, 255)

current_dir = os.path.dirname(__file__)
images_path = os.path.join(current_dir, "images")


mickey_clock = MickeyClock(images_path)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    
    mickey_clock.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()