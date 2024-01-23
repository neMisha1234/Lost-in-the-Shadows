import pygame
import math


class Attack(pygame.sprite.Sprite):
    def init(self, pos, angle, damage, range):
        super().init()
        self.image = pygame.Surface([50, 50])
        self.rect = self.image.get_rect()
        self.pos = pos
        self.angle = angle
        self.damage = damage
        self.range = range

    def update(self):
        self.move_to_direction(self.angle)
        if self.rect.colliderect(self.enemy.rect):
            self.enemy.health -= self.damage

    def move_to_direction(self, angle):
        angle = math.radians(angle)
        x = math.cos(angle) * 4
        y = math.sin(angle) * 4
        self.rect.move_ip(x, y)


class Enemy(pygame.sprite.Sprite):
    def handle_attack(self, attack):
        if attack.rect.distance_to(self.rect) <= attack.range:
            print('atack sucsesfully')
        else:
            print("Attack_misses!")

def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    enemy = Enemy(screen.get_width() // 2, screen.get_height() // 3, (100, 100), (64, 64))
    attack = Attack((enemy.rect.centerx(), enemy.rect.centery()), -90, 110, 200)
    all_sprites.add(enemy, attack)
