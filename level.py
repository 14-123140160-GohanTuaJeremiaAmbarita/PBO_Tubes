import pygame
from settings import HEIGHT, WIDTH


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
        """Return the power-up limits for each type per level as a dictionary."""
        # Example: Each type of power-up will have its limit
        if self.level_number == 1:
            return {
                "Double Attack": -1,  # Unlimited uses
                "Poison Attack": 3,  # 3 uses
                "Big Projectile": 2,  # 2 uses
                "Heal": 1,  # 1 use
            }
        elif self.level_number == 2:
            return {
                "Double Attack": 2,  # 2 uses
                "Poison Attack": 1,  # 1 use
                "Big Projectile": 1,  # 1 use
                "Heal": 1,  # 1 use
            }
        elif self.level_number == 3:
            return {
                "Double Attack": 1,  # 1 use
                "Poison Attack": 1,  # 1 use
                "Big Projectile": 1,  # 1 use
                "Heal": 1,  # 1 use
            }
        return {}  # Default empty dictionary for other levels

    def _get_enemy_accuracy_boost(self):
        if self.level_number == 1:
            return 0  # No boost
        elif self.level_number == 2:
            return 0.15  # Moderate accuracy increase
        elif self.level_number == 3:
            return 0.30  # Significant accuracy increase
        return 0

    def _get_enemy_power_boost(self):
        if self.level_number == 1:
            return 0  # No boost
        elif self.level_number == 2:
            return 5  # +5 damage
        elif self.level_number == 3:
            return 10  # +10 damage
        return 0

    def _get_time_limit(self):
        if self.level_number == 3:
            return 100  # 100 seconds
        return None  # No time limit for other levels
