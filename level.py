import pygame
from settings import *


class Level:
    def __init__(self, level_number, powerup_limits_per_type):
        self.level_number = level_number
        self.background_img = self._load_background()
        self.powerup_limits_per_type = self._get_powerup_limits_per_type()
        self.enemy_accuracy_boost = self._get_enemy_accuracy_boost()
        self.enemy_power_boost = self._get_enemy_power_boost()
        self.time_limit = self._get_time_limit()  # In seconds, None if no limit

    def _load_background(self):
        # Load and scale background based on level number
        try:
            if self.level_number == 1:
                img = pygame.image.load("aset/map/mountain.png")
            elif self.level_number == 2:
                img = pygame.image.load("aset/map/house.png")
            elif self.level_number == 3:
                img = pygame.image.load("aset/map/beach.png")
            else:
                img = pygame.image.load("aset/default.png")  # Fallback for other levels
            # Scale to your game's WIDTH and HEIGHT (assuming these are global or passed)
            return pygame.transform.scale(img, (WIDTH, HEIGHT))
        except pygame.error as e:
            print(f"Error loading background for level {self.level_number}: {e}")
            # Fallback to a plain color if image fails to load
            default_surface = pygame.Surface((800, 600))
            default_surface.fill((100, 100, 100))  # Grey color
            return default_surface

    def _get_powerup_limits_per_type(self):
        """
        Mengembalikan batas penggunaan power-up untuk setiap jenis per level
        berdasarkan konfigurasi di settings.py, memetakan indeks ke nama.
        """
        # Dapatkan konfigurasi batas power-up untuk level saat ini dari LEVEL_CONFIGS
        limits_from_settings_by_index = LEVEL.get(self.level_number, {}).get(
            "powerup_limits", {}
        )

        # Buat dictionary baru dengan nama power-up sebagai kunci
        # dan batas penggunaan sebagai nilai, berdasarkan urutan POWERUPS.
        mapped_limits = {}
        for index, limit in limits_from_settings_by_index.items():
            # Pastikan indeks valid dalam daftar POWERUPS
            if 0 <= index < len(POWERUPS):
                powerup_name = POWERUPS[index]["name"]
                mapped_limits[powerup_name] = limit
        return mapped_limits

    def _get_enemy_accuracy_boost(self):
        """Mengembalikan peningkatan akurasi musuh berdasarkan konfigurasi level dari settings.py."""
        return LEVEL.get(self.level_number, {}).get("enemy_accuracy_boost", 0)

    def _get_enemy_power_boost(self):
        """Mengembalikan peningkatan kekuatan musuh berdasarkan konfigurasi level dari settings.py."""
        return LEVEL.get(self.level_number, {}).get("enemy_power_boost", 0)

    def _get_time_limit(self):
        """Mengembalikan batas waktu level berdasarkan konfigurasi level dari settings.py."""
        return LEVEL.get(self.level_number, {}).get("time_limit", None)
        mapped_limits = {}
