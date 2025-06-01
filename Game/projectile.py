import pygame
from settings import GRAVITY

player_projectile = None
enemy_projectile = None


class Projectile:
    def __init__(self, x, y, vel_x, vel_y, image, radius=None):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.image = image
        self.radius = radius if radius is not None else image.get_width() // 2
        self.active = False

    def update(self):
        if self.active:
            self.vel_y += GRAVITY
            self.x += self.vel_x
            self.y += self.vel_y

    def draw(self, screen):
        if self.active:
            screen.blit(
                self.image,
                (
                    int(self.x - self.image.get_width() // 2),
                    int(self.y - self.image.get_height() // 2),
                ),
            )

    def deactivate(self):
        self.active = False
        self.x = -100
        self.y = -100
        self.vel_x = 0
        self.vel_y = 0


player_projectile = None
enemy_projectile = None


def reset_player_projectile():
    """Menonaktifkan projectile pemain."""
    global player_projectile
    if player_projectile:
        player_projectile.deactivate()


def reset_enemy_projectile():
    """Menonaktifkan projectile musuh."""
    global enemy_projectile
    if enemy_projectile:
        enemy_projectile.deactivate()
