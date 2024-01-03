import datetime as dt

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y, fps, w, h):
        super().__init__(group)
        self.image = pygame.surface.Surface((25, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.playerx = None
        self.playerw = 25
        self.agr_range = 200
        self.rect.midbottom = (x, y)
        self.vx, self.vy = 50, 100
        self.w, self.h = w, h
        self.damage = 25
        self.fall_vector = 0
        self.fps = fps
        self.attack_speed = dt.timedelta(seconds=1.7)

    def set_player(self, playerx):
        if self.rect.x + self.rect.h + self.agr_range > playerx > self.rect.x - self.agr_range:
            self.playerx = playerx
        else:
            self.playerx = None

    def jump_and_fall(self):
        self.rect.y -= self.fall_vector * self.vy / self.fps
        self.fall_vector -= 1

    def update(self, objects, player):
        last_x = self.rect.x
        last_y = self.rect.y
        self.jump_and_fall()

        if self.playerx != None:
            if self.playerx + self.playerw <= self.rect.x:
                self.rect.x -= self.vx / self.fps
            elif self.playerx >= self.rect.x + self.rect.w:
                self.rect.x += self.vx / self.fps

        temp = pygame.sprite.spritecollide(self, objects, False)

        for obj in temp:
            conx1 = obj.rect.x + obj.rect.x + obj.rect.w > self.rect.x > obj.rect.x
            conx2 = obj.rect.x + obj.rect.x > self.rect.x + self.rect.w > obj.rect.x - obj.rect.w
            cony_up = obj.rect.y < self.rect.y + self.rect.h < obj.rect.h + obj.rect.y
            cony_down = obj.rect.y < self.rect.y < obj.rect.h + obj.rect.y
            if conx1 or conx2:
                self.rect.x = last_x
            if cony_down and last_y > obj.rect.y + obj.rect.h:
                self.rect.y = obj.rect.y + obj.rect.h
                self.fall_vector = 0
            if cony_up and last_y + self.rect.h <= obj.rect.y:
                self.floor = obj.rect.y - self.rect.h
                self.rect.y = obj.rect.y - self.rect.h
                self.fall_vector = 0
