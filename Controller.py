import pygame


class Controller:
    def set_current_window(self, window):
        self.current_window = window

    def open_window(self, screen):
        self.current_window.start(screen)

    def window_event(self, event):
        return self.current_window.check_event(event)
