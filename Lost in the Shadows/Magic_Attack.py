import pygame
from load_image import load_image


class MagicAttack(pygame.sprite.Sprite):
    def __init__(self, pos, damage, scale, color, hero, attack_speed):
        super().__init__()
        if not hero.mw:
            self.animation_dct = {
                "fb1": pygame.transform.scale(load_image("fireball(1).png", colorkey=(255, 255, 255)), (scale + 20, scale)),
                "fb2": pygame.transform.scale(load_image("fireball(2).png", colorkey=(255, 255, 255)), (scale + 20, scale)),
                "fb3": pygame.transform.scale(load_image("fireball(3).png", colorkey=(255, 255, 255)), (scale + 20, scale)),
                "fb4": pygame.transform.scale(load_image("fireball(4).png", colorkey=(255, 255, 255)), (scale + 20, scale))}
        else:
            self.animation_dct = {
                "fb1": pygame.transform.scale(load_image("greenball(1).png", colorkey=(255, 255, 255)),
                                              (scale + 20, scale)),
                "fb2": pygame.transform.scale(load_image("greenball(2).png", colorkey=(255, 255, 255)),
                                              (scale + 20, scale)),
                "fb3": pygame.transform.scale(load_image("greenball(3).png", colorkey=(255, 255, 255)),
                                              (scale + 20, scale)),
                "fb4": pygame.transform.scale(load_image("greenball(4).png", colorkey=(255, 255, 255)),
                                              (scale + 20, scale))}
        self.image = self.animation_dct["fb1"]
        self.rect = self.image.get_rect()
        self.damage = damage
        self.rect.x, self.rect.y = pos
        self.speed = attack_speed
        self.fps = 60
        self.hero = hero

        self.fly_anim = ["fb1", "fb1", "fb1", "fb2", "fb2", "fb2", "fb3", "fb3", "fb3", "fb3", "fb4", "fb4", "fb4"]
        self.flag = -1 if hero.left else 1
        self.step = 0

    def update(self, enemies, objects):
        self.hero.is_attack = False
        if self.hero.rect.x - 400 <= self.rect.x <= self.hero.rect.x + 400:
            self.rect.x += self.speed / self.fps * self.flag
            self.image = self.animation_dct[self.fly_anim[self.step]]
            if self.flag == 1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.step += 1
            if self.step >= len(self.fly_anim):
                self.step = 0
            if pygame.sprite.spritecollideany(self, objects):
                self.kill()
            for enemy in enemies:
                if pygame.sprite.collide_rect(self, enemy):
                    self.kill()
                    self.hero.total_damage += self.damage
                    enemy.get_damage(self)
                    break
        else:
            self.kill()
