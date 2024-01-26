import pygame

from Controller import Controller
from windows import Menu

screen = pygame.display.set_mode((1000, 500))
pygame.init()
controller = Controller()
mn = Menu(1000, 500, controller)
controller.set_current_window(mn)
game = True
fps = 60
clock = pygame.time.Clock()
while game:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if controller.window_event(event, keys=keys):
            game = False
    controller.open_window(screen)
    clock.tick(fps)
    pygame.display.flip()