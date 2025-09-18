import pygame, random, sys

from ship import Ship
from states import GameState
from asteroid import Asteroid
from stars import Stars
from gasoline import Gasoline
from score import Score
from game_over_screen import GameOver
from fuel_indicator import FuelIndicator
from menu_screen import StartGame

class Rocket:
    def __init__(self):
        pygame.init()
        # Винести в Music module
        pygame.mixer.init()
        pygame.mixer.music.load('assets/sounds/space-theme-loop-ready.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        self.screen = pygame.display.set_mode((400, 700), pygame.SCALED, vsync=True)
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.asteroids_type = ['images/braun_big.bmp', 'images/gray_big.bmp', 'images/braun_small.bmp', 'images/gray_small.bmp']
        self.game_over = GameOver(self.screen)
        self.start_game_screen = StartGame(self.screen)


        self.spawn_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.spawn_event, 1000)

        self.fuel_event = pygame.USEREVENT + 2
        pygame.time.set_timer(self.fuel_event, 10000)

        self._build_world()


    def go_menu(self):
        self.state = GameState.MENU
        pygame.time.set_timer(self.spawn_event, 0)
        pygame.time.set_timer(self.fuel_event, 0)
        self._build_world()
        pygame.time.set_timer(self.spawn_event, 1000)
        pygame.time.set_timer(self.fuel_event, 10000)


    def go_game(self):
        self.state = GameState.GAME


    def go_game_over(self):
        self.state = GameState.GAME_OVER



    def _build_world(self):
        self.gasoline_add_list = [1000, 5000, 10000, 20000, 40000, 70000, 100000, 135000, 180000, 250000]
        self.ship = Ship(self)
        self.fuel_bar = FuelIndicator(self)
        self.ship_group = pygame.sprite.GroupSingle(self.ship)
        self.rocket_speed = 5
        self.event_type = 'ASTEROID'

        self.asteroids = pygame.sprite.Group()
        self.gasoline_canisters = pygame.sprite.Group()
        self._create_stars()
        self.score = Score(self)

    def reset_game(self):
        self.go_menu()


    def run_game(self):
        while self.running:
            self._check_events()
            if self.state == 'MENU':
                pass
            elif self.state == "GAME":
                self.asteroids.update()
                self.ship.update(self)
                self.gasoline_canisters.update()
                self.stars.update(self.rocket_speed)
                self._add_new_star(self.stars)
                self._check_collide()

            elif self.state == "GAME_OVER":
                self.game_over.set_score(self.score.score)

            self._update_screen()
            self.clock.tick(120)
        pygame.quit()


    def _create_stars(self):
        self.stars = pygame.sprite.Group()
        for star in range(0, 40):
            x = random.randrange(1, 400)
            y = random.randrange(1, 700)
            self.stars.add(Stars(self, x, y))

    def _add_new_star(self, stars):
        if len(self.stars) < 80:
            x = 80 - len(self.stars)
            for i in range(0, x):
                x = random.randrange(1, 400)
                y = random.randrange(-700, 0)
                self.stars.add(Stars(self, x, y))



    def _check_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.start_game_screen.button_rect.collidepoint(event.pos):
                        self.state = "GAME"
                elif event.type == pygame.KEYDOWN:
                        self._key_down_events(event)
                elif event.type == pygame.KEYUP:
                    self._key_up_events(event)
                elif event.type == self.spawn_event and self.state == 'GAME':
                    self.score.update_score(self.rocket_speed)
                    self._type_of_event()

                    if len(self.asteroids) < 1 and self.event_type == 'ASTEROID' and len(self.gasoline_canisters) < 1:
                        asteroid = self.asteroids_type[random.randint(0,3)]
                        new_ast = Asteroid(self, asteroid, self.rocket_speed)
                        self.asteroids.add(new_ast)
                    elif self.event_type == 'GASOLINE':
                        new_gasoline = Gasoline(self, self.rocket_speed)
                        self.gasoline_canisters.add(new_gasoline)

                elif event.type == self.fuel_event and self.state == 'GAME':
                    self.fuel_bar.on_enter()
                    self.fuel_bar.fuel_update()



    def _type_of_event(self):
        next_gasoline = self.gasoline_add_list[0]
        if self.score.score >= next_gasoline:
            self.event_type = 'GASOLINE'
            self.gasoline_add_list.pop(0)
        else:
            self.event_type ='ASTEROID'



    def _key_down_events(self, event):
        if event.key == pygame.K_RIGHT and self.state == 'GAME':
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT and self.state == 'GAME':
            self.ship.moving_left = True
        elif event.key == pygame.K_UP and self.state == 'GAME':
            for asteroid in self.asteroids:
                asteroid.vy += 1
            for gasoline in self.gasoline_canisters:
                gasoline.vy += 1
            self.rocket_speed += 1
        elif event.key == pygame.K_DOWN and self.state == 'GAME':
            for asteroid in self.asteroids:
                if asteroid.vy > 1:
                    asteroid.vy -= 1
            for gasoline in self.gasoline_canisters:
                if gasoline.vy > 1:
                    gasoline.vy -= 1
            if self.rocket_speed > 1:
                self.rocket_speed -= 1
        elif event.key == pygame.K_ESCAPE and self.state == 'GAME':
            self.state = 'MENU'
        elif event.key == pygame.K_ESCAPE and self.state == 'MENU':
            self.state = 'GAME'
        elif event.key == pygame.K_r and self.state == 'GAME_OVER':
            self.reset_game()
        elif event.key == pygame.K_ESCAPE and self.state == 'GAME_OVER':
            sys.exit()


    def _key_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False



    def _update_screen(self):
        if self.state == 'MENU':
            self.start_game_screen.draw()
        elif self.state == 'GAME':
            self.screen.fill((4,0,63))
            for stars in self.stars.sprites():
                stars.draw_star()
            self.ship.blitme()
            for asteroid in self.asteroids.sprites():
                asteroid.draw_asteroid()
            for gasoline in self.gasoline_canisters.sprites():
                gasoline.draw_gasoline()
            self.score.blitme()
            self.fuel_bar.blitme(self)
        elif self.state == 'GAME_OVER':
            self.screen.fill((255,255,255))
            self.game_over.draw()

        pygame.display.flip()



    def _check_collide(self):
        if pygame.sprite.spritecollide(self.ship_group.sprite, self.asteroids, False, pygame.sprite.collide_mask):
            self.state = 'GAME_OVER'
            self.game_over.on_enter()

        elif pygame.sprite.spritecollide(self.ship_group.sprite, self.gasoline_canisters, False, pygame.sprite.collide_mask):
            if self.fuel_bar.fuel < 3:
                self.fuel_bar.fuel += 1
            elif self.fuel_bar.fuel == 3:
                pygame.time.set_timer(self.fuel_event, 0)
                pygame.time.set_timer(self.fuel_event, 10000)

            for gasoline in self.gasoline_canisters:
                gasoline.kill_canister()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    rocket = Rocket()
    rocket.run_game()

