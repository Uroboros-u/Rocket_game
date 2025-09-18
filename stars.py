import random
import pygame

class StarsField:
    def __init__(
        self,
        width: int,
        height: int,
        layers=(   # (кількість, базова_швидкість, розмір_пікселя)
            (30,  5.0, 1),   # далекий шар
            (20,  10.0, 2)  # ближній шар
        ),
        spawn_rate_per_sec= 5.0,  # середня кількість нових зірок/сек по всіх шарах
        color=(255, 255, 255)
    ):
        self.w, self.h = width, height
        self.color = color
        self.layers_def = layers
        self.spawn_rate = spawn_rate_per_sec
        self.spawn_acc = 0.0

        # зірка = dict(x=float, y=float, vy=float, size=int)
        self.layers = [[] for _ in layers]

        # стартове заповнення екрана
        for i, (count, base_vy, size) in enumerate(layers):
            for _ in range(count):
                x = random.uniform(0, self.w)
                y = random.uniform(0, self.h)
                # рандомізація швидкості
                vy = random.uniform(0.8, 1.2) * base_vy
                self.layers[i].append({"x": x, "y": y, "vy": vy, "size": size})

    def update(self, dt: float, scroll_speed: float):
        for i, stars in enumerate(self.layers):
            for s in stars:
                vy = s["vy"] + scroll_speed / 10
                s["y"] += vy * dt

            # видаляємо ті що нижче екрана
            self.layers[i] = [s for s in stars if s["y"] < self.h + 5]


        self.spawn_acc += dt * self.spawn_rate

        spawn_count = int(self.spawn_acc)
        if spawn_count > 0:
            self.spawn_acc -= spawn_count
            self._spawn_top(spawn_count)

    def _spawn_top(self, n: int):
        for _ in range(n):
            i = random.randrange(len(self.layers))
            count, base_vy, size = self.layers_def[i]
            x = random.uniform(0, self.w)
            y = -2.0  # поза екраном
            vy = random.uniform(0.8, 1.2) * base_vy
            self.layers[i].append({"x": x, "y": y, "vy": vy, "size": size})

    def draw(self, screen: pygame.Surface):
        for stars in self.layers:
            for s in stars:
                x = int(s["x"])
                y = int(s["y"])
                size = s["size"]

                screen.fill(self.color, (x, y, size, size))
