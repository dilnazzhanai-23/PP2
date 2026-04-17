import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = os.listdir(music_folder)
        self.playlist = [track for track in self.playlist if track.endswith(".mp3")]

        self.current_index = 0
        self.is_playing = False

        pygame.mixer.init()

    def load_track(self):
        track_path = os.path.join(self.music_folder, self.playlist[self.current_index])
        pygame.mixer.music.load(track_path)

    def play(self):
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
        return self.playlist[self.current_index]