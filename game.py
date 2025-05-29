import pygame
import math
import random
from settings import *  # Asumsi settings.py berisi WIDTH, HEIGHT, dan warna

# Konfigurasi dasar
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Warfare")  # Judul jendela game

# --- Pemuatan Gambar ---
# Projectile pemain (tulang anjing)
player_projectile_img = pygame.image.load("aset/dog/bone.png").convert_alpha()
# Projectile musuh (Pastikan Anda memiliki file "aset/cat/fish_bone.png")
enemy_projectile_img = pygame.image.load("aset/cat/fish_bone.png").convert_alpha()


# Karakter
player_img = pygame.image.load(
    "aset/dog/idle.png"
)  # Sekarang memuat 'cat_hit' untuk player
enemy_img = pygame.image.load("aset/cat/idle.png")  # Sekarang memuat 'cat' untuk enemy

# Elemen UI/Game
powerup_box_img = pygame.image.load("aset/dog/hit.png")
fence_img = pygame.image.load("aset/map/fence.png")


# --- Resize Gambar ---
player_img = pygame.transform.scale(player_img, (150, 150))
enemy_img = pygame.transform.scale(enemy_img, (150, 150))
powerup_box_img = pygame.transform.scale(powerup_box_img, (40, 40))
# Menyesuaikan ukuran gambar projectile
player_projectile_img = pygame.transform.scale(player_projectile_img, (50, 50))
enemy_projectile_img = pygame.transform.scale(enemy_projectile_img, (50, 50))

fence_width, fence_height = 100, 400
fence_img = pygame.transform.scale(fence_img, (fence_width, fence_height))


# --- Fungsi Gambar ---
def draw_player(screen, x, y):
    """Menggambar pemain di layar."""
    screen.blit(
        player_img,
        (x - player_img.get_width() // 2, y - player_img.get_height() // 2),
    )


def draw_enemy(screen, x, y):
    """Menggambar musuh di layar."""
    screen.blit(
        enemy_img, (x - enemy_img.get_width() // 2, y - enemy_img.get_height() // 2)
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
    # Menggambar gambar di tengah koordinat x, y
    screen.blit(
        img,
        (int(x - img.get_width() // 2), int(y - img.get_height() // 2)),
    )


def draw_powerup_box(screen, x, y):
    """Menggambar kotak power-up di layar."""
    screen.blit(
        powerup_box_img,
        (x - powerup_box_img.get_width() // 2, y - powerup_box_img.get_height() // 2),
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
