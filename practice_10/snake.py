import pygame
import random

# Initialization
pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
black=(0,0,0)
white=(255,255,255) 
red = (255,0,0)
green =(0,255,0)

# Game Variables
snake_pos = [300, 200]
snake_body = [[300, 200]]
direction = 'RIGHT'
change_to = direction

food_pos = [random.randrange(1, (width//20)) * 20, random.randrange(1, (height//20)) * 20]
food_spawn = True

score = 0
level = 1
speed = 5  

# Game Loop
run = True
while run:
    # Check for Key Presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to

    # Move the Snake
    if direction == 'UP':    snake_pos[1] -= 20
    if direction == 'DOWN':  snake_pos[1] += 20
    if direction == 'LEFT':  snake_pos[0] -= 20
    if direction == 'RIGHT': snake_pos[0] += 20

    # Logic: Snake Growth 
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
        # LEVEL LOGIC: Every 3 foods, increase level and speed
        if score % 3 == 0:
            level += 1
            speed += 3 
    else:
        snake_body.pop()

    # Logic: Random Food 
    if not food_spawn:
        while True:
            food_pos = [random.randrange(1, (width//20)) * 20, 
                        random.randrange(1, (height//20)) * 20]
            # Make sure food isn't inside the snake body
            if food_pos not in snake_body:
                break
        food_spawn = True

    # Logic: Border Collision 
    if snake_pos[0] < 0 or snake_pos[0] > width-20 or \
       snake_pos[1] < 0 or snake_pos[1] > height-20:
        run = False # Game Over

    # Logic: Body Collision 
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            run = False

    # Drawing Everything 
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 20, 20))
    
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 20, 20))

    # Draw Score & Level 
    font = pygame.font.SysFont('arial', 20)
    score_surf = font.render(f'Score: {score}  Level: {level}', True, white)
    screen.blit(score_surf, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()