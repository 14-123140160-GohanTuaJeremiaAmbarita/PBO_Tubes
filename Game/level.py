import pygame
from settings import LEVEL, WIDTH, HEIGHT, POWERUPS
from Game.game import load_and_scale_image


class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.background_img = self._load_background()
        self.powerup_limits_per_type = self._get_powerup_limits_per_type()
        self.enemy_accuracy_boost = self._get_enemy_accuracy_boost()
        self.enemy_power_boost = self._get_enemy_power_boost()
        self.time_limit = self._get_time_limit()

        self.fence_x = self._get_fence_x()
        self.fence_y = self._get_fence_y()
        self.fence_height = self._get_fence_height()
        self.fence_width = self._get_fence_width()
        self.fence_img = (
            self._load_fence_image()
        )  # Memastikan atribut ini diinisialisasi

        self.player_x = self._get_player_x()
        self.player_y = self._get_player_y()
        self.enemy_x = self._get_enemy_x()
        self.enemy_y = self._get_enemy_y()

    def _load_background(self):
        try:
            if self.level_number == 1:
                img = pygame.image.load("aset/map/beach.png")
            elif self.level_number == 2:
                img = pygame.image.load("aset/map/mountain.png")
            elif self.level_number == 3:
                img = pygame.image.load("aset/map/house.png")
            else:
                img = pygame.image.load("aset/default.png")
            return pygame.transform.scale(img, (WIDTH, HEIGHT))
        except pygame.error as e:
            print(
                f"ERROR: Gagal memuat latar belakang untuk level {self.level_number}: {e}"
            )
            default_surface = pygame.Surface((WIDTH, HEIGHT))
            default_surface.fill((100, 100, 100))
            return default_surface

    def _load_fence_image(self):
        try:
            fence_path = "aset/map/fence.png"
            scaled_img = load_and_scale_image(
                fence_path, (self.fence_width, self.fence_height)
            )
            # print(f"DEBUG: _load_fence_image mengembalikan gambar dengan ukuran: {scaled_img.get_size() if scaled_img else 'None'}")
            return scaled_img
        except pygame.error as e:
            print(
                f"ERROR: Gagal memuat gambar pagar untuk level {self.level_number}: {e}"
            )
            default_surface = pygame.Surface(
                (self.fence_width, self.fence_height), pygame.SRCALPHA
            )
            default_surface.fill((150, 150, 150, 128))
            return default_surface

    def _get_powerup_limits_per_type(self):
        limits_from_settings_by_index = LEVEL.get(self.level_number, {}).get(
            "powerup_limits", {}
        )
        mapped_limits = {}
        for index, limit in limits_from_settings_by_index.items():
            if 0 <= index < len(POWERUPS):
                powerup_name = POWERUPS[index]["name"]
                mapped_limits[powerup_name] = limit
        return mapped_limits

    def _get_enemy_accuracy_boost(self):
        return LEVEL.get(self.level_number, {}).get("enemy_accuracy_boost", 0)

    def _get_enemy_power_boost(self):
        return LEVEL.get(self.level_number, {}).get("enemy_power_boost", 0)

    def _get_time_limit(self):
        return LEVEL.get(self.level_number, {}).get("time_limit", None)

    def _get_fence_x(self):
        return LEVEL.get(self.level_number, {}).get("fence_x", 550)

    def _get_fence_y(self):
        return LEVEL.get(self.level_number, {}).get("fence_y", 400)

    def _get_fence_height(self):
        return LEVEL.get(self.level_number, {}).get("fence_height", 400)

    def _get_fence_width(self):
        return LEVEL.get(self.level_number, {}).get("fence_width", 150)

    def _get_player_x(self):
        return LEVEL.get(self.level_number, {}).get("player_x", 100)

    def _get_player_y(self):
        return LEVEL.get(self.level_number, {}).get("player_y", 525)

    def _get_enemy_x(self):
        return LEVEL.get(self.level_number, {}).get("enemy_x", 950)

    def _get_enemy_y(self):
        return LEVEL.get(self.level_number, {}).get("enemy_y", 575)
