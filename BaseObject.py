import pygame

wall = pygame.surface.Surface((51, 51))
wall.fill((0, 0, 255))
floor = pygame.surface.Surface((51, 51))
floor.fill((150, 255, 250))
tile_images = {
    'wall': wall,
    'floor': floor
}

tile_width = tile_height = 51

class BaseObject(pygame.sprite.Sprite):
    def __init__(self, group, tile_type, pos_x, pos_y, all_sprites):
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        super().__init__(group, all_sprites)
