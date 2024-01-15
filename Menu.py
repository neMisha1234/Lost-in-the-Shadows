import pygame
from Button import Button
from load_image import load_image
from Game import Game
from Game_over import Game_Over


class Menu:
    def __init__(self, w, h, cntrl):
        pygame.init()
        self.start_image = load_image("screen.jpg")
        self.w = w
        self.h = h
        self.btns = []
        self.btn_names = [" Начать игру ", "  Настройки  ", "Выйти из игры"]
        self.controller = cntrl
        self.go = Game_Over(w, h, cntrl, self)
        self.game = Game(cntrl, self, self.go)

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
                    if btn.get_text().strip() == "Настройки":
                        pass
                    if btn.get_text().strip() == "Начать игру":
                        self.controller.set_current_window(self.game)



    def start(self, screen):
        screen.fill((0, 0, 0))
        self.btns = []
        for i in range(3):
            self.create_button(25, 50 + 150 * i, self.btn_names[i], screen)

        screen.blit(self.start_image, (self.w // 1.8, 0))


