import pygame
from pygame.sprite import Sprite

class Stars(Sprite):
    def __init__(self, rocket_game, x, y):
        super().__init__()
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()

        self.star_width = 2
        self.star_height = 2
        self.star_color = (255, 255, 255)

        self.rect = pygame.Rect(0, 0, self.star_width, self.star_height)


        self.rect.x = x
        self.rect.y = y


    def update(self, speed):
        self.rect.y = self.rect.y + int(speed/3)
        if self.rect.top > self.screen_rect.bottom:
            self.kill()

    def draw_star(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.star_color, self.rect)