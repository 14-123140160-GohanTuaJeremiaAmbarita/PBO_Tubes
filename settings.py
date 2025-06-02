WIDTH = 1200
HEIGHT = 800
GRAVITY = 0.5

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

PLAYER_CHAR_SIZE = (150, 150)
PLAYER_RADIUS = 30
PLAYER_MAX_HEALTH = 100
ENEMY_RADIUS = 30
ENEMY_MAX_HEALTH = 100
BASE_DAMAGE = 100

MIN_PLAYER_BASE_SPEED = 10
MAX_PLAYER_CHARGE_TIME = 2000
MIN_ENEMY_BASE_SPEED = 10
MAX_PROJECTILE_SPEED = 30
FENCE_WIDTH = 150
FENCE_HEIGHT = 400
FENCE_X = 550
FENCE_Y = 400

shoot_area = None

INITIAL_WIND_STRENGTH = 0.0
INITIAL_WIND_DIRECTION = 1
INITIAL_WIND_DURATION = 1
INITIAL_WIND_ROUND_START = 0

clock = None

wind_strength = 0.0
wind_direction = 0
wind_duration = 0
wind_round_start = 0
round_number = 1

player_projectile = None
enemy_projectile = None

e_charge_start = 0
e_charging = False

HIT_DURATION = 1000
MISS_DURATION = 1000


POWERUP_BOX_SIZE = 80
POWERUP_SPACING = 10
POWERUPS = [
    {
        "name": "Double Attack",
        "desc": "Attack damage x2 this round",
        "color": (255, 165, 0),
        "effect": lambda damage: damage * 2,
        "type": "damage",
    },
    {
        "name": "Poison Attack",
        "desc": "Enemy skip next turn if hit and cause knockback",
        "color": (128, 0, 128),
        "effect": None,
        "type": "poison",
    },
    {
        "name": "Big Projectile",
        "desc": "Bigger projectile and hit area",
        "color": (255, 255, 0),
        "effect": None,
        "type": "size",
    },
    {
        "name": "Heal",
        "desc": "Heal 30 HP but skip attack",
        "color": (0, 255, 0),
        "effect": lambda player: setattr(
            player, "health", min(player.health + 30, 100)
        ),
        "type": "heal",
    },
]

LEVEL = {
    1: {
        "powerup_limits": {
            0: -1,
            1: -1,
            2: -1,
            3: -1,
        },
        "enemy_accuracy_boost": 0,
        "enemy_power_boost": 5,
        "time_limit": None,
        "player_x": WIDTH // 6,
        "player_y": 575,
        "enemy_x": 1100,
        "enemy_y": 575,
        "fence_height": FENCE_HEIGHT,
        "fence_width": FENCE_WIDTH,
        "fence_x": FENCE_X,
        "fence_y": FENCE_Y,
    },
    2: {
        "powerup_limits": {
            0: 2,
            1: 2,
            2: 2,
            3: 2,
        },
        "enemy_accuracy_boost": 0.15,
        "enemy_power_boost": 10,
        "time_limit": None,
        "player_x": 150,
        "player_y": 525,
        "enemy_x": WIDTH - 100,
        "enemy_y": 525,
        "fence_height": FENCE_HEIGHT // 2 - 50,
        "fence_width": FENCE_WIDTH - 100,
        "fence_x": FENCE_X,
        "fence_y": FENCE_Y,
    },
    3: {
        "powerup_limits": {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
        },
        "enemy_accuracy_boost": 0.30,
        "enemy_power_boost": 15,
        "time_limit": 100,
        "player_x": 150,
        "player_y": 575,
        "enemy_x": 1100,
        "enemy_y": 575,
        "fence_height": FENCE_HEIGHT,
        "fence_width": FENCE_WIDTH,
        "fence_x": FENCE_X,
        "fence_y": FENCE_Y,
    },
}
FONT_SIZE_TEXT = 30
FONT_SIZE_TITLE = 40
FONT_SIZE_GAME_OVER = 50
