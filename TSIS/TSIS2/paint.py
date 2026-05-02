import pygame
import sys
from datetime import datetime
from tools import draw_generic_shape, flood_fill

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Pygame Paint")
    clock = pygame.time.Clock()
    
    current_color = (255, 0, 0) 
    mode = 'pen' 
    brush_size = 3
    
    points = [] 
    drawing = False
    start_pos = None
    last_pos = None 

    text_active = False
    text_pos = (0, 0)
    text_buffer = ""
    font = pygame.font.SysFont(None, 24)

    while True:
        screen.fill((0, 0, 0))
        
        
        for shape_type, color, data, thick in points:
            if shape_type == 'line':
                
                pygame.draw.line(screen, color, data[0], data[1], thick)
            elif shape_type == 'pixel':
                screen.set_at(data, color)
            elif shape_type == 'text':
                text_surf = font.render(data, True, color)
                screen.blit(text_surf, thick)
            else:
                draw_generic_shape(screen, shape_type, color, data[0], data[1], thick)

        
        if drawing and mode not in ['pen', 'eraser', 'fill', 'text']:
            draw_generic_shape(screen, mode, current_color, start_pos, pygame.mouse.get_pos(), brush_size)

        
        if text_active:
            text_surf = font.render(text_buffer + "|", True, current_color)
            screen.blit(text_surf, text_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            
            if text_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    points.append(('text', current_color, text_buffer, text_pos))
                    text_active = False
                    text_buffer = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    if event.unicode.isprintable():
                        text_buffer += event.unicode
                continue 
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_r: current_color = (255, 0, 0)
                if event.key == pygame.K_g: current_color = (0, 255, 0)
                if event.key == pygame.K_b: current_color = (0, 0, 255)
                if event.key == pygame.K_w: current_color = (255, 255, 255)
                
                
                if event.key == pygame.K_4: mode = 'right_triangle'
                if event.key == pygame.K_5: mode = 'equilateral_triangle'
                if event.key == pygame.K_6: mode = 'rhombus'
                if event.key == pygame.K_7: mode = 'eraser'
                if event.key == pygame.K_8: mode = 'circle'
                if event.key == pygame.K_9: mode = 'rect'
                if event.key == pygame.K_0: mode = 'square'
                
                
                if event.key == pygame.K_p: mode = 'pen'
                if event.key == pygame.K_l: mode = 'straight_line'
                if event.key == pygame.K_f: mode = 'fill'
                if event.key == pygame.K_t: mode = 'text'

            
                if event.key == pygame.K_1: brush_size = 2
                if event.key == pygame.K_2: brush_size = 5
                if event.key == pygame.K_3: brush_size = 10

                
                if event.key == pygame.K_s and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"canvas_{timestamp}.png"
                    pygame.image.save(screen, filename)
                    print(f"Canvas saved as {filename}")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 'text':
                    text_active = True
                    text_pos = event.pos
                    text_buffer = ""
                elif mode == 'fill':
                    target_color = screen.get_at(event.pos)[:3]
                    if target_color != current_color:
                        flood_fill(screen, event.pos, target_color, current_color, points)
                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos 

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and mode not in ['pen', 'eraser', 'fill', 'text']:
                    points.append((mode, current_color, (start_pos, event.pos), brush_size))
                drawing = False
                last_pos = None 

            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'pen' or mode == 'eraser':
                    color = (0, 0, 0) if mode == 'eraser' else current_color
                    thick = 20 if mode == 'eraser' else brush_size
                    
                    points.append(('line', color, (last_pos, event.pos), thick))
                    last_pos = event.pos 

        pygame.display.flip()
        clock.tick(60)

main()