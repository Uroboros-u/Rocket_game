import pygame

class FuelIndicator:
    def __init__(self, rocket_game):
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()
        self.fuel = 3
        self.enter_time = pygame.time.get_ticks()

        self._image_update()

    def on_enter(self):
        self.enter_time = pygame.time.get_ticks()

    def blitme(self, rocket_game):
        if self.fuel == 3:
            self._image_update('images/full.png')
        elif self.fuel == 2:
            self._image_update('images/2.png')
        elif self.fuel == 1:
            self._image_update('images/1.png')
        elif self.fuel == 0:
            elapsed = pygame.time.get_ticks() - self.enter_time
            if elapsed > 400 and (elapsed // 350) % 2 == 0:
                self._image_update('images/empty.png')
            else:
                self._image_update('images/1.png')
        elif self.fuel < 0:
            rocket_game.state = "GAME_OVER"

        self.screen.blit(self.image, self.rect)

    def fuel_update(self):
        self.fuel -= 1


    def _empty(self):
        while self.fuel == 0:
            elapsed = pygame.time.get_ticks() - self.enter_time
            if elapsed > 400 and (elapsed // 350) % 2 == 0:
                self._image_update('images/empty.png')
            else:
                self._image_update('images/1.png')


    def _image_update(self, image='images/full.png'):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topright = self.screen_rect.topright
        self.rect.y = self.rect.y - 5
        self.rect.x = self.rect.x