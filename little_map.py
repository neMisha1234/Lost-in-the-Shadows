import pygame
from HpBar import HpBar

from BaseCharacter import BaseCharacter
from Field import load_level, generate_level
from Enemy import Enemy

hero_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
size = w, h = 2000, 500
pygame.init()
map = pygame.surface.Surface(size)
map.fill((255, 255, 255))
screen = pygame.display.set_mode((1000, 500))
fps = 60


def generate_location():
    generate_level(load_level("small_lvl"), objects, all_sprites)


clock = pygame.time.Clock()
game = True
generate_location()
enemy = Enemy(enemy_sprites, 400, 200, fps, w, h, all_sprites)
hero = BaseCharacter(hero_sprites, 50, 200, fps, w, h, all_sprites)
hpbar = HpBar(750, h - 50, hero.hp)

while game:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            hero.climb = True
        else:
            hero.climb = False

    map.fill((255, 255, 255))

    hero_sprites.update(objects, enemy_sprites)
    hero_sprites.draw(map)
    if not hero_sprites:
        print("GAME_OVER")
        break
    hpbar.draw(map)

    enemy_sprites.update(objects, hero)
    enemy_sprites.draw(map)
    enemy.set_player(hero.rect.x)

    objects.draw(map)
    hpbar.update(hero.hp)
    hpbar.draw(map)
    screen.blit(map, (0, 0))


    pygame.display.flip()
