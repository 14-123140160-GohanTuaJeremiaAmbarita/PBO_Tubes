import random
import pygame  # Diperlukan untuk pygame.Rect dan warna
from settings import (
    INITIAL_WIND_STRENGTH,
    INITIAL_WIND_DIRECTION,
    INITIAL_WIND_DURATION,
    INITIAL_WIND_ROUND_START,
    BLUE,  # Untuk warna bar angin
    ORANGE,  # Untuk warna bar angin
    BLACK,  # Diperlukan untuk menggambar bar
    WIDTH,  # Diperlukan untuk posisi bar angin
)


# Variabel global untuk angin, diinisialisasi dengan nilai awal dari settings.py
wind_strength = INITIAL_WIND_STRENGTH
wind_direction = INITIAL_WIND_DIRECTION
wind_duration = INITIAL_WIND_DURATION
wind_round_start = INITIAL_WIND_ROUND_START


def generate_wind(current_round_number):
    """Menghasilkan kekuatan, arah, dan durasi angin acak."""
    global wind_strength, wind_direction, wind_duration, wind_round_start
    wind_strength = random.uniform(0.1, 0.6)
    wind_direction = random.choice([-1, 1])  # -1 untuk kiri, 1 untuk kanan
    wind_duration = random.choice([1, 2])  # Angin bertahan 1 atau 2 putaran
    wind_round_start = current_round_number  # Catat putaran saat angin dihasilkan


def apply_wind_effect(base_speed, shooter_direction):
    """Menyesuaikan kecepatan projectile berdasarkan efek angin."""
    if wind_direction == shooter_direction:
        return base_speed * (1 + wind_strength * 0.25)
    else:
        return max(1, base_speed * (1 - wind_strength * 0.25))


def draw_wind_bar(screen, x, y, strength, direction):
    """Menggambar indikator kekuatan dan arah angin."""
    max_width = 100
    width = int(strength * max_width)
    bar_rect = pygame.Rect(x - max_width // 2, y, width, 10)
    bar_color = BLUE  # Warna default

    if direction == 1:  # Angin ke kanan (arah pemain)
        bar_color = BLUE
    else:  # Angin ke kiri (berlawanan arah pemain)
        bar_color = ORANGE

    # Gambar bar angin dengan warna yang sesuai
    pygame.draw.rect(screen, bar_color, bar_rect)
    pygame.draw.rect(
        screen, BLACK, pygame.Rect(x - max_width // 2, y, max_width, 10), 2
    )

    # Gambar panah
    arrow_color = bar_color  # Warna panah sama dengan bar
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
