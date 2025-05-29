import pygame
import math
import random
from settings import *
from game import *
from level import Level
from projectile import Projectile

gravity = 0.5
player_radius = PLAYER_RADIUS
enemy_radius = ENEMY_RADIUS
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


def generate_wind():
    global wind_strength, wind_direction, wind_duration, wind_round_start
    wind_strength = random.uniform(0.1, 0.6)
    wind_direction = random.choice([-1, 1])
    wind_duration = random.choice([1, 2])
    wind_round_start = round_number


def apply_wind_effect(base_speed, shooter_direction):
    if wind_direction == shooter_direction:
        return base_speed * (1 + wind_strength * 0.35)
    else:
        return max(1, base_speed * (1 - wind_strength * 0.35))


def reset_player_projectile():
    global player_projectile
    if player_projectile:
        player_projectile.deactivate()


def reset_enemy_projectile():
    global enemy_projectile
    if enemy_projectile:
        enemy_projectile.deactivate()


def check_collision(px, py, ex, ey, er):
    distance_squared = (px - ex) ** 2 + (py - ey) ** 2
    return distance_squared <= er**2


def check_fence_collision(px, py, fx, fy, fheight):
    fence_width = 40
    return fx < px < fx + fence_width and fy < py < fy + fheight


def game_loop(
    screen, initial_level_number, player_projectile_img, enemy_projectile_img
):
    global clock, round_number
    global player_projectile, enemy_projectile
    global power
    global e_charge_start, e_charging

    current_level_number = initial_level_number
    initial_powerup_limits_dict = LEVEL[current_level_number]["powerup_limits"]
    current_level = Level(current_level_number, initial_powerup_limits_dict)

    selected_powerup = None
    powerup_used_this_round = False
    powerup_uses_counts = {i: 0 for i in range(len(POWERUPS))}

    clock = pygame.time.Clock()

    player_x, player_y = WIDTH // 6, 525
    enemy_x, enemy_y = WIDTH - 100, 525
    fence_x, fence_y = FENCE_X, FENCE_Y
    fence_height = FENCE_HEIGHT

    player_health = 100
    enemy_health = 100

    round_number = 1
    generate_wind()

    player_projectile = Projectile(-100, -100, 0, 0, player_projectile_img)
    enemy_projectile = Projectile(-100, -100, 0, 0, enemy_projectile_img)

    p_is_charging = False
    p_shoot_start_time = 0
    p_projectile_angle = math.pi / 4
    power = 0

    e_charge_start = 0
    e_charging = False
    enemy_charge_duration = 1500

    player_turn = True
    enemy_knockback = False
    enemy_skip_turn = False

    level_start_time = pygame.time.get_ticks()
    time_remaining = current_level.time_limit

    powerup_box_size = POWERUP_BOX_SIZE
    start_x = player_x - ((powerup_box_size + 10) * len(POWERUPS) - 10) // 2
    start_y = fence_y - 200
    powerup_boxes = []
    for i in range(len(POWERUPS)):
        rect = pygame.Rect(
            start_x + i * (powerup_box_size + 10),
            start_y,
            powerup_box_size,
            powerup_box_size,
        )
        powerup_boxes.append((rect, i))

    shoot_area = pygame.Rect(0, HEIGHT - 150, WIDTH, 150)

    running = True
    while running:
        screen.fill(WHITE)
        draw_background(screen, current_level.background_img)

        if current_level.time_limit is not None:
            elapsed_time = (pygame.time.get_ticks() - level_start_time) / 1000
            time_remaining = max(0, current_level.time_limit - elapsed_time)
            if time_remaining <= 0:
                draw_text(
                    screen,
                    "Waktu Habis! Musuh Menang",
                    WIDTH // 2,
                    HEIGHT // 2 - 50,
                    50,
                    RED,
                )
                pygame.display.update()
                pygame.time.wait(3000)
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn:
                    for rect_item in powerup_boxes:
                        rect = rect_item[0]
                        i = rect_item[1]
                        if rect.collidepoint(event.pos) and not powerup_used_this_round:
                            powerup_name = POWERUPS[i]["name"]
                            current_powerup_limit = (
                                current_level.powerup_limits_per_type.get(
                                    powerup_name, -1
                                )
                            )
                            current_powerup_uses = powerup_uses_counts[i]

                            if (
                                current_powerup_limit == -1
                                or current_powerup_uses < current_powerup_limit
                            ):
                                selected_powerup = i
                                powerup_used_this_round = True
                                powerup_uses_counts[i] += 1

                                if POWERUPS[i]["type"] == "heal":
                                    player_health = min(100, player_health + 30)
                                    player_turn = False
                                    round_number += 1
                                    selected_powerup = None
                                    e_charge_start = pygame.time.get_ticks()
                                    e_charging = True
                                break

                    if shoot_area.collidepoint(event.pos):
                        if not player_projectile.active and not p_is_charging:
                            p_shoot_start_time = pygame.time.get_ticks()
                            p_is_charging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if player_turn and p_is_charging:
                    hold_time = pygame.time.get_ticks() - p_shoot_start_time
                    power = min(150, hold_time // 10)
                    base_speed = min(20 + hold_time / 100, 20)
                    p_projectile_speed = apply_wind_effect(base_speed, 1)

                    proj_image_for_player = player_projectile_img
                    proj_radius_for_player = player_projectile_img.get_width() // 2

                    if (
                        selected_powerup is not None
                        and POWERUPS[selected_powerup]["type"] == "size"
                    ):
                        proj_image_for_player = pygame.transform.scale(
                            player_projectile_img,
                            (
                                player_projectile_img.get_width() * 2,
                                player_projectile_img.get_height() * 2,
                            ),
                        )
                        proj_radius_for_player *= 2

                    player_projectile.x = player_x
                    player_projectile.y = player_y
                    player_projectile.vel_x = p_projectile_speed * math.cos(
                        p_projectile_angle
                    )
                    player_projectile.vel_y = -p_projectile_speed * math.sin(
                        p_projectile_angle
                    )
                    player_projectile.image = proj_image_for_player
                    player_projectile.radius = proj_radius_for_player
                    player_projectile.active = True

                    p_is_charging = False

        if p_is_charging:
            hold_time = pygame.time.get_ticks() - p_shoot_start_time
            power = min(100, hold_time // 10)

        if current_level_number > 1:
            draw_fence(screen, fence_x, fence_y, fence_height)
        draw_player(screen, player_x, player_y)
        draw_enemy(screen, enemy_x, enemy_y)

        if player_projectile.active:
            player_projectile.update()
            player_projectile.draw(screen)

            if check_fence_collision(
                player_projectile.x, player_projectile.y, fence_x, fence_y, fence_height
            ):
                reset_player_projectile()
                player_turn = False
                round_number += 1
                selected_powerup = None
                powerup_used_this_round = False
                e_charge_start = pygame.time.get_ticks()
                e_charging = True
            elif check_collision(
                player_projectile.x,
                player_projectile.y,
                enemy_x,
                enemy_y,
                enemy_radius + player_projectile.radius,
            ):
                damage = 10
                if (
                    selected_powerup is not None
                    and POWERUPS[selected_powerup]["type"] == "damage"
                ):
                    damage = POWERUPS[selected_powerup]["effect"](damage)

                if (
                    selected_powerup is not None
                    and POWERUPS[selected_powerup]["type"] == "poison"
                ):
                    enemy_skip_turn = True
                    enemy_knockback = True

                enemy_health -= damage
                reset_player_projectile()
                player_turn = False
                round_number += 1
                selected_powerup = None
                powerup_used_this_round = False

                if not enemy_skip_turn:
                    e_charge_start = pygame.time.get_ticks()
                    e_charging = True
                else:
                    enemy_skip_turn = False
                    player_turn = True
                    round_number += 1
                    generate_wind()
            elif (
                player_projectile.x < 0
                or player_projectile.x > WIDTH
                or player_projectile.y > HEIGHT
            ):
                reset_player_projectile()
                player_turn = False
                round_number += 1
                selected_powerup = None
                powerup_used_this_round = False
                e_charge_start = pygame.time.get_ticks()
                e_charging = True

        if not player_turn:
            now = pygame.time.get_ticks()
            if enemy_knockback:
                enemy_knockback = False
                player_turn = True
                round_number += 1
                powerup_used_this_round = False
                generate_wind()
            elif e_charging:
                if now - e_charge_start >= enemy_charge_duration:
                    base_speed = random.uniform(10, 20)

                    angle = 3 * math.pi / 4
                    if current_level.enemy_accuracy_boost > 0:
                        angle_offset = random.uniform(-0.1, 0.1) * (
                            1 - current_level.enemy_accuracy_boost
                        )
                        angle += angle_offset

                    e_projectile_speed = apply_wind_effect(base_speed, -1)

                    enemy_projectile.x = enemy_x
                    enemy_projectile.y = enemy_y
                    enemy_projectile.vel_x = e_projectile_speed * math.cos(angle)
                    enemy_projectile.vel_y = -e_projectile_speed * math.sin(angle)
                    enemy_projectile.image = enemy_projectile_img
                    enemy_projectile.active = True

                    e_charging = False
            if enemy_projectile.active:
                enemy_projectile.update()
                enemy_projectile.draw(screen)

                if check_fence_collision(
                    enemy_projectile.x,
                    enemy_projectile.y,
                    fence_x,
                    fence_y,
                    fence_height,
                ):
                    reset_enemy_projectile()
                    player_turn = True
                    round_number += 1
                    powerup_used_this_round = False
                    generate_wind()
                elif check_collision(
                    enemy_projectile.x,
                    enemy_projectile.y,
                    player_x,
                    player_y,
                    player_radius + enemy_projectile.radius,
                ):
                    damage_taken = 10 + current_level.enemy_power_boost
                    player_health -= damage_taken
                    reset_enemy_projectile()
                    player_turn = True
                    round_number += 1
                    powerup_used_this_round = False
                    generate_wind()
                elif (
                    enemy_projectile.x < 0
                    or enemy_projectile.x > WIDTH
                    or enemy_projectile.y > HEIGHT
                ):
                    reset_enemy_projectile()
                    player_turn = True
                    round_number += 1
                    powerup_used_this_round = False
                    generate_wind()

        draw_health_bar(screen, 50, HEIGHT - 80, player_health, 100)
        draw_text(screen, "HP Pemain", 50, HEIGHT - 100, 20)
        draw_health_bar(screen, WIDTH - 150, HEIGHT - 80, enemy_health, 100)
        draw_text(screen, "HP Musuh", WIDTH - 150, HEIGHT - 100, 20)
        draw_text(screen, f"Putaran: {round_number}", WIDTH // 2, 20, 40)
        draw_text(screen, f"Level: {current_level_number}", 80, 20, 30)

        if current_level.time_limit is not None:
            draw_text(screen, f"TIME: {int(time_remaining)}", WIDTH - 80, 20, 30, RED)

        for rect_item in powerup_boxes:  # Iterasi sebagai tuple (rect, i)
            rect = rect_item[0]
            i = rect_item[1]
            powerup_name = POWERUPS[i]["name"]
            current_powerup_limit = current_level.powerup_limits_per_type.get(
                powerup_name, -1
            )
            current_powerup_uses = powerup_uses_counts[i]

            is_available = (
                current_powerup_limit == -1
                or current_powerup_uses < current_powerup_limit
            )

            if is_available:
                # Gambar latar belakang kotak power-up
                screen.blit(powerup_box_img, (rect.x, rect.y))
                # Gambar ikon power-up
                if powerup_name in resized_powerup_images:
                    img = resized_powerup_images[powerup_name]
                    screen.blit(img, rect)  # Menggambar ikon mengisi seluruh kotak
                pygame.draw.rect(screen, BLACK, rect, 2)  # Bingkai kotak power-up

                # Teks nama power-up (hanya kata pertama)
                draw_text(
                    screen,
                    POWERUPS[i]["name"].split()[0],
                    rect.centerx,
                    rect.centery - 5,
                    20,
                )
                # Teks jumlah penggunaan tersisa
                if current_powerup_limit != -1:
                    draw_text(
                        screen,
                        f"({current_powerup_limit - current_powerup_uses})",
                        rect.centerx,
                        rect.centery + 15,
                        15,
                        BLACK,
                    )

                # Tampilkan deskripsi saat dihover
                if rect.collidepoint(pygame.mouse.get_pos()):
                    desc_text = POWERUPS[i]["desc"]
                    draw_text(screen, desc_text, rect.centerx, rect.y - 20, 15, BLACK)
            else:
                # Jika power-up tidak tersedia, gambar latar belakang redup
                dimmed_box_img = powerup_box_img.copy()
                dimmed_box_img.set_alpha(80)  # Buat semi-transparan
                screen.blit(dimmed_box_img, (rect.x, rect.y))

                # Gambar ikon power-up yang redup
                if powerup_name in resized_powerup_images:
                    dimmed_icon_img = resized_powerup_images[powerup_name].copy()
                    dimmed_icon_img.set_alpha(80)
                    screen.blit(
                        dimmed_icon_img, rect
                    )  # Menggambar ikon mengisi seluruh kotak
                pygame.draw.rect(screen, (100, 100, 100), rect, 2)  # Bingkai abu-abu

                # Teks nama power-up (redup)
                draw_text(
                    screen,
                    POWERUPS[i]["name"].split()[0],
                    rect.centerx,
                    rect.centery - 5,
                    20,
                    (150, 150, 150),  # Teks abu-abu
                )
                # Teks jumlah penggunaan (0)
                draw_text(
                    screen, "(0)", rect.centerx, rect.centery + 15, 15, (150, 150, 150)
                )

        def draw_wind_bar(x, y, strength, direction):
            """Menggambar indikator kekuatan dan arah angin."""
            max_width = 100
            width = int(strength * max_width)
            bar_rect = pygame.Rect(x - max_width // 2, y, width, 10)

            if direction == 1:
                arrow_points = [
                    (x + width / 2, y + 5),
                    (x + width / 2 - 10, y),
                    (x + width / 2 - 10, y + 10),
                ]
            else:
                arrow_points = [
                    (x - width / 2, y + 5),
                    (x - width / 2 + 10, y),
                    (x - width / 2 + 10, y + 10),
                ]

            pygame.draw.rect(screen, BLUE, bar_rect)
            pygame.draw.rect(
                screen, BLACK, pygame.Rect(x - max_width // 2, y, max_width, 10), 2
            )
            pygame.draw.polygon(screen, BLUE, arrow_points)

        draw_wind_bar(WIDTH // 2, 50, wind_strength, wind_direction)
        draw_text(screen, "WIND", WIDTH // 2, 30, 25)

        if p_is_charging:
            draw_power_bar(screen, player_x, player_y - 50, power)

        if player_health <= 0:
            draw_text(
                screen,
                "Game Over! Musuh Menang",
                WIDTH // 2,
                HEIGHT // 2 - 50,
                50,
                RED,
            )
            pygame.display.update()
            pygame.time.wait(3000)
            return False

        elif enemy_health <= 0:
            draw_text(screen, "Anda Menang!", WIDTH // 2, HEIGHT // 2 - 50, 50, GREEN)
            pygame.display.update()
            pygame.time.wait(1500)

            current_level_number += 1
            if current_level_number <= 3:
                next_level_powerup_limits_dict = LEVEL[current_level_number][
                    "powerup_limits"
                ]
                current_level = Level(
                    current_level_number, next_level_powerup_limits_dict
                )

                player_health = 100
                enemy_health = 100
                round_number = 1
                generate_wind()
                reset_player_projectile()
                reset_enemy_projectile()
                player_turn = True
                selected_powerup = None
                powerup_used_this_round = False
                powerup_uses_counts = {i: 0 for i in range(len(POWERUPS))}
                level_start_time = pygame.time.get_ticks()

                print(f"Maju ke Level {current_level_number}")
            else:
                draw_text(
                    screen,
                    "Selamat! Anda Menyelesaikan Semua Level!",
                    WIDTH // 2,
                    HEIGHT // 2 - 50,
                    40,
                    BLUE,
                )
                pygame.display.update()
                pygame.time.wait(3000)
                return True

        if round_number - wind_round_start >= wind_duration:
            generate_wind()

        pygame.display.update()
        clock.tick(60)

    return False
