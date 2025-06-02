import pygame
from settings import *
from Game.game import draw_text, load_and_scale_image


class Level:
    def __init__(self, level_number, initial_powerup_limits_dict):
        self.level_number = level_number
        self.background_img = self._load_background()
        self.powerup_limits_per_type = initial_powerup_limits_dict
        self.enemy_accuracy_boost = self._get_enemy_accuracy_boost()
        self.enemy_power_boost = self._get_enemy_power_boost()
        self.time_limit = self._get_time_limit()

        self.fence_x = self._get_fence_x()
        self.fence_y = self._get_fence_y()
        self.fence_height = self._get_fence_height()
        self.fence_width = self._get_fence_width()

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
            print(f"Error loading background for level {self.level_number}: {e}")
            default_surface = pygame.Surface((WIDTH, HEIGHT))
            default_surface.fill((100, 100, 100))
            return default_surface

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

    def display_level_win_message(self, screen):
        message = f"Level {self.level_number} Selesai!"
        draw_text(screen, message, WIDTH // 2, HEIGHT // 2 - 50, 50, GREEN)
        pygame.display.update()
        pygame.time.wait(2000)
        print(f"DEBUG: Pesan kemenangan level {self.level_number} ditampilkan.")

    def display_all_levels_completed_message(self, screen):
        message = "Selamat! Anda Menyelesaikan Semua Level!"
        draw_text(screen, message, WIDTH // 2, HEIGHT // 2 - 50, 40, BLUE)
        pygame.display.update()
        pygame.time.wait(3000)
        print("DEBUG: Pesan semua level selesai ditampilkan.")
