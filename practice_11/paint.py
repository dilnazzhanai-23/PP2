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
# Modes: pencil, rect, circle, eraser, square, right_tri, eq_tri, rhombus
mode = "pencil"  

startX, startY = 0, 0
currX, currY = 0, 0
prevX, prevY = 0, 0

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def get_square_rect(x1, y1, x2, y2):
    side = max(abs(x2 - x1), abs(y2 - y1))
    new_x = x1 if x2 > x1 else x1 - side
    new_y = y1 if y2 > y1 else y1 - side
    return pygame.Rect(new_x, new_y, side, side)

def get_right_tri_pts(x1, y1, x2, y2):
    return [(x1, y1), (x1, y2), (x2, y2)]

def get_eq_tri_pts(x1, y1, x2, y2):
    side = x2 - x1
    height = (math.sqrt(3) / 2) * side
    # Drawing from top-center, bottom-left, bottom-right
    return [(x1 + side/2, y1), (x1, y1 + height), (x1 + side, y1 + height)]

def get_rhombus_pts(x1, y1, x2, y2):
    mid_x = x1 + (x2 - x1) / 2
    mid_y = y1 + (y2 - y1) / 2
    return [(mid_x, y1), (x1, mid_y), (mid_x, y2), (x2, mid_y)]

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            startX, startY = event.pos
            prevX, prevY = event.pos
            currX, currY = event.pos

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos
                
                if mode == "pencil":
                    pygame.draw.line(base_layer, current_color, (prevX, prevY), (currX, currY), THICKNESS)
                    prevX, prevY = currX, currY
                
                elif mode == "eraser":
                    pygame.draw.circle(base_layer, BLACK, (currX, currY), THICKNESS * 2)

                elif mode in ["rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]:
                    screen.blit(base_layer, (0, 0))
                    if mode == "rect":
                        pygame.draw.rect(screen, current_color, calculate_rect(startX, startY, currX, currY), THICKNESS)
                    elif mode == "square":
                        pygame.draw.rect(screen, current_color, get_square_rect(startX, startY, currX, currY), THICKNESS)
                    elif mode == "circle":
                        radius = int(math.hypot(currX - startX, currY - startY))
                        pygame.draw.circle(screen, current_color, (startX, startY), radius, THICKNESS)
                    elif mode == "right_tri":
                        pygame.draw.polygon(screen, current_color, get_right_tri_pts(startX, startY, currX, currY), THICKNESS)
                    elif mode == "eq_tri":
                        pygame.draw.polygon(screen, current_color, get_eq_tri_pts(startX, startY, currX, currY), THICKNESS)
                    elif mode == "rhombus":
                        pygame.draw.polygon(screen, current_color, get_rhombus_pts(startX, startY, currX, currY), THICKNESS)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            if mode == "rect":
                pygame.draw.rect(base_layer, current_color, calculate_rect(startX, startY, currX, currY), THICKNESS)
            elif mode == "square":
                pygame.draw.rect(base_layer, current_color, get_square_rect(startX, startY, currX, currY), THICKNESS)
            elif mode == "circle":
                radius = int(math.hypot(currX - startX, currY - startY))
                pygame.draw.circle(base_layer, current_color, (startX, startY), radius, THICKNESS)
            elif mode == "right_tri":
                pygame.draw.polygon(base_layer, current_color, get_right_tri_pts(startX, startY, currX, currY), THICKNESS)
            elif mode == "eq_tri":
                pygame.draw.polygon(base_layer, current_color, get_eq_tri_pts(startX, startY, currX, currY), THICKNESS)
            elif mode == "rhombus":
                pygame.draw.polygon(base_layer, current_color, get_rhombus_pts(startX, startY, currX, currY), THICKNESS)

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
            if event.key == pygame.K_5: mode = "square"
            if event.key == pygame.K_6: mode = "right_tri"
            if event.key == pygame.K_7: mode = "eq_tri"
            if event.key == pygame.K_8: mode = "rhombus"
            
            # Actions
            if event.key == pygame.K_EQUALS: THICKNESS += 1
            if event.key == pygame.K_MINUS:  THICKNESS = max(1, THICKNESS - 1)
            if event.key == pygame.K_c:
                base_layer.fill(BLACK)

    # Rendering
    if not (LMBpressed and mode in ["rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]):
        screen.blit(base_layer, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()