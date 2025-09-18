import pygame, random, sys

from constants import *
from ship import Ship
from states import GameState
from asteroid import Asteroid
from stars import StarsField
from gasoline import Gasoline
from score import Score
from game_over_screen import GameOver
from fuel_indicator import Fuel
from menu_screen import StartGame


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('assets/sounds/space-theme-loop-ready.wav')
        self.asteroids_type = ['images/braun_big.bmp', 'images/gray_big.bmp', 'images/braun_small.bmp',
                               'images/gray_small.bmp']
        self.screen = pygame.display.set_mode((400, 700), pygame.SCALED, vsync=True)
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU

        self.scroll_speed = MIN_SCROLL_SPEED

        self.spawn_acc = 0.0
        self.fuel_acc = 0.0
        self.gasoline = 0.0
        self.time_alive = 0.0

        self.fuel_spawn_interval = FUEL_SPAWN_INTERVAL

        self.go_menu()

    def go_menu(self):
        self.state = GameState.MENU

        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        # if hasattr(self, "all_sprites"): self.all_sprites.empty()
        # if hasattr(self, "asteroids"): self.asteroids.empty()

        self.menu_screen = StartGame(self.screen)
        self.game_over_screen = None

    def go_game(self):
        self.state = GameState.GAME

        self.spawn_acc = 2.0
        self.fuel_acc = 0.0
        self.gasoline = 0.0
        self.time_alive = 0.0

        self.scroll_speed = MIN_SCROLL_SPEED

        self.ship = Ship(self)
        self.fuel = Fuel(self)
        self.score = Score(self)
        self.fuel_spawn_interval = FUEL_SPAWN_INTERVAL

        self.all_sprites = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.gas_items = pygame.sprite.Group()
        self.stars = StarsField(400, 700)

        if hasattr(self, "all_sprites"): self.all_sprites.empty()
        if hasattr(self, "asteroids"): self.asteroids.empty()

        self.menu_screen = None

    def go_game_over(self):
        self.state = GameState.GAME_OVER
        pygame.mixer.music.stop()
        self.game_over_screen = GameOver(self.screen)


# MENU ----
    def handle_event_menu(self, e: pygame.event.Event):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.menu_screen and self.menu_screen.button_rect.collidepoint(e.pos):
                self.go_game()
            pass
        if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.go_game()

    def update_menu(self, dt: float):
        pass

    def draw_menu(self, screen: pygame.Surface):
        if self.menu_screen: self.menu_screen.draw()



# GO_GAME ----
    def handle_event_game(self, e: pygame.event.Event):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif e.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif e.key == pygame.K_UP:
                self.scroll_speed = min(self.scroll_speed + SCROLL_STEP, MAX_SCROLL_SPEED)
            elif e.key == pygame.K_DOWN:
                self.scroll_speed = max(self.scroll_speed - SCROLL_STEP, MIN_SCROLL_SPEED)

        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif e.key == pygame.K_LEFT:
                self.ship.moving_left = False

        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            self.go_menu()


    def update_game(self, dt: float):
        self.stars.update(dt, self.scroll_speed)
        self.ship.update(self.scroll_speed, dt)
        self.asteroids.update(dt, self.scroll_speed)
        self.gas_items.update(dt, self.scroll_speed)
        self._spawn_asteroid(dt)
        self._spawn_gasoline(dt)
        self.fuel.update()
        self._fuel(dt)
        self.score.update(dt, self.scroll_speed)
        self._check_collision()


    def _check_collision(self):
        ship = self.ship
        candidates_gas = pygame.sprite.spritecollide(ship, self.gas_items, dokill=False)
        picked_any = False

        for gas in candidates_gas:
            collide = pygame.sprite.collide_mask(ship, gas) if hasattr(ship, "mask") and hasattr(gas, "mask") else True
            if collide:
                picked_any = True
                gas.kill()
                self.fuel.plus_fuel()
                self.fuel_acc = 0.0

        # --- корабель vs астероїди ---
        candidates_ast = pygame.sprite.spritecollide(ship, self.asteroids, dokill=False)
        for ast in candidates_ast:
            collide = pygame.sprite.collide_mask(ship, ast) if hasattr(ship, "mask") and hasattr(ast, "mask") else True
            if collide:
                self.go_game_over()
                return

    def _fuel(self, dt):
        self.fuel_acc += dt
        if self.fuel_acc > 5.0:
            fuel = self.fuel.minus_fuel()
            if not fuel:
                self.go_game_over()
            self.fuel_acc = 0.0

    def _spawn_asteroid(self, dt):
        relative_speed_y = abs(ASTEROID_SPEED + self.scroll_speed)
        spawn_interval = 1.0 / (0.5 * (relative_speed_y / 200))

        self.spawn_acc += dt
        while self.spawn_acc >= spawn_interval:
            self.spawn_acc -= spawn_interval
            asteroid = Asteroid(self.screen)  # передай інші параметри, які в тебе є
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)

    def _spawn_gasoline(self, dt):
        self.gasoline += dt
        self.time_alive += dt
        k = self.scroll_speed / 100
        spawn_interval = self.fuel_spawn_interval / k + self.time_alive / 5
        while self.gasoline >= spawn_interval:
            self.gasoline -= spawn_interval
            gasoline = Gasoline(self.screen)  # передай інші параметри, які в тебе є
            self.gas_items.add(gasoline)
            self.all_sprites.add(gasoline)

    def draw_game(self, screen: pygame.Surface):
        screen.fill((4, 0, 63))
        self.stars.draw(screen)
        self.asteroids.draw(screen)
        self.gas_items.draw(screen)
        self.score.draw()
        self.fuel.draw()
        self.ship.draw()



# GO_GAME_OVER
    def handle_event_game_over(self, e: pygame.event.Event):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            self.go_menu()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            sys.exit()

    def update_game_over(self, dt: float):
        self.game_over_screen.set_score(self.score.score)

    def draw_game_over(self, screen: pygame.Surface):
        if self.game_over_screen: self.game_over_screen.draw()




    def handle_event(self, e):
        if self.state is GameState.MENU:
            self.handle_event_menu(e)
        elif self.state is GameState.GAME:
            self.handle_event_game(e)
        elif self.state is GameState.GAME_OVER:
            self.handle_event_game_over(e)

    def update(self, dt: float):
        if self.state is GameState.MENU:
            self.update_menu(dt)
        elif self.state is GameState.GAME:
            self.update_game(dt)
        elif self.state is GameState.GAME_OVER:
            self.update_game_over(dt)

    def draw(self, screen: pygame.Surface):
        if self.state is GameState.MENU:
            self.draw_menu(screen)
        elif self.state is GameState.GAME:
            self.draw_game(screen)
        elif self.state is GameState.GAME_OVER:
            self.draw_game_over(screen)

    def run_game(self):
        """main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(e)

            self.update(dt)
            self.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
