import pygame

class StartGame:
    def __init__(self, screen, font_name="Arial"):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.font = pygame.font.SysFont(font_name, 18, True)

        self.text = self.font.render('Start Game', True, (255,255,255))
        self.rect_text = self.text.get_rect(center=(400 // 2, 700 // 2))
        self.button_rect = pygame.Rect(400 // 2 - 100, 700 // 2 - 20, 200, 40)


        self.image = pygame.image.load('images/start_screen.png').convert_alpha()
        self.rect_img = self.image.get_rect()

        self.rect_img.center = self.screen_rect.center


    def draw(self):
        self.screen.blit(self.image, self.rect_img)
        pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect, width=2 ,border_radius=5)
        self.screen.blit(self.text, self.rect_text)




