import pygame
from load_image import load_image


class Button:
    def __init__(self, left, top, w, h):
        self.left = left
        self.top = top
        self.weight = w
        self.height = h

    def draw_btn_and_txt(self, text, screen, background, size=False):
        self.text = text
        if background:
            pygame.draw.rect(screen, "blue", (self.left, self.top, self.weight, self.height), width=3)
        else:
            pygame.draw.rect(screen, "white", (self.left, self.top, self.weight, self.height), width=3)

        if not size:
            font = pygame.font.Font(None, self.weight // (len(text) // 2))
        else:
            font = pygame.font.Font(None, size)

        text = font.render(f"{text}", 1, (255, 255, 255) if not background else "blue")
        screen.blit(text, (self.left + self.weight // 2 - text.get_width() // 2, self.top + self.height // 2 - text.get_height() // 2))

    def draw_btn_with_image(self, screen, image_name):
        self.text = image_name
        image = load_image(image_name, colorkey="white")
        image = pygame.transform.scale(image, (self.weight, self.height))
        screen.blit(image, (self.left, self.top))

    def check_position(self, x, y):
        flag = self.left < x < self.left + self.weight and self.top < y < self.top + self.height
        return flag

    def get_text(self):
        return self.text


class Scroll_btns:
    def __init__(self, lst_of_txt):
        self.texts = lst_of_txt
        self.left, self.weight, self.top, self.height = -1, -1, -1, -1
        self.text = ""

    def draw_btn_choice(self, screen, x, y, w, h, size):
        font = pygame.font.Font(None, size)
        for i in range(len(self.texts)):
            pygame.draw.rect(screen, (255, 255, 255), (x, y + h * i, w, h), width=2)
            self.left, self.weight, self.top, self.height = x, w, y, h
            text = font.render(self.texts[i], 1, (255, 255, 255))
            screen.blit(text, (x, y + h * i))

    def check_position(self, x, y):
        flag = self.left < x < self.left + self.weight and self.top < y < self.top + self.height
        return flag
    def get_text(self):
        return self.text
