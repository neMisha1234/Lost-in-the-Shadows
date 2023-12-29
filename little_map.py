import pygame
from pygame import Rect

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

hero = BaseCharacter(hero_sprites, 50, 200, fps, w, h)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + w / 2, -t + h / 2

    l = min(0, l)
    l = max(-(camera.width - w), l)
    t = max(-(camera.height - h), t)
    t = min(0, t)

    return Rect(l, t, w, h)


camera = Camera(camera_configure, w, h)


def generate_location():
    # floor
    BaseObject(objects, 0, h - 100, w, 100, (50, 50, 50))

    # platform
    BaseObject(objects, 200, 310, 100, 25, (255, 0, 0))

    BaseObject(objects, 500, 330, 50, 70, (255, 0, 0))
    BaseObject(objects, 700, 300, 50, 100, (255, 0, 0))
    BaseObject(objects, 900, 100, 100, 300, (150, 255, 250))


clock = pygame.time.Clock()
game = True
generate_location()

while game:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            hero.climb[0] = True
        else:
            hero.climb[0] = False

    map.fill((255, 255, 255))

    hero_sprites.update(objects)
    hero_sprites.draw(map)
    camera.update(hero)

    objects.draw(map)
    screen.blit(map, (0, 0))

    pygame.display.flip()
