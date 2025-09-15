import pygame, random
from pygame.sprite import Sprite

class Gasoline(Sprite):
    def __init__(self, rocket_game, speed):
        super().__init__()
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()

        self.image = pygame.image.load('images/gasoline.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -150

        self.vy = speed

    def update(self):
        self.rect.y = self.rect.y + self.vy

        if self.rect.top > self.screen_rect.bottom:
            self.kill_canister()

    def kill_canister(self):
        self.kill()

    def draw_gasoline(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)



