import pygame
import math
from tools import *

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
COLORS = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0)}
current_color = COLORS["red"]

# State Variables
running = True
LMBpressed = False
THICKNESS = 5  # Default Medium
mode = "pencil"

startX, startY = 0, 0
currX, currY = 0, 0
prevX, prevY = 0, 0

# Text Tool Variables
font = pygame.font.SysFont("Arial", 24)
text_buffer = ""
text_pos = (0, 0)
typing = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # TEXT TOOL LOGIC
        if typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Commit text to base layer
                    text_surf = font.render(text_buffer, True, current_color)
                    base_layer.blit(text_surf, text_pos)
                    text_buffer = ""
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    text_buffer = ""
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
            elif event.type == pygame.TEXTINPUT:
                text_buffer += event.text
            continue # Skip other inputs while typing

        # MOUSE EVENTS
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            startX, startY = event.pos
            prevX, prevY = event.pos
            
            if mode == "fill":
                flood_fill(base_layer, startX, startY, current_color)
            elif mode == "text":
                typing = True
                text_pos = (startX, startY)

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos
                if mode == "pencil":
                    pygame.draw.line(base_layer, current_color, (prevX, prevY), (currX, currY), THICKNESS)
                    prevX, prevY = currX, currY
                elif mode == "eraser":
                    pygame.draw.circle(base_layer, COLORS["black"], (currX, currY), THICKNESS * 2)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            # Finalize shapes on base_layer
            if mode == "line":
                pygame.draw.line(base_layer, current_color, (startX, startY), (currX, currY), THICKNESS)
            elif mode == "rect":
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

        # KEYBOARD SHORTCUTS
        if event.type == pygame.KEYDOWN:
            # Ctrl+S to Save
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(base_layer)
            
            # Color Selection
            if event.key == pygame.K_r: current_color = COLORS["red"]
            if event.key == pygame.K_g: current_color = COLORS["green"]
            if event.key == pygame.K_b: current_color = COLORS["blue"]
            
            # Tool Selection
            tools = {pygame.K_p: "pencil", pygame.K_l: "line", pygame.K_f: "fill", pygame.K_t: "text", 
                     pygame.K_e: "eraser", pygame.K_r: "rect", pygame.K_c: "circle"}
            if event.key in tools: mode = tools[event.key]
            
            # Thickness Selection
            if event.key == pygame.K_1: THICKNESS = 2   # Small
            if event.key == pygame.K_2: THICKNESS = 5   # Medium
            if event.key == pygame.K_3: THICKNESS = 10  # Large

    # RENDERING
    screen.blit(base_layer, (0, 0))

    # Live Previews
    if LMBpressed:
        if mode == "line":
            pygame.draw.line(screen, current_color, (startX, startY), pygame.mouse.get_pos(), THICKNESS)
        elif mode == "rect":
            pygame.draw.rect(screen, current_color, calculate_rect(startX, startY, *pygame.mouse.get_pos()), THICKNESS)


    if typing:
        preview_text = font.render(text_buffer + "|", True, current_color)
        screen.blit(preview_text, text_pos)

    # UI Overlay
    info = font.render(f"Mode: {mode} | Size: {THICKNESS} | Color: {current_color}", True, "gray")
    screen.blit(info, (10, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()