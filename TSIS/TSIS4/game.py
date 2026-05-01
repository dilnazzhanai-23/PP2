import pygame
import random
import json
import os
import db


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)        
POISON_BLUE = (0, 0, 255)  
UI_BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 600, 400
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')
EAT_SOUND_PATH = os.path.join(BASE_DIR, 'assets', 'eating_apple.wav')

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Verdana", 20)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        curr_c = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, curr_c, self.rect, border_radius=5)
        txt = self.font.render(self.text, True, WHITE)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

class TextInput:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.font = pygame.font.SysFont("Verdana", 24)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif len(self.text) < 12 and event.unicode.isalnum(): self.text += event.unicode
            return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=5)
        txt = self.font.render(self.text, True, BLACK)
        surface.blit(txt, (self.rect.x + 10, self.rect.y + 5))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake: Hardcore Poison")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state = "MENU"
        self.settings = self.load_settings()
        
        try: self.eat_sound = pygame.mixer.Sound(EAT_SOUND_PATH)
        except: self.eat_sound = None

        self.username_input = TextInput(200, 100, 200, 40)
        self.init_ui()
        self.reset_game_vars()

    def load_settings(self):
        default = {"snake_color": [0, 255, 0], "grid": True, "sound": True}
        try:
            if os.path.exists(SETTINGS_PATH):
                with open(SETTINGS_PATH, 'r') as f:
                    data = json.load(f)
                    for k in default:
                        if k not in data: data[k] = default[k]
                    return data
            return default
        except: return default

    def init_ui(self):
        self.btn_play = Button(200, 160, 200, 40, "Play", UI_BLUE, (100, 200, 255))
        self.btn_leaderboard = Button(200, 210, 200, 40, "Leaderboard", UI_BLUE, (100, 200, 255))
        self.btn_quit = Button(200, 260, 200, 40, "Quit", RED, (150, 0, 0))
        self.btn_back = Button(200, 340, 200, 40, "Back to Menu", RED, (150, 0, 0))

    def reset_game_vars(self):
        self.snake_pos = [300, 200]
        self.snake_body = [[300, 200], [280, 200], [260, 200]]
        self.direction = 'RIGHT'
        self.change_to = 'RIGHT'
        self.score, self.level, self.speed = 0, 1, 7
        
        self.food_spawn = False
        self.food_lifetime = 5000
        self.food_timer_start = 0
        
        self.poison_active = False
        self.spawn_poison() 
        
        self.obstacles = []

    def spawn_food(self):
        while True:
            pos = [random.randrange(1, WIDTH//20)*20, random.randrange(1, HEIGHT//20)*20]
            if pos not in self.snake_body and pos not in self.obstacles:
                self.food_pos = pos
                break
        r = random.randint(1, 10)
        if r <= 7: self.food_weight, self.food_color = 1, RED
        elif r <= 9: self.food_weight, self.food_color = 3, ORANGE
        else: self.food_weight, self.food_color = 5, PURPLE
        self.food_timer_start = pygame.time.get_ticks()
        self.food_spawn = True

    def spawn_poison(self):
        while True:
            pos = [random.randrange(1, WIDTH//20)*20, random.randrange(1, HEIGHT//20)*20]
            # Убеждаемся, что яд не на змее и не на месте обычной еды
            if pos not in self.snake_body:
                if not hasattr(self, 'food_pos') or pos != self.food_pos:
                    self.poison_pos = pos
                    self.poison_active = True
                    break

    def update(self):
        now = pygame.time.get_ticks()
        self.direction = self.change_to
        if self.direction == 'UP': self.snake_pos[1] -= 20
        elif self.direction == 'DOWN': self.snake_pos[1] += 20
        elif self.direction == 'LEFT': self.snake_pos[0] -= 20
        elif self.direction == 'RIGHT': self.snake_pos[0] += 20

        self.snake_body.insert(0, list(self.snake_pos))

        if not self.food_spawn: self.spawn_food()
        if not self.poison_active: self.spawn_poison() 
        
        if now - self.food_timer_start > self.food_lifetime:
            self.food_spawn = False
            self.poison_active = False 

        if self.snake_pos == self.food_pos:
            if self.settings.get('sound') and self.eat_sound: self.eat_sound.play()
            self.score += self.food_weight
            self.food_spawn = False
            if self.score // 5 >= self.level:
                self.level += 1
                self.speed += 1
                if self.level >= 3:
                    self.obstacles.append([random.randrange(1, WIDTH//20)*20, random.randrange(1, HEIGHT//20)*20])
        else:
            self.snake_body.pop()

        if self.poison_active and self.snake_pos == self.poison_pos:

            if self.settings.get('sound') and self.eat_sound: self.eat_sound.play()
            
            self.poison_active = False
            if len(self.snake_body) > 2:
                self.snake_body.pop()
                self.snake_body.pop()
                if len(self.snake_body) <= 1:
                    self.trigger_game_over()
            else:
                self.trigger_game_over()

        if (self.snake_pos[0] < 0 or self.snake_pos[0] >= WIDTH or 
            self.snake_pos[1] < 0 or self.snake_pos[1] >= HEIGHT or 
            self.snake_pos in self.snake_body[1:] or self.snake_pos in self.obstacles):
            self.trigger_game_over()

    def trigger_game_over(self):
        db.save_game_session(self.player_name, self.score, self.level)
        self.state = "GAMEOVER"

    def draw(self):
        self.screen.fill(BLACK)
        now = pygame.time.get_ticks()

        if self.state == "GAME":
            if self.settings.get('grid'):
                for x in range(0, WIDTH, 20): pygame.draw.line(self.screen, (25, 25, 25), (x, 0), (x, HEIGHT))
                for y in range(0, HEIGHT, 20): pygame.draw.line(self.screen, (25, 25, 25), (0, y), (WIDTH, y))

            for b in self.snake_body:
                pygame.draw.rect(self.screen, self.settings['snake_color'], (b[0], b[1], 18, 18))
            
            if self.food_spawn:
                pygame.draw.rect(self.screen, self.food_color, (self.food_pos[0], self.food_pos[1], 20, 20))
            
            if self.poison_active:
                pygame.draw.rect(self.screen, POISON_BLUE, (self.poison_pos[0], self.poison_pos[1], 20, 20))

            for o in self.obstacles: pygame.draw.rect(self.screen, (80, 80, 80), (o[0], o[1], 20, 20))

            font = pygame.font.SysFont("Arial", 20, bold=True)
            info_txt = font.render(f"Score: {self.score}  Level: {self.level}", True, WHITE)
            self.screen.blit(info_txt, (10, 10))
            
            time_left = max(0, (self.food_lifetime - (now - self.food_timer_start)) // 1000)
            timer_txt = font.render(f"Food Timer: {time_left}s", True, YELLOW if time_left > 1 else RED)
            self.screen.blit(timer_txt, (WIDTH - 160, 10))

        elif self.state == "MENU":
            title = pygame.font.SysFont("Verdana", 30, bold=True).render("SNAKE GAME", True, GREEN)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
            self.username_input.draw(self.screen)
            self.btn_play.draw(self.screen)
            self.btn_leaderboard.draw(self.screen)
            self.btn_quit.draw(self.screen)

        elif self.state == "LEADERBOARD":
            leaders = db.get_leaderboard()
            for i, r in enumerate(leaders):
                t = pygame.font.SysFont("Arial", 18).render(f"{i+1}. {r[0]} - {r[1]} pts (Lvl {r[2]})", True, WHITE)
                self.screen.blit(t, (150, 60 + i*25))
            self.btn_back.draw(self.screen)

        elif self.state == "GAMEOVER":
            msg = pygame.font.SysFont("Verdana", 45, bold=True).render("GAME OVER", True, RED)
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 120))
            self.btn_back.draw(self.screen)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.is_running = False
            if self.state == "MENU":
                self.username_input.handle_event(event)
                if self.btn_play.is_clicked(event):
                    self.player_name = self.username_input.text or "Guest"
                    self.reset_game_vars()
                    self.state = "GAME"
                if self.btn_leaderboard.is_clicked(event): self.state = "LEADERBOARD"
                if self.btn_quit.is_clicked(event): self.is_running = False
            elif self.state == "GAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != 'DOWN': self.change_to = 'UP'
                    if event.key == pygame.K_DOWN and self.direction != 'UP': self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT and self.direction != 'RIGHT': self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT and self.direction != 'LEFT': self.change_to = 'RIGHT'
            elif self.state in ["GAMEOVER", "LEADERBOARD"]:
                if self.btn_back.is_clicked(event): self.state = "MENU"

    def run(self):
        while self.is_running:
            self.handle_events()
            if self.state == "GAME": self.update()
            self.draw()
            self.clock.tick(self.speed if self.state == "GAME" else 30)

if __name__ == "__main__":
    pygame.init()
    db.init_db()
    Game().run()