import pygame
import math
import random
from settings import *
from abc import ABC, abstractmethod  # Untuk Abstraksi

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CAT vs DOG")

try:
    hit_sound = pygame.mixer.Sound("aset/audio/hit.wav")
    miss_sound_player = pygame.mixer.Sound("aset/audio/dog.mp3")
    miss_sound_enemy = pygame.mixer.Sound("aset/audio/cat.ogg")
    pygame.mixer.music.load("aset/audio/backsound.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"ERROR: Gagal memuat audio: {e}")


# Fungsi pembantu untuk memuat gambar dengan penanganan error
def load_and_scale_image(path, size, alpha=True):
    try:
        img = pygame.image.load(path)
        if alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
        return pygame.transform.scale(img, size)
    except pygame.error as e:
        print(f"ERROR: Gagal memuat gambar dari {path}: {e}")
        return pygame.Surface(size, pygame.SRCALPHA if alpha else 0)


# --- Kelas Abstrak Character (Abstraksi & Pewarisan) ---
class Character(ABC, pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        idle_image_path,
        hit_image_path,
        edge_image_path,
        size,
        max_health,
        flipped_horizontally=False,
    ):
        super().__init__()
        self._max_health = max_health  # Enkapsulasi
        self._current_health = max_health  # Enkapsulasi
        self._x = x  # Enkapsulasi
        self._y = y  # Enkapsulasi
        self._state = "idle"  # Enkapsulasi
        self._state_timer = 0  # Enkapsulasi
        self._flipped_horizontally = flipped_horizontally  # Enkapsulasi

        # Pemuatan dan scaling gambar untuk semua state
        self._idle_image = load_and_scale_image(idle_image_path, size)
        self._hit_image = load_and_scale_image(hit_image_path, size)
        self._edge_image = load_and_scale_image(edge_image_path, size)

        self.image = self._idle_image
        self.rect = self.image.get_rect(center=(int(self._x), int(self._y)))

    @property
    def health(self):
        return self._current_health

    @health.setter
    def health(self, value):
        self._current_health = max(0, min(value, self._max_health))

    # Properti untuk enkapsulasi posisi
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.rect.centerx = int(self._x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.rect.centery = int(self._y)

    # Properti untuk enkapsulasi state
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state != new_state:  # Hanya update jika state berubah
            self._state = new_state
            self._state_timer = pygame.time.get_ticks()

    @abstractmethod
    def draw(self, screen):  # Metode abstrak (Polimorfisme)
        pass

    def update_image_by_state(self, current_time, hit_duration, miss_duration):
        """Memperbarui gambar karakter berdasarkan state dan timer."""
        if self._state == "hit" and current_time - self._state_timer >= hit_duration:
            self.state = "idle"  # Menggunakan setter untuk reset state
        elif (
            self._state == "edge" and current_time - self._state_timer >= miss_duration
        ):
            self.state = "idle"  # Menggunakan setter untuk reset state

        if self._state == "hit":
            self.image = self._hit_image
        elif self._state == "edge":
            self.image = self._edge_image
        else:
            self.image = self._idle_image

        # Terapkan flip secara konsisten di sini
        self.image = pygame.transform.flip(
            self.image, self._flipped_horizontally, False
        )


class Player(Character):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            "aset/cat/idle.png",
            "aset/cat/hit.png",
            "aset/cat/edge.png",
            PLAYER_CHAR_SIZE,
            PLAYER_MAX_HEALTH,
            flipped_horizontally=True,
        )
        self.radius = PLAYER_RADIUS

    def draw(self, screen):
        self.update_image_by_state(pygame.time.get_ticks(), HIT_DURATION, MISS_DURATION)
        screen.blit(self.image, self.rect)


class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            "aset/dog/idle.png",
            "aset/dog/hit.png",
            "aset/dog/edge.png",
            PLAYER_CHAR_SIZE,
            ENEMY_MAX_HEALTH,
            flipped_horizontally=True,
        )
        self.radius = ENEMY_RADIUS

    def draw(self, screen):
        self.update_image_by_state(pygame.time.get_ticks(), HIT_DURATION, MISS_DURATION)
        screen.blit(self.image, self.rect)


# --- Pemuatan Gambar Global (yang tidak terkait langsung dengan Character) ---
player_projectile_img = load_and_scale_image("aset/cat/fish_bone.png", (50, 50))
enemy_projectile_img = load_and_scale_image("aset/dog/bone.png", (50, 50))
background_img = load_and_scale_image(
    "aset/map/beach.png", (WIDTH, HEIGHT), alpha=False
)
fence_img = load_and_scale_image("aset/map/fence.png", (FENCE_WIDTH, FENCE_HEIGHT))

powerup_raw_images = {
    "Double Attack": load_and_scale_image(
        "aset/powerups/Double_Attack.png", (POWERUP_BOX_SIZE, POWERUP_BOX_SIZE)
    ),
    "Poison Attack": load_and_scale_image(
        "aset/powerups/poison.png", (POWERUP_BOX_SIZE, POWERUP_BOX_SIZE)
    ),
    "Big Projectile": load_and_scale_image(
        "aset/powerups/Big_Projectile.png", (POWERUP_BOX_SIZE, POWERUP_BOX_SIZE)
    ),
    "Heal": load_and_scale_image(
        "aset/powerups/heal.png", (POWERUP_BOX_SIZE, POWERUP_BOX_SIZE)
    ),
}
resized_powerup_images = powerup_raw_images  # Sudah di-scale oleh load_and_scale_image

powerup_box_img = pygame.Surface((POWERUP_BOX_SIZE, POWERUP_BOX_SIZE))
powerup_box_img.fill((200, 200, 200))


# --- Fungsi Gambar Umum (tidak terkait langsung dengan instance Character) ---
def draw_power_bar(screen, x, y, power):
    max_width = 100
    width = max(0, min(int(power), max_width))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(x - max_width // 2, y, width, 10))
    pygame.draw.rect(
        screen, BLACK, pygame.Rect(x - max_width // 2, y, max_width, 10), 2
    )


def draw_health_bar(screen, x, y, health, max_health):
    ratio = max(0, min(health / max_health, 1))
    pygame.draw.rect(screen, RED, (x, y, 100, 10))
    pygame.draw.rect(screen, GREEN, (x, y, int(100 * ratio), 10))
    pygame.draw.rect(screen, BLACK, (x, y, 100, 10), 2)


def draw_text(screen, text, x, y, size=30, color=BLACK):
    font = pygame.font.Font(None, size)
    render = font.render(text, True, color)
    text_rect = render.get_rect(center=(x, y))
    screen.blit(render, text_rect)
