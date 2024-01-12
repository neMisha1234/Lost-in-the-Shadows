import datetime
import pygame
from load_image import load_image


class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, group, x, y, fps, w, h, all_sprites):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("Player.png", colorkey=(255, 255, 255)), (20, 50))
        self.rect = self.image.get_rect()
        self.im_left = pygame.transform.flip(self.image, True, False)
        self.im_right = self.image.convert()
        self.rect.midbottom = (x, y)
        self.vx, self.vy = 150, 50
        self.all_sprites = all_sprites
        self.w, self.h = w, h
        self.isFall = True
        self.onfloor = False

        time = datetime.datetime.now().time()
        self.time_to_get_damage = datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        self.damage_resist = 20

        self.fall_vector = 0
        self.fps = fps

        self.flag = False
        self.climb = False
        self.push_cnt = 25
        self.push = False
        self.left = self.right = False
        self.near_wall = False

        self.hp = 100

    def jump_and_fall(self, enemys):
        last_x = self.rect.x
        last_y = self.rect.y

        if self.push:
            self.rect.x += 150 / self.fps * self.push
            if pygame.sprite.spritecollide(self, self.all_sprites, False):
                self.rect.x = last_x
            self.push_cnt -= 1
            if self.push_cnt == 0:
                self.push_cnt = 25
                self.push = False
        self.rect.y -= self.fall_vector * self.vy / self.fps
        temp = pygame.sprite.spritecollide(self, self.all_sprites, False)
        if temp:
            for en in pygame.sprite.spritecollide(self, enemys, False):
                time = datetime.datetime.now().time()
                if datetime.timedelta(hours=time.hour, minutes=time.minute,
                                      seconds=time.second) >= self.time_to_get_damage + en.attack_speed:
                    if en.rect.x + en.rect.w < self.rect.x:
                        self.push = 1
                    else:
                        self.push = -1
                    self.fall_vector = 3
                    self.time_to_get_damage = datetime.timedelta(hours=time.hour, minutes=time.minute,
                                                                 seconds=time.second)
            if last_y < self.rect.y:
                self.rect.y = last_y
                self.fall_vector = 0
                self.flag = True
                self.onfloor = True
            elif last_y > self.rect.y:
                self.rect.y = last_y
                self.fall_vector = 0
                self.flag = False
        else:
            self.flag = False
            self.fall_vector -= 1
            self.onfloor = False

    def check_hp(self):
        if self.hp <= 0:
            self.kill()

    def get_damage(self, d):
        self.hp -= d * ((100 - self.damage_resist) / 100)

    def update(self, objects, enemys):
        last_x = self.rect.x
        last_y = self.rect.y
        w = 0
        s = 0
        if self.left:
            self.image = self.im_left
        else:
            self.image = self.im_right

        for en in enemys:
            if self.rect.colliderect(en.rect):
                time = datetime.datetime.now().time()
                if datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second) >= self.time_to_get_damage + en.attack_speed:
                    self.get_damage(en.damage)
                    print(en.rect.x + en.rect.w, self.rect.x)
                    if en.rect.x + en.rect.w >= self.rect.x >  en.rect.x:
                        self.push = 1
                    else:
                        self.push = -1
                    self.fall_vector = 3
                    self.time_to_get_damage = datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
            self.check_hp()

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a]) and (self.rect.x >= 0):
            if keys[pygame.K_CAPSLOCK]:
                self.rect.x -= self.vx * 1.5 / self.fps
            else:
                self.rect.x -= self.vx / self.fps
            self.left = True
        if (keys[pygame.K_w]) and self.climb:
            w = self.vy / self.fps

        if (keys[pygame.K_s]) and self.climb:
            s = self.vy / self.fps

        if (keys[pygame.K_d]) and (self.rect.x <= self.w):
            self.left = False
            if keys[pygame.K_CAPSLOCK]:
                self.rect.x += self.vx * 1.5 / self.fps
            else:
                self.rect.x += self.vx / self.fps
        if pygame.sprite.spritecollide(self, self.all_sprites, False):
            self.rect.x = last_x
            self.near_wall = True
        else:
            self.near_wall = False

        if keys[pygame.K_SPACE]:
            if self.flag:
                self.flag = False
                self.fall_vector = 12
        self.jump_and_fall(enemys)

        if self.climb and self.near_wall:
            self.rect.x = last_x
            self.fall_vector = 0
            if self.onfloor:
                self.rect.y -= w
            else:
                self.rect.y -= w - s
            if pygame.sprite.spritecollide(self, self.all_sprites, False):
                self.rect.y = last_y
