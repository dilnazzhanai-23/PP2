import pygame
import db
from game import Game

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init() # Инициализация модуля звука
    db.init_db()        # Создание таблиц БД, если их нет
    
    # Запускаем игру
    game_app = Game()
    game_app.run()