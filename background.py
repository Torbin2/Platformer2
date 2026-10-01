import math
import random

import pygame


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


class Background:
    def __init__(self, size: tuple[int, int], point_density: float, scale: int, color: tuple[int, int, int] = (255, 255, 255)):
        self._s = pygame.Surface(size)
        self._s.set_colorkey((0, 0, 0))

        self._offsets: dict[int, tuple[float, float]] = {}

        points = []
        not_generated = 0
        min_dist = point_density * min(size) / 10
        for _ in range(round(point_density * min(size))):
            x, y = random.randint(0, self._s.get_width()), random.randint(0, self._s.get_width())

            for ox, oy in points:
                if _dist((ox, oy), (x, y)) < min_dist:
                    break
            else:
                not_generated = 0
                pygame.draw.rect(self._s, color, (x, y, scale, scale))

            if not_generated > 50:
                break
            not_generated += 1

    def render(self, screen: pygame.Surface, render_offset: tuple[float, float], layers: int):
        if screen.get_size() != self._s.get_size():
            raise ValueError('Background needs to be recreated upon screen resize')

        starting_depth = 2
        layer_depth = 5
        for layer in range(starting_depth, layers + starting_depth):
            if layer not in self._offsets:
                self._offsets[layer] = (random.random() * self._s.get_width(), random.random() * self._s.get_height())

            x, y = (
                (render_offset[0] / (layer_depth * layer) + self._offsets[layer][0]) % self._s.get_width(),
                (render_offset[1] / (layer_depth * layer) + self._offsets[layer][1]) % self._s.get_height()
            )
            screen.blit(self._s, (x, y))
            screen.blit(self._s, (x - self._s.get_width(), y))
            screen.blit(self._s, (x, y - self._s.get_height()))
            screen.blit(self._s, (x - self._s.get_width(), y - self._s.get_height()))
