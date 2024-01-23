import pygame
import random
from pygame.sprite import Sprite
class MagicAttack(pygame.sprite.Sprite):
    def init(self, pos, scale, color):
        super().init()
        self.image = pygame.Surface([scale, scale])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.speed = 10
        def update(self):
            if self.rect.x < 600:
                self.rect.x += self.speed
                else:
                    for enemy in enemies:
                        if pygame.sprite.collide_rect(self, enemy):
                             self.kill()
                             enemy.health -= 20
                             break
                        else:
                            self.kill()
enemy = Enemy(random.randint(0, 590), 64, (255, 0, 0))
enemies.add(enemy)
magic_attack = MagicAttack(300, 32, (0, 255, 0))
# Запустить атаку магии
all_sprites_list = pygame.sprite.LayeredUpdates()
all_sprites_list.add(enemies, magic_attack)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        all_sprites_list.update()
                        magic_attack.update()  # Обновить атаку магии после нажатия клавиши
                        all_sprites_list.draw(screen)
# сразу с примером как она примерно должна работать 
