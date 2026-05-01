import pygame
import math
from datetime import datetime

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
    return [(x1 + side/2, y1), (x1, y1 + height), (x1 + side, y1 + height)]

def get_rhombus_pts(x1, y1, x2, y2):
    mid_x = x1 + (x2 - x1) / 2
    mid_y = y1 + (y2 - y1) / 2
    return [(mid_x, y1), (x1, mid_y), (mid_x, y2), (x2, mid_y)]

def save_canvas(surface):
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pygame.image.save(surface, filename)
    print(f"Saved as {filename}")

def flood_fill(surface, x, y, new_color):
    """Stack-based flood fill to avoid recursion limits."""
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]
    while stack:
        curr_x, curr_y = stack.pop()
        if surface.get_at((curr_x, curr_y)) != target_color:
            continue

        surface.set_at((curr_x, curr_y), new_color)

        if curr_x + 1 < width: stack.append((curr_x + 1, curr_y))
        if curr_x - 1 >= 0: stack.append((curr_x - 1, curr_y))
        if curr_y + 1 < height: stack.append((curr_x, curr_y + 1))
        if curr_y - 1 >= 0: stack.append((curr_x, curr_y - 1))