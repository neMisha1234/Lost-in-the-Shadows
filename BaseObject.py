import pygame


class BaseObject(pygame.sprite.Sprite):
    def __init__(self, group, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.surface.Surface((w, h))
        self.image.fill(color)
        super().__init__(group)
        pygame.draw.rect(self.image, color, (x, y, w, h))