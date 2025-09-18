import pygame

class Fuel:
    def __init__(self, rocket_game):
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()
        self.fuel = 3

        self._image_update()


    def minus_fuel(self):
        self.fuel -= 1
        print(self.fuel)
        return self.fuel

    def plus_fuel(self):
        if self.fuel < 3:
            self.fuel += 1

    def update(self):
        if self.fuel == 3:
            self._image_update('assets/images/full.png')
        elif self.fuel == 2:
            self._image_update('assets/images/2.png')
        elif self.fuel == 1:
            self._image_update('assets/images/1.png')
        elif self.fuel == 0:
            self._image_update('assets/images/empty.png')

    def _image_update(self, image='assets/images/full.png'):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topright = self.screen_rect.topright
        self.rect.y = self.rect.y - 5
        self.rect.x = self.rect.x

    def draw(self):
        self.screen.blit(self.image, self.rect)