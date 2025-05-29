import pygame
from game import *
from game_loop import game_loop  # Import game_loop
from menu import main_menu  # Import the new main_menu function

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CAT vs DOG")  # Judul jendela game

running_app = (
    True  # Loop ini menjaga aplikasi tetap berjalan, memungkinkan kembali ke menu
)
while running_app:

    # Panggil menu utama dan dapatkan level yang dipilih
    chosen_level = main_menu(screen)

    # Jika level dipilih (tombol START ditekan), mulai game loop
    if chosen_level is not None:
        # game_loop mengembalikan True jika semua level selesai, False jika tidak
        # Teruskan gambar projectile pemain dan musuh ke game_loop
        game_result = game_loop(
            screen, chosen_level, player_projectile_img, enemy_projectile_img
        )

        if game_result:
            # Jika semua level selesai, mungkin tampilkan layar "Anda menang" terakhir atau langsung keluar
            print("Semua level selesai! Keluar dari game.")
            running_app = False  # Keluar dari aplikasi setelah semua level selesai
        # Jika game_result adalah False (pemain kalah atau keluar), loop akan terus menampilkan menu utama
    else:
        # Jika main_menu mengembalikan None (pengguna menutup jendela), keluar dari aplikasi
        running_app = False

pygame.quit()
