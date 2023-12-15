import pygame


class Button:
    def __init__(self, left, top, w, h, mode, screen):
        self.left = left
        self.top = top
        self.weight = w
        self.height = h
        self.screen = screen
        self.mode = mode

    def draw_btn_and_txt(self, text):
        pygame.draw.rect(self.screen, "white", (self.left, self.top, self.weight, self.height), width=1)
        font = pygame.font.Font(None, self.weight // (len(text) // 2))
        text = font.render(f"{text}", 1, (255, 255, 255))
        self.screen.blit(text, (self.left + self.weight // 2 - text.get_width() // 2, self.top + self.height // 2 - text.get_height() // 2))

    def check_position(self, x, y):
        return self.left < x < self.left + self.weight and self.top < y < self.top + self.height

    def get_mode(self):
        return self.mode
