import pygame
from Button import Button
from load_image import load_image
from Game import Game


class Game_Over:
    def __init__(self, w, h, cntrl, mn):
        pygame.init()
        self.start_image = load_image("Game_Over.png")
        self.w = w
        self.h = h
        self.btns = []
        self.btn_names = ["Начать с последней точки", "Вернуться в главное меню", "     Выйти из игры     "]
        self.controller = cntrl
        self.game = Game(cntrl, mn, self)
        self.menu = mn
        self.menu.game = self.game

    def create_button(self, x, y, text, screen):
        btn = Button(x, y, 500, 100)
        btn.draw_btn_and_txt(text, screen)
        self.btns.append(btn)

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.btns:
                if btn.check_position(*pygame.mouse.get_pos()):
                    if btn.get_text().strip() == "Выйти из игры":
                        return True
                    if btn.get_text().strip() == "Вернуться в главное меню":
                        self.controller.set_current_window(self.menu)
                    if btn.get_text().strip() == "Начать с последней точки":
                        self.controller.set_current_window(self.game)

    def start(self, screen):
        screen.fill((0, 0, 0))
        self.btns = []
        for i in range(3):
            self.create_button(self.w // 2 - self.start_image.get_rect().w // 2 - 70, 100 + 100 * i, self.btn_names[i], screen)

        screen.blit(self.start_image, (self.w // 2 - self.start_image.get_rect().w // 2, 0))
