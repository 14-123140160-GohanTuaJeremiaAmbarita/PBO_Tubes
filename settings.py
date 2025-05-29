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
PLAYER_RADIUS = 20
PLAYER_MAX_HEALTH = 100
ENEMY_RADIUS = 20
ENEMY_MAX_HEALTH = 100

# Pagar
FENCE_WIDTH = 100
FENCE_HEIGHT = 400
FENCE_X = 550
FENCE_Y = 400

# Area tembak (untuk input)
shoot_area = None  # Akan diinisialisasi di main game

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

gravity = 0.5  # Radius untuk deteksi tabrakan musuh
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


POWERUP_BOX_SIZE = 80
POWERUP_SPACING = 10
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

LEVEL = {
    1: {
        "powerup_limits": {
            0: -1,  # Power-up di index 0 (Double Attack) - Tidak terbatas
            1: -1,  # Power-up di index 1 (Poison Attack) - Tidak terbatas
            2: -1,  # Power-up di index 2 (Big Projectile) - Tidak terbatas
            3: -1,  # Power-up di index 3 (Heal) - Tidak terbatas
        },
        "enemy_accuracy_boost": 0,  # Tidak ada peningkatan akurasi musuh
        "enemy_power_boost": 0,  # Tidak ada peningkatan kekuatan musuh
        "time_limit": None,  # Tidak ada batas waktu
    },
    2: {
        "powerup_limits": {
            0: 2,  # Power-up di index 0 - 2 kali penggunaan
            1: 2,  # Power-up di index 1 - 2 kali penggunaan
            2: 2,  # Power-up di index 2 - 2 kali penggunaan
            3: 2,  # Power-up di index 3 - 2 kali penggunaan
        },
        "enemy_accuracy_boost": 0.15,  # Peningkatan akurasi musuh moderat
        "enemy_power_boost": 5,  # +5 kerusakan untuk musuh
        "time_limit": None,  # Tidak ada batas waktu
    },
    3: {
        "powerup_limits": {
            0: 1,  # Power-up di index 0 - 1 kali penggunaan
            1: 1,  # Power-up di index 1 - 1 kali penggunaan
            2: 1,  # Power-up di index 2 - 1 kali penggunaan
            3: 1,  # Power-up di index 3 - 1 kali penggunaan
        },
        "enemy_accuracy_boost": 0.30,  # Peningkatan akurasi musuh signifikan
        "enemy_power_boost": 10,  # +10 kerusakan untuk musuh
        "time_limit": 100,  # Batas waktu 100 detik
    },
}
# Power-up box positions akan diatur di main, berdasarkan jumlah power-up

# Lain-lain
FONT_SIZE_TEXT = 30
FONT_SIZE_TITLE = 40
FONT_SIZE_GAME_OVER = 50

# Ketersediaan fitur lain bisa ditambahkan di sini
