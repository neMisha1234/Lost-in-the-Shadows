import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
timer = pygame.time.Clock()


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))
    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False
    up = False
    hero.update(left, right)  # передвижение
    hero.draw(screen)

    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True

            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True

            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False
        screen.blit(bg, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()