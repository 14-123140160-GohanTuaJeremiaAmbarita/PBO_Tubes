import random
import pygame
from settings import (
    INITIAL_WIND_STRENGTH,
    INITIAL_WIND_DIRECTION,
    INITIAL_WIND_DURATION,
    INITIAL_WIND_ROUND_START,
    BLUE,
    ORANGE,
    BLACK,
    WIDTH,
)


class Wind:
    def __init__(self):
        self.strength = INITIAL_WIND_STRENGTH
        self.direction = INITIAL_WIND_DIRECTION
        self.duration = INITIAL_WIND_DURATION
        self.round_start = INITIAL_WIND_ROUND_START
        self.direction = random.choice([-1, 1])
        self.duration = random.choice([1, 2])

    def generate(self, current_round_number):
        self.strength = random.uniform(0.1, 0.5)
        self.direction = random.choice([-1, 1])
        self.duration = random.choice([1, 2])
        self.round_start = current_round_number
        print(
            f"DEBUG: Angin baru dihasilkan! Putaran: {current_round_number}, Kekuatan: {self.strength:.2f}, Arah: {'Kanan' if self.direction == 1 else 'Kiri'}, Durasi: {self.duration} putaran."
        )
        print(
            f"DEBUG Wind: Durasi Angin: {self.duration}, Arah Angin: {self.direction}"
        )

    def apply_effect(self, base_speed, shooter_direction):
        if self.direction == shooter_direction:
            return base_speed * (1 + self.strength * 0.25)
        else:
            return max(1, base_speed * (1 - self.strength * 0.25))

    def draw_bar(self, screen, x, y):
        max_width = 100
        width = int(self.strength * max_width)
        bar_rect = pygame.Rect(x - max_width // 2, y, width, 10)
        bar_color = BLUE

        if self.direction == 1:
            bar_color = BLUE
        else:
            bar_color = ORANGE
        pygame.draw.rect(screen, bar_color, bar_rect)
        pygame.draw.rect(
            screen, BLACK, pygame.Rect(x - max_width // 2, y, max_width, 10), 2
        )

        arrow_color = bar_color
        if self.direction == 1:
            arrow_points = [
                (x + width / 2, y + 5),
                (x + width / 2 - 10, y),
                (x + width / 2 - 10, y + 10),
            ]
        else:
            arrow_points = [
                (x - width / 2, y + 5),
                (x - width / 2 + 10, y),
                (x - width / 2 + 10, y + 10),
            ]
        pygame.draw.polygon(screen, arrow_color, arrow_points)


wind = Wind()
