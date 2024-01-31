import datetime as dt
from load_image import load_image
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, x, y, fps, w, h, all_sprites):
        super().__init__(group, all_sprites)
        self.image = load_image("enemy.png", colorkey="white")
        self.image = pygame.transform.scale(self.image, (100, 80))
        self.rect = self.image.get_rect()
        self.playerx = None
        self.playerw = 25
        self.agr_range = 200
        self.rect.midbottom = (x, y)
        self.vx, self.vy = 55, 100
        self.w, self.h = w, h
        self.damage = 25
        self.fall_vector = 0
        self.step = 0
        self.fps = fps
        self.hp = 100
        self.animation_dct = {"right_leg": pygame.transform.scale(load_image("enemy_right.png", colorkey="white"), (100, 80)), "stand": pygame.transform.scale(load_image("enemy.png", colorkey="white"), (100, 80)),
                 "right_leg2": pygame.transform.scale(load_image("enemy_right2.png", colorkey="white"), (100, 80)), "left_leg": pygame.transform.scale(load_image("enemy_left.png", colorkey="white"), (100, 80)),
                 "left_leg2": pygame.transform.scale(load_image("enemy_left2.png", colorkey="white"), (100, 80))}
        self.walk_animation = ["stand", "right_leg", "right_leg", "right_leg", "right_leg", "right_leg", "right_leg2",
                               "right_leg2", "right_leg2", "right_leg2", "right_leg2",
                               "stand", "stand", "stand", "stand", "stand", "left_leg", "left_leg", "left_leg", "left_leg", "left_leg", "left_leg2", "left_leg2",
                               "left_leg2", "left_leg2", "left_leg2", "stand"]
        self.attack_speed = dt.timedelta(seconds=1.7)

    def set_player(self, playerx):
        if self.rect.x + self.rect.h + self.agr_range > playerx > self.rect.x - self.agr_range:
            self.playerx = playerx
        else:
            self.playerx = None

    def jump_and_fall(self):
        self.rect.y -= self.fall_vector * self.vy / self.fps
        self.fall_vector -= 1

    def get_damage(self, attack):
        self.hp -= attack.damage
        if self.hp <= 0:
            attack.hero.kills += 1

    def check_hp(self):
        if self.hp <= 0:
            self.kill()

    def update(self, objects, player):
        last_x = self.rect.x
        last_y = self.rect.y
        self.jump_and_fall()
        self.check_hp()

        if self.playerx != None:
            if self.playerx + self.playerw - 5 <=  self.rect.x:
                self.rect.x -= self.vx / self.fps
                self.image = self.animation_dct[self.walk_animation[self.step]]
                self.step += 1
                if self.step >= len(self.walk_animation):
                    self.step = 0
            elif self.playerx >= self.rect.x + self.rect.w:
                self.rect.x += self.vx / self.fps
                self.image = pygame.transform.flip(self.animation_dct[self.walk_animation[self.step]], True, False)
                self.step += 1
                if self.step >= len(self.walk_animation):
                    self.step = 0
        else:
            self.image = self.animation_dct["stand"]

        temp = pygame.sprite.spritecollide(self, objects, False)

        for obj in temp:
            conx1 = obj.rect.x + obj.rect.w > self.rect.x + self.rect.w > obj.rect.x
            conx2 = obj.rect.x + obj.rect.w > self.rect.x > obj.rect.x
            cony_up = obj.rect.y < self.rect.y + self.rect.h < obj.rect.h + obj.rect.y
            cony_down = obj.rect.y < self.rect.y < obj.rect.h + obj.rect.y
            if conx1 or conx2:
                self.rect.x = last_x
                # self.image = self.animation_dct["stand"]
            if cony_down and last_y > obj.rect.y + obj.rect.h:
                self.rect.y = obj.rect.y + obj.rect.h
                self.fall_vector = 0
            if cony_up and last_y + self.rect.h <= obj.rect.y:
                self.floor = obj.rect.y - self.rect.h
                self.rect.y = obj.rect.y - self.rect.h
                self.fall_vector = 0
