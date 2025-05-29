# config/settings.py

# Ukuran layar
WIDTH = 1200
HEIGHT = 800

# Warna (RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Objek karakter
PLAYER_RADIUS = 5
PLAYER_MAX_HEALTH = 100
ENEMY_RADIUS = 5
ENEMY_MAX_HEALTH = 100

# Pagar
FENCE_WIDTH = 10
FENCE_HEIGHT = 250
fence_x = WIDTH // 2
fence_y = HEIGHT // 2 - FENCE_HEIGHT // 2

# Area tembak (untuk input)
shoot_area = None  # Akan diinisialisasi di main game

# Power-up box
POWERUP_BOX_SIZE = 40
POWERUP_SPACING = 10

# Angin
INITIAL_WIND_STRENGTH = 0.0
INITIAL_WIND_DIRECTION = 1  # 1 = kanan, -1 = kiri
INITIAL_WIND_DURATION = 1  # dalam ronde

# Projectile pemain
PLAYER_PROJECTILE_RADIUS = 5
PLAYER_PROJECTILE_SPEED_BASE = 10
PLAYER_PROJECTILE_MAX_SPEED = 20

# Projectile musuh
ENEMY_PROJECTILE_RADIUS = 5
ENEMY_PROJECTILE_SPEED_MIN = 10
ENEMY_PROJECTILE_SPEED_MAX = 20

gravity = 0.5
player_radius = 20  # Radius untuk deteksi tabrakan pemain
enemy_radius = 20  # Radius untuk deteksi tabrakan musuh
clock = None

# Variabel global untuk angin
wind_strength = 0.0
wind_direction = 0
wind_duration = 0
wind_round_start = 0
round_number = 1

# Objek projectile global (akan diinisialisasi di game_loop)
player_projectile = None
enemy_projectile = None

# Variabel global untuk pengisian daya musuh
# Penting: Inisialisasi di sini agar ada di scope global
e_charge_start = 0
e_charging = False


# Power-up
POWERUPS = [
    {
        "name": "Double Attack",
        "desc": "Attack damage x2 this round",
        "color": (255, 165, 0),  # ORANGE
        "effect": lambda damage: damage * 2,
        "type": "damage",
    },
    {
        "name": "Poison Attack",
        "desc": "Enemy skip next turn if hit and cause knockback",
        "color": (128, 0, 128),  # PURPLE
        "effect": None,
        "type": "poison",
    },
    {
        "name": "Big Projectile",
        "desc": "Bigger projectile and hit area",
        "color": (255, 255, 0),  # YELLOW
        "effect": None,
        "type": "size",
    },
    {
        "name": "Heal",
        "desc": "Heal 30 HP but skip attack",
        "color": (0, 255, 0),  # GREEN
        "effect": lambda player: setattr(
            player, "health", min(player.health + 30, 100)
        ),
        "type": "heal",
    },
]

LEVEL_CONFIGS = {
    1: {
        "powerup_limits": {
            0: -1,
            1: -1,
            2: -1,
            3: -1,
        },  # Level 1: All power-ups unlimited
    },
    2: {
        "powerup_limits": {
            0: 2,
            1: 2,
            2: 2,
            3: 2,
        },  # Level 2: Each power-up can be used 2 times
    },
    3: {
        "powerup_limits": {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
        },  # Level 3: Each power-up can be used 1 time
    },
}
# Power-up box positions akan diatur di main, berdasarkan jumlah power-up

# Lain-lain
FONT_SIZE_TEXT = 30
FONT_SIZE_TITLE = 40
FONT_SIZE_GAME_OVER = 50

# Ketersediaan fitur lain bisa ditambahkan di sini
