import pygame


class HpBar:
    def __init__(self, x, y, hp):
        self.image1 = pygame.surface.Surface((200, 25))
        self.image1.fill((25, 0, 0))
        self.image2 = pygame.surface.Surface((200, 25))
        self.image2.fill((255, 0, 0))
        self.x = x
        self.y = y
        self.w1, self.h, self.w2 = 200, 25, 200
        self.k = hp / 100

    def update(self, hp):
        k = hp / 100
        w2 = k * self.w2
        if hp > 0:
            self.image2 = pygame.surface.Surface((w2, self.h))
            self.image2.fill((255, 0, 0))

    def draw(self, screen):
        screen.blit(self.image1, (self.x, self.y))
        screen.blit(self.image2, (self.x, self.y))