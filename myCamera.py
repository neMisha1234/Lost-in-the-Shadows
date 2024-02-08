import pygame


class Camera:
    def __init__(self, player, map, w, h, end_x, end_y):
        self.player = player
        self.map = map
        self.w, self.h = w, h
        self.end_x = end_x
        self.end_y = end_y

    def follow_player(self):
        x = (self.player.rect.x + self.player.rect.w // 2 - self.w // 2)
        y = self.player.rect.y + self.player.rect.h // 2 - self.h // 2
        if x < 0:
            x = 0
        elif self.w + x > self.end_x:
            x = self.end_x - self.w
        if y < 0:
            y = 0
        if self.h + y >= self.end_y:
            y = self.end_y - self.h

        return (-x, -y)