import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]
        self.current_index = 0
        self.is_playing = False
        self.track_length = 0 

        pygame.mixer.init()

    def load_track(self):
        track_path = os.path.join(self.music_folder, self.playlist[self.current_index])
        pygame.mixer.music.load(track_path)
        
        temp_sound = pygame.mixer.Sound(track_path)
        self.track_length = temp_sound.get_length()

    def play(self):
        if self.playlist:
            self.load_track()
            pygame.mixer.music.play()
            self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track(self):
        return self.playlist[self.current_index] if self.playlist else "No Tracks"

    def get_progress(self):
        if not self.is_playing:
            return 0, self.track_length, 0
        
        current_pos = pygame.mixer.music.get_pos() / 1000.0
        if self.track_length > 0:
            ratio = current_pos / self.track_length
            return current_pos, self.track_length, min(ratio, 1.0)
        return 0, 0, 0