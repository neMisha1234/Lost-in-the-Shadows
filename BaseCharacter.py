import datetime as dt
import pygame
from load_image import load_image
import sqlite3
from Items import items_function
from Atack import Attack


class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, group, x, y, fps, w, h, all_sprites):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("Player.png", colorkey="white"), (20, 50))
        self.rect = self.image.get_rect()
        self.im_left = pygame.transform.flip(self.image, True, False)
        self.im_right = self.image.convert()
        self.rect.midbottom = (x, y)
        self.vx, self.vy = 150, 50
        self.all_sprites = all_sprites
        self.w, self.h = w, h
        self.isFall = True
        self.onfloor = False
        self.energy = 100
        self.energy_v = 15
        self.kills = 0
        self.damage = 25
        self.mw = False
        self.is_attack = False
        self.total_damage = 0
        self.total_damage_block = 0

        time = dt.datetime.now().time()
        self.time_to_get_damage = dt.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
        self.damage_resist = 0

        self.fall_vector = 0
        self.fps = fps
        self.items = []

        self.flag = False
        self.climb = False
        self.push_cnt = 25
        self.push = False
        self.left = self.right = False
        self.near_wall = False

        self.attack_speed = 100

        self.hp = 100
        self.load_items_from_db()
        self.reload_energy = True
        self.MAX_ENERGY = 100

    def get_rect(self):
        return self.rect

    def load_items_from_db(self):
        con = sqlite3.connect("data/Items.sqlite")
        cur = con.cursor()
        t = 0
        self.items = list(map(lambda x: x[0], cur.execute("""SELECT name FROM all_items WHERE in_cur_invent > 0""").fetchall()))

        for item in self.items:
            if item == "Волшебный Посох":
                t += 1
            items_function[item](self)
        if not self.items:
            items_function["standart"](self)
        self.mw = t
    def check_energy(self):
        if self.reload_energy:
            self.energy += self.energy_v / self.fps
            if self.energy > self.MAX_ENERGY:
                self.energy = 100
        else:
            self.energy -= self.energy_v / self.fps
            if self.energy < 0:
                self.energy = 0

    def jump_and_fall(self, enemys):
        last_x = self.rect.x
        last_y = self.rect.y

        if self.push:
            self.rect.x += 150 / self.fps * self.push
            if pygame.sprite.spritecollide(self, self.all_sprites, False) or self.rect.x < 0:
                self.rect.x = last_x
            self.push_cnt -= 1
            if self.push_cnt == 0:
                self.push_cnt = 25
                self.push = False
        self.rect.y -= self.fall_vector * self.vy / self.fps

        temp = pygame.sprite.spritecollide(self, self.all_sprites, False)
        if temp:
            for en in pygame.sprite.spritecollide(self, enemys, False):
                time = dt.datetime.now().time()
                if dt.timedelta(hours=time.hour, minutes=time.minute,
                                      seconds=time.second) >= self.time_to_get_damage + en.attack_speed:
                    self.get_damage(en.damage)
                    if en.rect.x + en.rect.w < self.rect.x:
                        self.push = 1
                    else:
                        self.push = -1
                    self.fall_vector = 3
                    self.time_to_get_damage = dt.timedelta(hours=time.hour, minutes=time.minute,
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
            self.hp = 0
            self.kill()

    def get_damage(self, d):
        self.hp -= d * ((100 - self.damage_resist) / 100)
        self.total_damage_block += d * (self.damage_resist / 100)

    def update(self, objects, enemys):
        last_x = self.rect.x
        last_y = self.rect.y
        w = 0
        s = 0
        self.check_energy()
        if not self.climb:
            self.reload_energy = True
        if self.left:
            self.image = self.im_left
        else:
            self.image = self.im_right

        for en in enemys:
            if self.rect.colliderect(en.rect):
                time = dt.datetime.now().time()
                if dt.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second) >= self.time_to_get_damage + en.attack_speed:
                    self.get_damage(en.damage)
                    if en.rect.x + en.rect.w >= self.rect.x >  en.rect.x:
                        self.push = 1
                    else:
                        self.push = -1
                    self.fall_vector = 3
                    self.time_to_get_damage = dt.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
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
        self.attack = Attack((self.rect.x, self.rect.y), -90, self.damage, 50)

        if self.climb and self.near_wall:
            self.reload_energy = False
            self.check_energy()
            if self.energy:
                self.rect.x = last_x
                self.fall_vector = 0
                if self.onfloor:
                    self.rect.y -= w
                else:
                    self.rect.y -= w - s
                if pygame.sprite.spritecollide(self, self.all_sprites, False):
                    self.rect.y = last_y
            else:
                self.cull_down = True
                self.reload_energy = True
