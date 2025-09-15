import pygame

class Score:
    def __init__(self, rocket_game):
        self.screen = rocket_game.screen
        self.screen_rect = rocket_game.screen.get_rect()

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 36, True)

        self.text_surface = self.font.render(str(self.score), True, (187, 77, 26))

        self.rect = self.text_surface.get_rect()

        self.rect.topleft = self.screen_rect.topleft
        self.rect.x += 10
        self.rect.y += 10


    def blitme(self):
        self.screen.blit(self.text_surface, self.rect)

    def update_score(self, rocket_speed):
        if rocket_speed <= 8:
            rocket_speed = rocket_speed * 0.1

        self.score = int(self.score + (100 * rocket_speed))
        self.text_surface = self.font.render(str(self.score), True, (187, 77, 26))
        self.rect = self.text_surface.get_rect()
        self.rect.topleft = self.screen_rect.topleft
        self.rect.x += 10
        self.rect.y += 10