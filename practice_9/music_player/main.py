import pygame
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 120, 255)

font = pygame.font.Font(None, 28)
player = MusicPlayer("music")

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    curr_time, total_time, progress_ratio = player.get_progress()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SONG_END:
            player.next_track()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: player.play()
            elif event.key == pygame.K_s: player.stop()
            elif event.key == pygame.K_n: player.next_track()
            elif event.key == pygame.K_b: player.prev_track()
            elif event.key == pygame.K_q: running = False

    track_name = player.get_current_track()
    text = font.render(f"Track: {track_name}", True, BLACK)
    screen.blit(text, (20, 100))

    bar_x, bar_y = 50, 200
    bar_width, bar_height = 300, 10
    
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    
    pygame.draw.rect(screen, BLUE, (bar_x, bar_y, bar_width * progress_ratio, bar_height))

    time_str = f"{format_time(curr_time)} / {format_time(total_time)}"
    time_text = font.render(time_str, True, BLACK)
    screen.blit(time_text, (bar_x, bar_y + 20))

    hint = font.render("P: Play | S: Stop | N: Next | B: Back", True, (100, 100, 100))
    screen.blit(hint, (40, 350))

    pygame.display.update()
    clock.tick(60)

pygame.quit()