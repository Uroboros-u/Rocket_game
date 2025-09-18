import pygame

class GameOver:
    def __init__(self, screen, font_name="Arial"):
        self.screen = screen
        self.rect = self.screen.get_rect()

        self.font_title = pygame.font.SysFont(font_name, 56, True)
        self.font_text  = pygame.font.SysFont(font_name, 32, True)
        self.font_hint  = pygame.font.SysFont(font_name, 16, True)


        self.title_surf = self.font_title.render("GAME OVER", True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(self.rect.centerx, self.rect.centery - 80))

        self.hint_surf = self.font_hint.render("Press R to Restart • Esc to Quit", True, (220, 220, 220))
        self.hint_rect = self.hint_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 60))


        self.overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.overlay.fill((4,0,63))


        self._last_score = None
        self.score_surf = None
        self.score_rect = None


    def set_score(self, score: int):
        if score != self._last_score:
            self._last_score = score
            text = f"Your score: {score}"
            self.score_surf = self.font_text.render(text, True, (240, 240, 240))
            self.score_rect = self.score_surf.get_rect(center=self.rect.center)

    def draw(self):
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.title_surf, self.title_rect)
        if self.score_surf:
            self.screen.blit(self.score_surf, self.score_rect)
            self.screen.blit(self.hint_surf, self.hint_rect)
