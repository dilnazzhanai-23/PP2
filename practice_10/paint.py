import pygame
import math

# Initialization
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Paint Pro")
clock = pygame.time.Clock()

# Layers
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill("black")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# State Variables
running = True
LMBpressed = False
THICKNESS = 3
current_color = RED
mode = "pencil"  # pencil, rect, circle, eraser

startX, startY = 0, 0
currX, currY = 0, 0
prevX, prevY = 0, 0

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse Down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            startX, startY = event.pos
            prevX, prevY = event.pos
            currX, currY = event.pos

        # Mouse Motion 
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos
                
                if mode == "pencil":
                    pygame.draw.line(base_layer, current_color, (prevX, prevY), (currX, currY), THICKNESS)
                    prevX, prevY = currX, currY
                
                elif mode == "eraser":
                    pygame.draw.circle(base_layer, BLACK, (currX, currY), THICKNESS * 2)

                elif mode in ["rect", "circle"]:
                    # Live Preview logic: show base layer then draw shape on top
                    screen.blit(base_layer, (0, 0))
                    if mode == "rect":
                        pygame.draw.rect(screen, current_color, calculate_rect(startX, startY, currX, currY), THICKNESS)
                    elif mode == "circle":
                        radius = int(math.hypot(currX - startX, currY - startY))
                        pygame.draw.circle(screen, current_color, (startX, startY), radius, THICKNESS)

        # Mouse Up (Commit Shapes)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            if mode == "rect":
                pygame.draw.rect(base_layer, current_color, calculate_rect(startX, startY, currX, currY), THICKNESS)
            elif mode == "circle":
                radius = int(math.hypot(currX - startX, currY - startY))
                pygame.draw.circle(base_layer, current_color, (startX, startY), radius, THICKNESS)

        # Keyboard Events
        if event.type == pygame.KEYDOWN:
            # Color Selection
            if event.key == pygame.K_r: current_color = RED
            if event.key == pygame.K_g: current_color = GREEN
            if event.key == pygame.K_b: current_color = BLUE
            if event.key == pygame.K_w: current_color = WHITE
            
            # Tool Selection
            if event.key == pygame.K_1: mode = "pencil"
            if event.key == pygame.K_2: mode = "rect"
            if event.key == pygame.K_3: mode = "circle"
            if event.key == pygame.K_4: mode = "eraser"
            
            # Actions
            if event.key == pygame.K_EQUALS: THICKNESS += 1
            if event.key == pygame.K_MINUS:  THICKNESS = max(1, THICKNESS - 1)
            if event.key == pygame.K_c:
                base_layer.fill(BLACK)

    # Rendering
    
    if not (LMBpressed and mode in ["rect", "circle"]):
        screen.blit(base_layer, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()