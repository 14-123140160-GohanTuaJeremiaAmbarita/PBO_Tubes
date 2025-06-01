import random
import pygame  #
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

wind_strength = INITIAL_WIND_STRENGTH
wind_direction = INITIAL_WIND_DIRECTION
wind_duration = INITIAL_WIND_DURATION
wind_round_start = INITIAL_WIND_ROUND_START
wind_direction = random.choice([-1, 1])
wind_duration = random.choice([1, 2])


def generate_wind(current_round_number):
    global wind_strength, wind_direction, wind_duration, wind_round_start
    wind_strength = random.uniform(0.1, 0.5)
    wind_direction = random.choice([-1, 1])
    wind_duration = random.choice([1, 2])
    wind_round_start = current_round_number
    print(
        f"DEBUG: Angin baru dihasilkan! Putaran: {current_round_number}, Kekuatan: {wind_strength:.2f}, Arah: {'Kanan' if wind_direction == 1 else 'Kiri'}, Durasi: {wind_duration} putaran."
    )
    print(f"DEBUG Wind: Durasi Angin: {wind_duration}, Arah Angin: {wind_direction}")


def apply_wind_effect(base_speed, shooter_direction):
    if wind_direction == shooter_direction:
        return base_speed * (1 + wind_strength * 0.25)
    else:
        return max(1, base_speed * (1 - wind_strength * 0.25))


def draw_wind_bar(screen, x, y, strength, direction):
    max_width = 100
    width = int(strength * max_width)
    bar_rect = pygame.Rect(x - max_width // 2, y, width, 10)
    bar_color = BLUE

    if direction == 1:
        bar_color = BLUE
    else:
        bar_color = ORANGE
    pygame.draw.rect(screen, bar_color, bar_rect)
    pygame.draw.rect(
        screen, BLACK, pygame.Rect(x - max_width // 2, y, max_width, 10), 2
    )

    arrow_color = bar_color
    if direction == 1:
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
