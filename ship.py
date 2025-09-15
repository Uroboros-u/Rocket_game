import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, rocket_game):
        super().__init__()
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()

        self.image = pygame.image.load('images/rocket.bmp').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.alive_flag = True

        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.rect.y - 20

        self.x = float(self.rect.x)


        self.moving_right = False
        self.moving_left = False


    def kill_ship(self):
        self.alive_flag = False
        self.kill()


    def blitme(self):
        self.screen.blit(self.image, self.rect)


    def update(self, rocket_game):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            if rocket_game.rocket_speed >= 5:
                self.x += 4 + rocket_game.rocket_speed - 5
            else:
                self.x += 4

        if self.moving_left and self.rect.left > self.screen_rect.left:
            if rocket_game.rocket_speed >= 5:
                self.x -= 4 + rocket_game.rocket_speed - 5
            else:
                self.x -= 4


        self.rect.x = self.x
