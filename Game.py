import pygame
from HpBar import HpBar
from BaseCharacter import BaseCharacter
from Field import load_level, generate_level
from Enemy import Enemy


class Game:
    def __init__(self, cont, menu, go):
        self.controller = cont
        self.menu = menu
        self.hero_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.size = w, h = 2000, 500
        self.game_over = go

        self.map = pygame.surface.Surface(self.size)
        self.map.fill((255, 255, 255))
        self.fps = 60

        def generate_location():
            generate_level(load_level("small_lvl"), self.objects, self.all_sprites)

        generate_location()
        self.enemy = Enemy(self.enemy_sprites, 400, 200, self.fps, w, h, self.all_sprites)
        self.hero = BaseCharacter(self.hero_sprites, 100, 200, self.fps, w, h, self.all_sprites)
        self.hpbar = HpBar(750, h - 50, self.hero.hp)

    def check_event(self, event):
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.hero.climb = True
        else:
            self.hero.climb = False


    def start(self, screen):
        self.map.fill((255, 255, 255))

        self.hero_sprites.update(self.objects, self.enemy_sprites)
        self.hero_sprites.draw(self.map)
        if not self.hero_sprites:
            print("GAME_OVER")
            self.controller.set_current_window(self.game_over)

        self.hpbar.draw(self.map)

        self.enemy_sprites.update(self.objects, self.hero)
        self.enemy_sprites.draw(self.map)
        self.enemy.set_player(self.hero.rect.x)

        self.objects.draw(self.map)
        self.hpbar.update(self.hero.hp)
        self.hpbar.draw(self.map)
        screen.blit(self.map, (0, 0))