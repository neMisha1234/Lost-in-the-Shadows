import pygame
from BaseCharacter import BaseCharacter
from BaseObject import BaseObject

hero_sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()
size = w, h = 2000, 500
pygame.init()
map = pygame.surface.Surface(size)
map.fill((255, 255, 255))
screen = pygame.display.set_mode((1000, 500))
fps = 60


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - w // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - h // 2)


def generate_location():
    # floor
    BaseObject(objects, 0, h - 100, w, 100, (50, 50, 50))

    # platform
    BaseObject(objects, 200, 310, 100, 25, (255, 0, 0))

    BaseObject(objects, 500, 330, 50, 70, (255, 0, 0))
    BaseObject(objects, 700, 300, 50, 70, (255, 0, 0))


hero = BaseCharacter(hero_sprites, 50, 200, fps, w, h)
clock = pygame.time.Clock()
game = True
generate_location()

while game:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    map.fill((255, 255, 255))

    hero_sprites.update(objects)
    hero_sprites.draw(map)

    objects.draw(map)
    screen.blit(map, (0, 0))

    pygame.display.flip()
