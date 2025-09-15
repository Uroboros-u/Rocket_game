import pygame, random
from pygame.sprite import Sprite

class Asteroid(Sprite):
    def __init__(self, rocket_game, asteroid, speed):
        super().__init__()
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()

        self.original_image = pygame.image.load(asteroid).convert_alpha()
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)


        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = -150

        self.angle = 0

        self.rotation_speed = random.uniform(-0.2, 0.2)


        self.vy = speed


    def update(self):
        self.rect.y = self.rect.y + self.vy

        self.angle = (self.angle + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

        self.mask = pygame.mask.from_surface(self.image)

        if self.rect.top > self.screen_rect.bottom:
            self.kill()

    def draw_asteroid(self):
        """Draw the bullet to the screen."""
        self.screen.blit(self.image, self.rect)



