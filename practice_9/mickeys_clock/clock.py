import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, base_path):
       
        self.clock_img = pygame.image.load(os.path.join(base_path, 'clock.png')).convert_alpha()
        self.mickey = pygame.image.load(os.path.join(base_path, 'mickey.png')).convert_alpha()
        self.hand_l = pygame.image.load(os.path.join(base_path, 'hand_left.png')).convert_alpha()
        self.hand_r = pygame.image.load(os.path.join(base_path, 'hand_right.png')).convert_alpha()

        self.clock_img = pygame.transform.scale(self.clock_img, (1100, 800))
        self.mickey = pygame.transform.scale(self.mickey, (500, 400))

        self.hand_l_base = pygame.transform.scale(self.hand_l, (150, 250)) 
        self.hand_r_base = pygame.transform.scale(self.hand_r, (150, 250)) 

        self.center = (350, 350)
    
    def get_angles(self):
        now = datetime.datetime.now()
        m = now.minute
        s = now.second

        seconds_angle = -(s * 6)
        minutes_angle = -(m * 6 + s * 0.1)

        return seconds_angle, minutes_angle

    def draw(self, screen):
        
        clock_rect = self.clock_img.get_rect(center=self.center)
        screen.blit(self.clock_img, clock_rect)

        mic_rect = self.mickey.get_rect(center=(self.center[0], self.center[1] -5)) 
        screen.blit(self.mickey, mic_rect)

        seconds_angle, minutes_angle = self.get_angles()

        self.blit_rotated_hand(screen, self.hand_l_base, self.center, seconds_angle)
        self.blit_rotated_hand(screen, self.hand_r_base, self.center, minutes_angle)

    def blit_rotated_hand(self, screen, image, pivot, angle):
        offset = pygame.math.Vector2(0, -image.get_height() /3)
        rotated_offset = offset.rotate(-angle)
        rotated_image = pygame.transform.rotate(image, angle)
        rect = rotated_image.get_rect(center=pivot + rotated_offset)
        
        screen.blit(rotated_image, rect)