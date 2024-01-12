import pygame
from Button import Button
from load_image import load_image


class Menu:
    def __init__(self, w, h):
        pygame.init()
        self.start_image = load_image("screen.jpg")
        self.w = w
        self.h = h
        self.btn_names = [" Начать игру ", "  Настройки  ", "Выйти из игры"]

    def create_button(self, x, y, text, screen):
        btn = Button(x, y, 500, 100)
        btn.draw_btn_and_txt(text, screen)

    def start(self, screen):
        screen.fill((0, 0, 0))
        for i in range(3):
            self.create_button(25, 50 + 150 * i, self.btn_names[i], screen)
        screen.blit(self.start_image, (self.w // 1.8, 0))



