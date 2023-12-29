import pygame


class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, group, x, y, fps, w, h):
        super().__init__(group)
        self.image = pygame.surface.Surface((25, 50))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.vx, self.vy = 150, 100
        self.w, self.h = w, h
        self.isFall = True
        self.fall_vector = 0
        self.fps = fps
        self.flag = False
        self.climb = [False, False]
        self.climb_counter = 200
        self.floor = h

    def jump_and_fall(self):
        self.rect.y -= self.fall_vector * self.vy / self.fps
        self.flag = False
        self.fall_vector -= 1

    def update(self, objects):
        last_x = self.rect.x
        last_y = self.rect.y
        w = 0
        s = 0

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a]) and (self.rect.x >= 0):
            if keys[pygame.K_CAPSLOCK]:
                self.rect.x -= self.vx * 1.5 / self.fps
            else:
                self.rect.x -= self.vx / self.fps

        if (keys[pygame.K_w]) and self.climb:
            w = self.vy / self.fps

        if (keys[pygame.K_s]) and self.climb:
            s = self.vy / self.fps

        if (keys[pygame.K_d]) and (self.rect.x <= self.w):
            if keys[pygame.K_CAPSLOCK]:
                self.rect.x += self.vx * 1.5 / self.fps
            else:
                self.rect.x += self.vx / self.fps

        if keys[pygame.K_SPACE]:
            if self.flag:
                self.fall_vector = 10
                self.jump_from_climb = False

        self.jump_and_fall()
        temp = pygame.sprite.spritecollide(self, objects, False)

        for obj in temp:
            conx1 = obj.rect.x + obj.rect.x + obj.rect.w > self.rect.x > obj.rect.x
            conx2 = obj.rect.x + obj.rect.x > self.rect.x + self.rect.w > obj.rect.x - obj.rect.w
            cony_up = obj.rect.y < self.rect.y + self.rect.h < obj.rect.h + obj.rect.y
            cony_down = obj.rect.y < self.rect.y < obj.rect.h + obj.rect.y
            if conx1 or conx2:
                self.rect.x = last_x
                self.climb[1] = True
            if self.climb[0] and self.climb[1] and not (cony_down and last_y > obj.rect.y + obj.rect.h):
                self.flag = True
                if self.floor < last_y - w + s:
                    self.rect.y = last_y - w
                else:
                    self.rect.y  = last_y - w + s
            if cony_down and last_y > obj.rect.y + obj.rect.h:
                self.rect.y = obj.rect.y + obj.rect.h
                self.fall_vector = 0
            if cony_up and last_y + self.rect.h <= obj.rect.y:
                self.floor = obj.rect.y - self.rect.h
                self.rect.y = obj.rect.y - self.rect.h
                self.fall_vector = 0
                self.flag = True
