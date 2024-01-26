import pygame, os
from load_image import load_image

pygame.init()

tile_width = tile_height = 51
floor = pygame.image.load(os.path.join('data', "Ground.jpg"))
floor = pygame.transform.scale(floor, (tile_width, tile_height))
floor_up = pygame.image.load(os.path.join('data', "Ground_up.jpg"))
floor_up = pygame.transform.scale(floor_up, (tile_width, tile_height))

wall = pygame.image.load(os.path.join('data', "wall.jpg"))
wall = pygame.transform.scale(wall, (tile_width, tile_height))

tile_images = {
    'wall': wall,
    'floor': floor,
    'floor_up': floor_up
}

class BaseObject(pygame.sprite.Sprite):
    def __init__(self, group, tile_type, pos_x, pos_y, all_sprites):
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        super().__init__(group, all_sprites)
