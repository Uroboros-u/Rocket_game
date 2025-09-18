import pygame

class Score:
    def __init__(self, rocket_game):
        self.font = pygame.font.SysFont("Arial", 36, True)
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()
        self.score = 0
        self._rect_settings()

    def draw(self):
        self.screen.blit(self.text_surface, self.rect)

    def update(self, dt, scroll_speed):
        self.score += int(scroll_speed * dt)
        self._rect_settings()

    def _rect_settings(self):
        self.text_surface = self.font.render(str(self.score), True, (187, 77, 26))
        self.rect = self.text_surface.get_rect()
        self.rect.topleft = self.screen_rect.topleft
        self.rect.x += 10
        self.rect.y += 10

