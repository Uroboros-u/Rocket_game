import pygame, random
from pygame.sprite import Sprite

from constants import GASOLINE_SPEED

class Gasoline(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load('assets/images/gasoline.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -150
        self.y = -150


    def update(self, dt, scroll_speed):
        vy = GASOLINE_SPEED + scroll_speed
        self.y += vy * dt
        self.rect.y = int(self.y)

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.top > self.screen_rect.bottom:
            self.kill_canister()

    def kill_canister(self):
        self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)



