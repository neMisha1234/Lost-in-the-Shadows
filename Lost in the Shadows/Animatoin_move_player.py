import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 576))
icon = pygame.image.load('images/hqdefault.jpg')
pygame.display.set_icon(icon)
bg = pygame.image.load('images/pp.jpg')
playerx = 150
playerspeed = 10
playery = 200
is_jump = False
jump = 10
animation_walk = [pygame.image.load('images/image1.png'),
                  pygame.image.load('images/image3.png'),
                  pygame.image.load('images/image4.png'),
                  pygame.image.load('images/image5.png'),
                  pygame.image.load('images/image6.png'),
]
player_anim_count = 1
running = True
while running:
    screen.blit(bg, (0, 0))
    screen.blit(animation_walk[player_anim_count], (playerx, playery))
    if player_anim_count == 4:
        player_anim_count = 0
    else:
        player_anim_count += 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] and playerx <= 900:
        playerx += playerspeed
    elif keys[pygame.K_a] and playerx >= 50:
        playerx -= playerspeed
    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump >= -10:
            if jump > 0:
                playery -= (jump ** 2) / 2
            else:
                playery += (jump ** 2) / 2
            jump -= 1
        else:
            is_jump = False
            jump = 10


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(10)
pygame.quit()
