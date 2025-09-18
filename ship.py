import pygame
from pygame.sprite import Sprite

from constants import SHIP_SPEED


class Ship(Sprite):
    def __init__(self, rocket_game):
        super().__init__()
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()

        self.image = pygame.image.load('assets/images/rocket.bmp').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.rect.y - 20
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False
        self.alive_flag = True

    def kill_ship(self):
        self.alive_flag = False
        self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self, scroll_speed, dt):
        vx = SHIP_SPEED + scroll_speed

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += vx * dt
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= vx * dt

        self.rect.x = int(self.x)
