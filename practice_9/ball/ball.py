import pygame
class Ball:
    def __init__(self,x,y,radius,s):
        self.x=x 
        self.y=y
        self.radius=radius
        self.s=s
        self.color=((255, 0, 0))

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y), self.radius)

    def move(self, keys, w, h):
        if keys[pygame.K_UP] and self.y - self.s >= self.radius:
            self.y -= self.s
        if keys[pygame.K_DOWN] and self.y + self.s<= h - self.radius :
            self.y += self.s
        if keys[pygame.K_LEFT] and self.x - self.s >= self.radius:
            self.x -= self.s
        if keys[pygame.K_RIGHT] and self.x +  self.s<= w - self.radius :
            self.x += self.s