import pygame, random
from pygame.sprite import Sprite

from constants import ASTEROID_SPEED

class Asteroid(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        img = self._random_asteroid()

        self.original_image = pygame.image.load(img).convert_alpha()
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect.midtop = self.screen_rect.midtop
        self.rect.y = -150
        self.y = -150
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)


    def _random_asteroid(self):
        asteroids = ['assets/images/braun_big.bmp',
                     'assets/images/braun_small.bmp',
                     'assets/images/gray_big.bmp',
                     'assets/images/gray_small.bmp']

        return random.choice(asteroids)

    def update(self, dt, scroll_speed):
        vy = ASTEROID_SPEED  + scroll_speed
        self.y += vy * dt
        self.rect.y = int(self.y)

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.top > self.screen_rect.bottom:
            self.kill()

    def draw(self, screen):
        self.screen.blit(self.image, self.rect)



