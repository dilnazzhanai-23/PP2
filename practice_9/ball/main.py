import pygame
from ball import Ball
pygame.init()

w=600
h=600
WHITE = (255, 255, 255)

screen=pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

ball = Ball(300, 300, 25, 20)
running=True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys=pygame.key.get_pressed()
    ball.move(keys,w,h)
    ball.draw(screen)

    pygame.display.update()
    clock.tick(60)




pygame.quit()