import pygame
from Game.game import *
from Game.game_loop import *
from menu import main_menu

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

running_app = True
while running_app:

    chosen_level = main_menu(screen)

    if chosen_level is not None:
        game_instance = GameLoop(
            screen, chosen_level, player_projectile_img, enemy_projectile_img
        )
        game_result = game_instance.run()

        if game_result == "quit_to_menu":
            pass
        elif game_result == "game_over_lose":
            running_app = False
        elif game_result == "all_levels_completed":
            running_app = False
        else:
            running_app = False
    else:
        running_app = False

pygame.quit()
