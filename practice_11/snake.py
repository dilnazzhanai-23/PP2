import pygame
import random

# Initialization
pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255) 
red = (255, 0, 0)      # Weight 1
orange = (255, 165, 0) # Weight 3
purple = (128, 0, 128) # Weight 5
green = (0, 255, 0)

# Game Variables
snake_pos = [300, 200]
snake_body = [[300, 200]]
direction = 'RIGHT'
change_to = direction

# Food Variables
food_pos = [random.randrange(1, (width//20)) * 20, random.randrange(1, (height//20)) * 20]
food_spawn = True
food_weight = 1
food_color = red
food_timer_start = pygame.time.get_ticks() # Get current time in ms
food_lifetime = 5000 # Food lasts 5 seconds

score = 0
level = 1
speed = 7 

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
    
    # Check if Food is eaten
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += food_weight
        food_spawn = False
        # LEVEL LOGIC: Every 10 points (roughly), increase level and speed
        if score // 10 >= level:
            level += 1
            speed += 2
    else:
        snake_body.pop()

    # Timer Expiry (If food isn't eaten in time)
    current_time = pygame.time.get_ticks()
    if current_time - food_timer_start > food_lifetime:
        food_spawn = False # Force a respawn if time is up

    # Random Food Respawn
    if not food_spawn:
        while True:
            food_pos = [random.randrange(1, (width//20)) * 20, 
                        random.randrange(1, (height//20)) * 20]
            if food_pos not in snake_body:
                break
        
        # Randomize Weight and Color
        # 70% chance weight 1, 20% weight 3, 10% weight 5
        rand_val = random.randint(1, 10)
        if rand_val <= 7:
            food_weight = 1
            food_color = red
        elif rand_val <= 9:
            food_weight = 3
            food_color = orange
        else:
            food_weight = 5
            food_color = purple
            
        food_timer_start = pygame.time.get_ticks() # Reset timer for new food
        food_spawn = True

    # Border Collision 
    if snake_pos[0] < 0 or snake_pos[0] > width-20 or \
       snake_pos[1] < 0 or snake_pos[1] > height-20:
        run = False 

    # Body Collision 
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            run = False

    # Drawing  
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 20, 20))
    
    # Draw Food with its specific color
    pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], 20, 20))

    # Draw Score, Level, and a simple Time Left indicator
    font = pygame.font.SysFont('arial', 20)
    time_left = max(0, (food_lifetime - (current_time - food_timer_start)) // 1000)
    
    score_surf = font.render(f'Score: {score}  Level: {level}  Food Expires in: {time_left}s', True, white)
    screen.blit(score_surf, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()