import pygame
import math

def draw_generic_shape(surface, shape_type, color, start, end, thickness):
    
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1

    if shape_type == 'rect':
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(dx), abs(dy))
        pygame.draw.rect(surface, color, rect, thickness)

    elif shape_type == 'circle':
        radius = int(math.sqrt(dx**2 + dy**2))
        pygame.draw.circle(surface, color, start, radius, thickness)

    elif shape_type == 'square':
        side = max(abs(dx), abs(dy))
        rect = pygame.Rect(x1 if x2 > x1 else x1 - side, y1 if y2 > y1 else y1 - side, side, side)
        pygame.draw.rect(surface, color, rect, thickness)

    elif shape_type == 'right_triangle':
        v = [start, end, (x1, y2)]
        pygame.draw.polygon(surface, color, v, thickness)

    elif shape_type == 'equilateral_triangle':
        height = int((math.sqrt(3) / 2) * dx)
        v = [start, (x2, y1), (x1 + dx // 2, y1 - height)]
        pygame.draw.polygon(surface, color, v, thickness)

    elif shape_type == 'rhombus':
        v = [(x1 + dx // 2, y1), (x2, y1 + dy // 2), (x1 + dx // 2, y2), (x1, y1 + dy // 2)]
        pygame.draw.polygon(surface, color, v, thickness)
        
    elif shape_type == 'straight_line':
        pygame.draw.line(surface, color, start, end, thickness)

def flood_fill(surface, start_pos, target_color, fill_color, points_list):
    
    width, height = surface.get_size()
    stack = [start_pos]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        
        if (x, y) in visited:
            continue
        visited.add((x, y))
        
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
            
        current_pixel = surface.get_at((x, y))[:3]
        if current_pixel == target_color:
            points_list.append(('pixel', fill_color, (x, y), 1))
            surface.set_at((x, y), fill_color)
            
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))
