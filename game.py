# game.py
import pygame
import math
import random
from settings import *


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CAT vs DOG")

player_projectile_img = pygame.image.load("aset/cat/fish_bone.png").convert_alpha()
enemy_projectile_img = pygame.image.load("aset/dog/bone.png").convert_alpha()

# Background
background_img = pygame.image.load("aset/map/beach.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Karakter
player_img = pygame.image.load("aset/cat/idle.png")  # Gambar pemain (kucing)
enemy_img = pygame.image.load("aset/dog/idle.png")  # Gambar musuh (anjing)

# Elemen UI/Game
fence_img = pygame.image.load("aset/map/fence.png")


player_img = pygame.transform.scale(player_img, (150, 150))
enemy_img = pygame.transform.scale(enemy_img, (150, 150))


player_projectile_img = pygame.transform.scale(player_projectile_img, (50, 50))
enemy_projectile_img = pygame.transform.scale(enemy_projectile_img, (50, 50))

fence_img = pygame.transform.scale(fence_img, (FENCE_WIDTH, FENCE_HEIGHT))


powerup_raw_images = {
    "Double Attack": pygame.image.load(
        "aset/powerups/Double_Attack.png"
    ).convert_alpha(),
    "Poison Attack": pygame.image.load("aset/powerups/poison.png").convert_alpha(),
    "Big Projectile": pygame.image.load(
        "aset/powerups/Big_Projectile.png"
    ).convert_alpha(),
    "Heal": pygame.image.load("aset/powerups/heal.png").convert_alpha(),
}

powerup_box_size = POWERUP_BOX_SIZE

resized_powerup_images = {
    name: pygame.transform.scale(img, (powerup_box_size, powerup_box_size))
    for name, img in powerup_raw_images.items()
}

powerup_box_img = pygame.Surface((powerup_box_size, powerup_box_size))
powerup_box_img.fill((200, 200, 200))  #


def draw_player(screen, x, y):
    """Menggambar pemain di layar. Gambar dibalik horizontal."""
    flipped_image = pygame.transform.flip(player_img, True, False)
    screen.blit(
        flipped_image,
        (x - flipped_image.get_width() // 2, y - flipped_image.get_height() // 2),
    )


def draw_enemy(screen, x, y):
    """Menggambar musuh di layar. Gambar dibalik horizontal."""
    flipped_image = pygame.transform.flip(enemy_img, True, False)
    screen.blit(
        flipped_image,
        (x - flipped_image.get_width() // 2, y - flipped_image.get_height() // 2),
    )


def draw_fence(screen, x, y, height):
    """Menggambar pagar di layar."""
    screen.blit(fence_img, (x, y))


def draw_projectile(screen, img, x, y):
    """
    Menggambar projectile menggunakan gambar yang diberikan.
    img: Objek Surface gambar projectile.
    x, y: Koordinat tengah projectile.
    """
    screen.blit(
        img,
        (int(x - img.get_width() // 2), int(y - img.get_height() // 2)),
    )


def draw_background(screen, background_img):
    """Menggambar latar belakang di layar."""
    screen.blit(background_img, (0, 0))


def draw_power_bar(screen, x, y, power):
    """Menggambar bar kekuatan tembakan pemain."""
    max_width = 100
    width = max(0, min(int(power), max_width))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(x - max_width // 2, y, width, 10))
    pygame.draw.rect(
        screen, BLACK, pygame.Rect(x - max_width // 2, y, max_width, 10), 2
    )


def draw_health_bar(screen, x, y, health, max_health):
    """Menggambar bar kesehatan."""
    ratio = max(0, min(health / max_health, 1))
    pygame.draw.rect(
        screen, RED, (x, y, 100, 10)
    )  # Latar belakang bar kesehatan (merah)
    pygame.draw.rect(
        screen, GREEN, (x, y, int(100 * ratio), 10)
    )  # Bar kesehatan aktual (hijau)
    pygame.draw.rect(screen, BLACK, (x, y, 100, 10), 2)  # Bingkai bar kesehatan


def draw_text(screen, text, x, y, size=30, color=BLACK):
    """Menggambar teks di layar."""
    font = pygame.font.Font(None, size)
    render = font.render(text, True, color)
    # Pusatkan teks berdasarkan koordinat x, y
    text_rect = render.get_rect(center=(x, y))
    screen.blit(render, text_rect)
