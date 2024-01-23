from turtledemo import clock

import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite


class Camera(object):
    def init(self, player, level_width, level_height):

        self.player = player
        self.level_width = level_width
        self.level_height = level_height
        self.camera_rect = self.get_camera_rect()


    def get_camera_rect(self):
         center_x = (self.level_width * 0.5) - (self.player.rect.width * 0.5)
         center_y = (self.level_height * 0.5) - (self.player.rect.height * 0.5)
         return pygame.Rect(center_x, center_y, self.player.rect.width, self.player.rect.height)


    def follow_player(self, dt):
        # Следовать за игроком
        camera_rect_center = Vector2(self.camera_rect.center)
        player_rect_center = self.player.get_rect().center
        camera_rect_center.x = player_rect_center.x
        camera_rect_center.y = player_rect_center.y
        self.camera_rect = camera_rect_center.as_rectangle()

        if self.camera_rect.right >= self.level_width - self.player.rect.width:
            # Останавливаем движение камеры, когда игрок достигает конца уровня
            self.follow_stopped = True
        elif self.follow_stopped:
            self.camera_rect = self.get_initial_camera_position()
            self.follow_stopped = False
    def get_initial_camera_position(self):
        left_side = self.level_width // 2 - self.camera_rect.width // 2
        top_side = int(self.level_height / 2) - self.camera_rect.height // 2
        return left_side, top_side



# Игрок
player_img = pygame.image.load('player.png').convert_alpha()
player = pygame.sprite.Sprite()
player.image = player_img
player.rect = player_img.get_rect()
player.rect.x = 50
player.rect.y = 450
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)

level_size = 1200
level = [
    [' ', ' ', ' ', ' '],
    ['#', ' ', '#', ' '],
    ['#', '#', '#', ' '],  # Конец уровня
    ['@', '@', '@', '@']  # Блоки с вопросительными знаками
]

for row in level:
    for col in row:
        if col == '#':
            block = pygame.Rect((0, 0), (30, 30))
            block.x = block.width * col_index
            block.y = block.height * row_index

            block_img = pygame.Surface(block.size)
            block_img.fill(pygame.Color('gray10'))
            block_surf = block_img.convert()

            all_sprites_list.add(pygame.sprite.Sprite())
            all_sprites_list[len(all_sprites_list) - 1].image = block_surf
            all_sprites_list[-1].rect = block

        elif col == ' ':
            pass
        else:
            block = pygame.Rect((24, 24), (26, 26))
            block.x = block.width * col_index + 7
            block.y = block.height * row_index + 23
            block_img = pygame.surface.Surface(block.size, pygame.SRCALPHA)
            pygame.draw.circle(block_img, pygame.Color('red'), block.center, 10)
            block_surf = block_img.convert_alpha()

            all_sprites_list.add(Sprite())
            all_sprites_list[len(all_sprites_list) - 1].image = block_surf
            all_sprites_list[-1].rect = block

camera = Camera(player, level_size, level_size)
while True:
    dt = clock.tick(60) / 1000  # 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.rect.move_ip(-1 * player.speed, 0)
    if keys[pygame.K_DOWN]:
        player.rect.move_ip(player.speed, 0)

    all_sprites_list.update()

    follow_player_camera = camera.follow_player(dt)

screen.fill((0, 0, 255))
all_sprites_list.draw(screen)
pygame.display.flip()
main()
