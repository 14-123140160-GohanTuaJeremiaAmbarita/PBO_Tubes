import pygame
import math
import random
from settings import *
from Game.game import (
    Character,
    Player,
    Enemy,
    hit_sound,
    miss_sound_player,
    miss_sound_enemy,
    player_projectile_img,
    enemy_projectile_img,
    powerup_box_img,
    resized_powerup_images,
    draw_power_bar,
    draw_health_bar,
    draw_text,
    fence_img,
)
from Game.level import Level
from Game.projectile import Projectile
from Game.wind import (
    generate_wind,
    apply_wind_effect,
    wind_strength,
    wind_direction,
    wind_duration,
    wind_round_start,
    draw_wind_bar,
)
from Game.collision_handler import check_collision, check_fence_collision


class GameLoop:
    def __init__(
        self, screen, initial_level_number, player_projectile_img, enemy_projectile_img
    ):
        """
        Menginisialisasi instance GameLoop.

        Args:
            screen (pygame.Surface): Objek permukaan Pygame untuk menggambar.
            initial_level_number (int): Nomor level awal game.
            player_projectile_img (pygame.Surface): Gambar untuk proyektil pemain.
            enemy_projectile_img (pygame.Surface): Gambar untuk proyektil musuh.
        """
        print("DEBUG: GameLoop __init__ started.")
        self.screen = screen
        self.clock = pygame.time.Clock()
        print("DEBUG: Screen and Clock initialized.")

        self.running = True  # Bendera untuk mengontrol loop utama permainan
        self.game_over = False  # Bendera untuk menunjukkan game over (kalah)
        self.game_won = False  # Bendera untuk menunjukkan permainan dimenangkan (semua level selesai)

        # Inisialisasi level
        self.current_level_number = initial_level_number
        print(f"DEBUG: Initializing Level {self.current_level_number}.")
        # initial_powerup_limits_dict tidak lagi diperlukan di sini karena Level class mengambilnya sendiri
        self.current_level = Level(self.current_level_number)
        print(
            f"DEBUG: Level {self.current_level_number} created with background {self.current_level.background_img.get_size()}."
        )

        # Inisialisasi karakter (menggunakan self.player dan self.enemy secara konsisten)
        self.player = Player(self.current_level.player_x, self.current_level.player_y)
        self.enemy = Enemy(self.current_level.enemy_x, self.current_level.enemy_y)
        print(
            f"DEBUG: Player initialized at ({self.player.x}, {self.player.y}) with HP {self.player.health}."
        )
        print(
            f"DEBUG: Enemy initialized at ({self.enemy.x}, {self.enemy.y}) with HP {self.enemy.health}."
        )

        # Inisialisasi pagar
        self.fence_x = self.current_level.fence_x
        self.fence_y = self.current_level.fence_y
        self.fence_height = self.current_level.fence_height
        self.fence_width = self.current_level.fence_width
        print(
            f"DEBUG: Fence initialized at ({self.fence_x}, {self.fence_y}) with dimensions {self.fence_width}x{self.fence_height}."
        )
        # fence_img diimpor global dari game.py, jadi tidak perlu disimpan di self.current_level.fence_img

        # Inisialisasi proyektil
        self.player_projectile_img = player_projectile_img
        self.enemy_projectile_img = enemy_projectile_img
        self.player_projectile = Projectile(
            -100, -100, 0, 0, self.player_projectile_img
        )
        self.player_projectile.deactivate()  # Pastikan nonaktif
        self.enemy_projectile = Projectile(-100, -100, 0, 0, self.enemy_projectile_img)
        self.enemy_projectile.deactivate()  # Pastikan nonaktif
        print("DEBUG: Player and Enemy Projectiles initialized (inactive).")

        # Inisialisasi status game
        self.round_number = 1
        print(f"DEBUG: Initial round number: {self.round_number}.")
        generate_wind(self.round_number)  # Generate wind for the first round
        print(
            f"DEBUG: Initial wind generated: Strength={wind_strength:.2f}, Direction={wind_direction}."
        )

        self.player_turn = True
        self.enemy_knockback = False
        self.enemy_skip_turn = False
        print(f"DEBUG: Player starts first turn: {self.player_turn}.")

        # Inisialisasi power-up
        self.selected_powerup = None
        self.powerup_used_this_round = False
        self.powerup_uses_counts = {i: 0 for i in range(len(POWERUPS))}
        self.powerup_box_size = POWERUP_BOX_SIZE
        self.powerup_boxes = (
            self._create_powerup_boxes()
        )  # Buat kotak power-up berdasarkan posisi pemain
        print(f"DEBUG: Power-ups initialized. Total power-up types: {len(POWERUPS)}.")

        # Inisialisasi pengisian daya tembakan pemain
        self.p_is_charging = False
        self.p_shoot_start_time = 0
        self.p_projectile_angle = math.pi / 4
        self.power = 0
        print("DEBUG: Player projectile charging state initialized.")

        # Inisialisasi pengisian daya tembakan musuh
        self.e_charge_start = 0
        self.e_charging = False
        self.enemy_charge_duration = 1500
        print("DEBUG: Enemy projectile charging state initialized.")

        # Inisialisasi waktu level (diambil dari current_level)
        self.level_start_time = pygame.time.get_ticks()
        self.time_remaining = self.current_level.time_limit
        print(
            f"DEBUG: Level start time recorded. Time limit: {self.time_remaining if self.time_remaining is not None else 'None'}."
        )

        # Area tembak
        self.shoot_area = pygame.Rect(0, HEIGHT - 150, WIDTH, 150)
        print(f"DEBUG: Shoot area defined: {self.shoot_area}.")
        print("DEBUG: GameLoop __init__ finished.")

    def _create_powerup_boxes(self):
        """Membuat kotak-kotak power-up untuk UI."""
        # Posisi power-up boxes disesuaikan dengan posisi player (bukan player_char)
        start_x = (
            self.player.x - ((self.powerup_box_size + 10) * len(POWERUPS) - 10) // 2
        )
        start_y = self.fence_y - 200
        powerup_boxes = []
        for i in range(len(POWERUPS)):
            rect = pygame.Rect(
                start_x + i * (self.powerup_box_size + 10),
                start_y,
                self.powerup_box_size,
                self.powerup_box_size,
            )
            powerup_boxes.append((rect, i))
        return powerup_boxes

    def _handle_input(self):
        """Menangani input pengguna (mouse dan keyboard)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("DEBUG: QUIT event detected. Exiting game loop.")
                self.running = False
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.player_turn:
                    # Cek klik power-up
                    for rect_item in self.powerup_boxes:
                        rect = rect_item[0]
                        i = rect_item[1]
                        if (
                            rect.collidepoint(event.pos)
                            and not self.powerup_used_this_round
                        ):
                            powerup_name = POWERUPS[i]["name"]
                            current_powerup_limit = (
                                self.current_level.powerup_limits_per_type.get(
                                    powerup_name, -1
                                )
                            )
                            current_powerup_uses = self.powerup_uses_counts[i]

                            if (
                                current_powerup_limit == -1
                                or current_powerup_uses < current_powerup_limit
                            ):
                                self.selected_powerup = i
                                self.powerup_used_this_round = True
                                self.powerup_uses_counts[i] += 1
                                print(
                                    f"DEBUG: Power-up '{powerup_name}' dipilih. Sisa penggunaan: {current_powerup_limit - current_powerup_uses if current_powerup_limit != -1 else 'Tidak Terbatas'}."
                                )

                                if POWERUPS[i]["type"] == "heal":
                                    heal_amount = 30
                                    self.player.health = min(
                                        self.player.health + heal_amount,
                                        PLAYER_MAX_HEALTH,  # Gunakan PLAYER_MAX_HEALTH dari settings
                                    )
                                    print(
                                        f"DEBUG: Heal power-up used. Player HP: {self.player.health}."
                                    )
                                    self.player_turn = (
                                        False  # Player's turn ends after using heal
                                    )
                                    self.round_number += 1  # Round increments here, as heal is a full action
                                    print(
                                        f"DEBUG: Round increased (Heal Power-up used). New round: {self.round_number}."
                                    )
                                    self.selected_powerup = None
                                    self.e_charge_start = pygame.time.get_ticks()
                                    self.e_charging = True
                                    generate_wind(
                                        self.round_number
                                    )  # Generate new wind
                                hit_sound.play()
                                break

                    # Cek klik area tembak
                    if self.shoot_area.collidepoint(event.pos):
                        if not self.player_projectile.active and not self.p_is_charging:
                            self.p_shoot_start_time = pygame.time.get_ticks()
                            self.p_is_charging = True
                            print("DEBUG: Player started charging shot.")

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.player_turn and self.p_is_charging:
                    hold_time = pygame.time.get_ticks() - self.p_shoot_start_time
                    charge_percentage = min(1.0, hold_time / MAX_PLAYER_CHARGE_TIME)
                    base_speed = (
                        MIN_PLAYER_BASE_SPEED
                        + (MAX_PROJECTILE_SPEED - MIN_PLAYER_BASE_SPEED)
                        * charge_percentage
                    )
                    speed = apply_wind_effect(base_speed, 1)

                    proj_image_for_player = player_projectile_img
                    proj_radius_for_player = player_projectile_img.get_width() // 2

                    if (
                        self.selected_powerup is not None
                        and POWERUPS[self.selected_powerup]["type"] == "size"
                    ):
                        proj_image_for_player = pygame.transform.scale(
                            player_projectile_img,
                            (
                                player_projectile_img.get_width() * 2,
                                player_projectile_img.get_height() * 2,
                            ),
                        )
                        proj_radius_for_player *= 2
                        print("DEBUG: Big Projectile power-up applied.")

                    self.player_projectile.deactivate()  # Pastikan dinonaktifkan sebelum digunakan kembali
                    self.player_projectile.x = self.player.x  # Gunakan self.player.x
                    self.player_projectile.y = self.player.y  # Gunakan self.player.y
                    self.player_projectile.vel_x = speed * math.cos(
                        self.p_projectile_angle
                    )
                    self.player_projectile.vel_y = -speed * math.sin(
                        self.p_projectile_angle
                    )
                    self.player_projectile.image = proj_image_for_player
                    self.player_projectile.radius = proj_radius_for_player
                    self.player_projectile.active = True

                    self.p_is_charging = False
                    self.player.state = "idle"  # Gunakan self.player.state
                    print(
                        f"DEBUG: Player released shot. Power: {self.power}, Speed: {speed:.2f}, Angle: {math.degrees(self.p_projectile_angle):.2f} deg. Projectile active."
                    )
                    print(
                        f"DEBUG: Player projectile initial position: ({self.player_projectile.x:.2f}, {self.player_projectile.y:.2f})."
                    )
        return True  # Game loop should continue

    def _update_game_state(self):
        """Memperbarui logika game (pergerakan proyektil, tabrakan, giliran)."""
        # Pembaruan animasi karakter
        self.player.update_image_by_state(
            pygame.time.get_ticks(), HIT_DURATION, MISS_DURATION
        )
        self.enemy.update_image_by_state(
            pygame.time.get_ticks(), HIT_DURATION, MISS_DURATION
        )

        # Pembaruan pengisian daya pemain untuk power bar
        if self.p_is_charging:
            hold_time = pygame.time.get_ticks() - self.p_shoot_start_time
            self.power = min(150, hold_time // 10)
            print(f"DEBUG: Power Bar: {self.power}")

        print(
            f"DEBUG: Putaran: {self.round_number}, Giliran Pemain: {self.player_turn}, Proyektil Pemain Aktif: {self.player_projectile.active}, Proyektil Musuh Aktif: {self.enemy_projectile.active}"
        )

        # --- Player Projectile Logic ---
        if self.player_projectile.active:
            self.player_projectile.update()
            print(
                f"DEBUG: Player Projectile Update - Posisi: ({self.player_projectile.x:.2f}, {self.player_projectile.y:.2f}), Kecepatan: ({self.player_projectile.vel_x:.2f}, {self.player_projectile.vel_y:.2f})"
            )

            player_projectile_resolved_this_frame = False  # Flag to ensure turn logic runs only once per projectile resolution
            # Check collision with fence
            if check_fence_collision(
                self.player_projectile.x,
                self.player_projectile.y,
                self.fence_x,
                self.fence_y,
                self.fence_height,
                self.fence_width,  # Meneruskan fence_width
            ):
                print(
                    f"DEBUG: Player projectile hit fence at ({self.player_projectile.x:.2f}, {self.player_projectile.y:.2f})."
                )
                miss_sound_player.play()
                self.player.state = "edge"  # Set player state to edge
                player_projectile_resolved_this_frame = True
            # Check collision with enemy
            elif check_collision(
                self.player_projectile.x,
                self.player_projectile.y,
                self.enemy.x,
                self.enemy.y,
                self.enemy.radius
                + self.player_projectile.radius,  # Menggunakan jumlah radius
            ):
                damage = BASE_DAMAGE  # Gunakan BASE_DAMAGE dari settings
                if (
                    self.selected_powerup is not None
                    and POWERUPS[self.selected_powerup]["type"] == "damage"
                ):
                    original_damage = damage
                    damage = POWERUPS[self.selected_powerup]["effect"](damage)
                    print(
                        f"DEBUG: Damage power-up applied. Original damage: {original_damage}, New damage: {damage}."
                    )

                if (
                    self.selected_powerup is not None
                    and POWERUPS[self.selected_powerup]["type"] == "poison"
                ):
                    self.enemy_skip_turn = True
                    self.enemy_knockback = True
                    print("DEBUG: Player hit enemy with Poison/Knockback power-up.")

                self.enemy.health -= damage
                hit_sound.play()
                self.enemy.state = "hit"  # Set enemy state to hit
                print(
                    f"DEBUG: Player projectile hit enemy. Enemy HP: {self.enemy.health}."
                )
                player_projectile_resolved_this_frame = True
            # Check if projectile went off-screen
            elif (
                self.player_projectile.x < 0
                or self.player_projectile.x > WIDTH
                or self.player_projectile.y > HEIGHT
            ):
                print(
                    f"DEBUG: Player projectile went off-screen at ({self.player_projectile.x:.2f}, {self.player_projectile.y:.2f})."
                )
                miss_sound_player.play()
                self.player.state = "edge"  # Set player state to edge
                player_projectile_resolved_this_frame = True

            if player_projectile_resolved_this_frame:
                self.player_projectile.deactivate()  # Direct call to deactivate the instance
                self.player_turn = False  # Switch to enemy turn
                self.selected_powerup = None  # Reset selected powerup
                self.powerup_used_this_round = False  # Reset powerup used for next turn
                print("DEBUG: Player projectile resolved. Turn switched to Enemy.")

                if self.enemy_skip_turn:
                    # Enemy's turn is immediately skipped, so round increments and turn goes back to player
                    self.enemy_skip_turn = False
                    self.player_turn = True
                    self.round_number += (
                        1  # Increment round here, as enemy's action is resolved
                    )
                    print(
                        f"DEBUG: Round increased (Player's turn resolved, Enemy skipped). New round: {self.round_number}. Turn: Player"
                    )
                    generate_wind(self.round_number)
                else:
                    # Start enemy charging if not skipped
                    self.e_charge_start = pygame.time.get_ticks()
                    self.e_charging = True
                    print(
                        f"DEBUG: Enemy starts charging. e_charging: {self.e_charging}"
                    )

        # --- Enemy Turn Logic ---
        # This block only runs if it's the enemy's turn
        if not self.player_turn:
            now = pygame.time.get_ticks()

            # If enemy was knocked back, resolve their turn immediately
            if self.enemy_knockback:
                print(
                    "DEBUG: Enemy knockback effect resolved. Turn switches to player."
                )
                self.enemy_knockback = False
                self.player_turn = True
                self.powerup_used_this_round = False  # Reset for player's new turn
                self.round_number += 1  # Increment round here as enemy's action is resolved (skipped by knockback)
                print(
                    f"DEBUG: Round increased (Enemy knockback resolved). New round: {self.round_number}. Turn: Player"
                )
                generate_wind(self.round_number)
                self.e_charging = False  # Ensure enemy isn't still charging
                self.enemy.state = "idle"  # Ensure enemy state is reset

            # If enemy is charging and hasn't launched a projectile yet
            elif self.e_charging and not self.enemy_projectile.active:
                if now - self.e_charge_start >= self.enemy_charge_duration:
                    # Enemy finishes charging and shoots
                    random_charge_percentage = random.uniform(
                        0.5, 1.0
                    )  # Musuh selalu mengisi daya setidaknya 50%
                    base_speed = (
                        MIN_ENEMY_BASE_SPEED
                        + (MAX_PROJECTILE_SPEED - MIN_ENEMY_BASE_SPEED)
                        * random_charge_percentage
                    )

                    angle = 3 * math.pi / 4  # Default angle for enemy
                    if self.current_level.enemy_accuracy_boost > 0:
                        angle_offset = random.uniform(-0.1, 0.1) * (
                            1 - self.current_level.enemy_accuracy_boost
                        )
                        angle += angle_offset
                    speed = apply_wind_effect(
                        base_speed, -1
                    )  # Apply wind effect for enemy (direction -1 for left)

                    self.enemy_projectile.deactivate()  # Ensure old projectile is deactivated
                    self.enemy_projectile.x = self.enemy.x  # Gunakan self.enemy.x
                    self.enemy_projectile.y = self.enemy.y  # Gunakan self.enemy.y
                    self.enemy_projectile.vel_x = speed * math.cos(angle)
                    self.enemy_projectile.vel_y = -speed * math.sin(angle)
                    self.enemy_projectile.image = (
                        enemy_projectile_img  # Ensure correct image
                    )
                    self.enemy_projectile.radius = (
                        enemy_projectile_img.get_width() // 2
                    )  # Ensure correct radius
                    self.enemy_projectile.active = True
                    self.e_charging = False  # Charging finished
                    self.enemy.state = "idle"  # Enemy returns to idle after shooting
                    print(
                        f"DEBUG: Enemy finished charging and shot. Projectile Active: {self.enemy_projectile.active}, Random Charge %: {random_charge_percentage:.2f}, Base Speed: {base_speed:.2f}, Speed (with wind): {speed:.2f}, Velocity: ({self.enemy_projectile.vel_x:.2f}, {self.enemy_projectile.vel_y:.2f})"
                    )
                    print(
                        f"DEBUG: Enemy projectile initial position: ({self.enemy_projectile.x:.2f}, {self.enemy_projectile.y:.2f}), Enemy position: ({self.enemy.x:.2f}, {self.enemy.y:.2f})"
                    )

            # --- Enemy Projectile Update and Collision Checks (runs every frame if active) ---
            # This block is now outside the e_charging check, so it continues to update after launch
            if self.enemy_projectile.active:
                self.enemy_projectile.update()
                print(
                    f"DEBUG: Enemy Projectile moving. Position: ({self.enemy_projectile.x:.2f}, {self.enemy_projectile.y:.2f}), Velocity: ({self.enemy_projectile.vel_x:.2f}, {self.enemy_projectile.vel_y:.2f})"
                )

                enemy_projectile_resolved_this_frame = False
                # Check collision with fence
                if check_fence_collision(
                    self.enemy_projectile.x,
                    self.enemy_projectile.y,
                    self.fence_x,
                    self.fence_y,
                    self.fence_height,
                    self.fence_width,  # Meneruskan fence_width
                ):
                    print(
                        f"DEBUG: Enemy projectile hit fence at ({self.enemy_projectile.x:.2f}, {self.enemy_projectile.y:.2f})."
                    )
                    miss_sound_enemy.play()
                    self.enemy.state = "edge"  # Set enemy state to edge
                    enemy_projectile_resolved_this_frame = True
                # Check collision with player
                elif check_collision(
                    self.enemy_projectile.x,
                    self.enemy_projectile.y,
                    self.player.x,
                    self.player.y,
                    self.player.radius
                    + self.enemy_projectile.radius,  # Menggunakan jumlah radius
                ):
                    damage_taken = (
                        self.current_level.enemy_power_boost
                    )  # Gunakan enemy_power_boost dari level
                    self.player.health -= damage_taken
                    hit_sound.play()
                    self.player.state = "hit"  # Set player state to hit
                    print(
                        f"DEBUG: Enemy projectile hit player. Player HP: {self.player.health}."
                    )
                    enemy_projectile_resolved_this_frame = True
                # Check if projectile went off-screen
                elif (
                    self.enemy_projectile.x < 0
                    or self.enemy_projectile.x > WIDTH
                    or self.enemy_projectile.y > HEIGHT
                ):
                    print(
                        f"DEBUG: Enemy projectile went off-screen at ({self.enemy_projectile.x:.2f}, {self.enemy_projectile.y:.2f})."
                    )
                    miss_sound_enemy.play()
                    self.enemy.state = "edge"  # Set enemy state to edge
                    enemy_projectile_resolved_this_frame = True

                if enemy_projectile_resolved_this_frame:
                    self.enemy_projectile.deactivate()  # Direct call to deactivate the instance
                    self.player_turn = True  # Switch back to player turn
                    self.powerup_used_this_round = False  # Reset for player's new turn
                    self.selected_powerup = None  # Reset selected powerup
                    self.round_number += (
                        1  # Increment round here, as enemy's action is resolved
                    )
                    print(
                        f"DEBUG: Round increased (Enemy's turn resolved). New round: {self.round_number}. Turn: Player"
                    )
                    generate_wind(self.round_number)

        # Wind update (outside turn logic, based on round_number)
        global wind_round_start, wind_duration  # Akses variabel global wind
        if self.round_number - wind_round_start >= wind_duration:
            print(
                f"DEBUG: Wind duration ended. Generating new wind for round {self.round_number}."
            )
            generate_wind(self.round_number)

        # Check level time limit
        if self.current_level.time_limit is not None:
            elapsed_time = (pygame.time.get_ticks() - self.level_start_time) / 1000
            self.time_remaining = max(0, self.current_level.time_limit - elapsed_time)
            if self.time_remaining <= 0:
                print("DEBUG: Time limit reached. Game Over.")
                self.game_over = True  # Set game_over flag
                return False  # Game ends

        # Check win/lose conditions
        if self.player.health <= 0:
            print("DEBUG: Player health zero. Game Over.")
            self.game_over = True  # Set game_over flag
            return False  # Game ends
        elif self.enemy.health <= 0:
            print("DEBUG: Enemy health zero. Player Wins.")
            self.game_won = True  # Set game_won flag
            return False  # Game ends

        return True  # Game continues

    def _draw_elements(self):
        """Menggambar semua elemen game ke layar."""
        self.screen.fill(WHITE)
        self.screen.blit(self.current_level.background_img, (0, 0))

        if self.current_level_number > 1:
            # Menggambar gambar pagar yang diimpor secara global dari game.py
            self.screen.blit(fence_img, (self.fence_x, self.fence_y))

        self.player.draw(self.screen)  # Gunakan self.player
        self.enemy.draw(self.screen)  # Gunakan self.enemy

        if self.player_projectile.active:
            self.player_projectile.draw(self.screen)
        if self.enemy_projectile.active:
            self.enemy_projectile.draw(self.screen)

        draw_health_bar(
            self.screen, 50, HEIGHT - 80, self.player.health, PLAYER_MAX_HEALTH
        )  # Gunakan self.player.health
        draw_text(self.screen, "HP Pemain", 50, HEIGHT - 100, 20)
        draw_health_bar(
            self.screen, WIDTH - 150, HEIGHT - 80, self.enemy.health, ENEMY_MAX_HEALTH
        )  # Gunakan self.enemy.health
        draw_text(self.screen, "HP Musuh", WIDTH - 150, HEIGHT - 100, 20)
        draw_text(self.screen, f"Putaran: {self.round_number}", WIDTH // 2, 20, 40)
        draw_text(self.screen, f"Level: {self.current_level_number}", 80, 20, 30)

        # Debug display: Round Number and Player Turn
        debug_text_round = f"Round: {self.round_number}"
        debug_text_turn = f"Turn: {'Player' if self.player_turn else 'Enemy'}"
        draw_text(self.screen, debug_text_round, WIDTH - 100, HEIGHT - 50, 20, BLUE)
        draw_text(self.screen, debug_text_turn, WIDTH - 100, HEIGHT - 30, 20, BLUE)

        if self.current_level.time_limit is not None:
            draw_text(
                self.screen,
                f"TIME: {int(self.time_remaining)}",
                WIDTH - 80,
                20,
                30,
                RED,
            )

        # Gambar indikator angin
        draw_wind_bar(self.screen, WIDTH // 2, 50, wind_strength, wind_direction)
        draw_text(self.screen, "WIND", WIDTH // 2, 30, 25)

        # Gambar bar kekuatan tembakan pemain
        if self.p_is_charging:
            draw_power_bar(
                self.screen, self.player.x, self.player.y - 50, self.power
            )  # Gunakan self.player.x

        # Gambar kotak power-up
        for rect_item in self.powerup_boxes:
            rect = rect_item[0]
            i = rect_item[1]
            powerup_name = POWERUPS[i]["name"]
            current_powerup_limit = self.current_level.powerup_limits_per_type.get(
                powerup_name, -1
            )
            current_powerup_uses = self.powerup_uses_counts[i]

            is_available = (
                current_powerup_limit == -1
                or current_powerup_uses < current_powerup_limit
            )

            if is_available:
                self.screen.blit(powerup_box_img, (rect.x, rect.y))
                if powerup_name in resized_powerup_images:
                    img = resized_powerup_images[powerup_name]
                    self.screen.blit(img, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)

                draw_text(
                    self.screen,
                    POWERUPS[i]["name"].split()[0],
                    rect.centerx,
                    rect.centery - 5,
                    20,
                )
                if current_powerup_limit != -1:
                    draw_text(
                        self.screen,
                        f"({current_powerup_limit - current_powerup_uses})",
                        rect.centerx,
                        rect.centery + 15,
                        15,
                        BLACK,
                    )

                if rect.collidepoint(pygame.mouse.get_pos()):
                    desc_text = POWERUPS[i]["desc"]
                    draw_text(
                        self.screen, desc_text, rect.centerx, rect.y - 20, 15, BLACK
                    )
            else:
                dimmed_box_img = powerup_box_img.copy()
                dimmed_box_img.set_alpha(80)
                self.screen.blit(dimmed_box_img, (rect.x, rect.y))

                if powerup_name in resized_powerup_images:
                    dimmed_icon_img = resized_powerup_images[powerup_name].copy()
                    dimmed_icon_img.set_alpha(80)
                    self.screen.blit(dimmed_icon_img, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)

                draw_text(
                    self.screen,
                    POWERUPS[i]["name"].split()[0],
                    rect.centerx,
                    rect.centery - 5,
                    20,
                    (150, 150, 150),
                )
                draw_text(
                    self.screen,
                    "(0)",
                    rect.centerx,
                    rect.centery + 15,
                    15,
                    (150, 150, 150),
                )

        pygame.display.update()

    def run(self):
        """Menjalankan loop utama game."""
        while self.running:
            # Handle input events
            if not self._handle_input():
                break  # If _handle_input returns False (e.g., QUIT event), exit loop

            # Update game state
            game_continue = self._update_game_state()
            if not game_continue:  # If _update_game_state returns False (game over/win)
                self.running = False  # Stop the main loop
                break

            # Draw elements to screen
            self._draw_elements()

            # Cap the frame rate
            self.clock.tick(60)

        # After the loop, determine game result
        if self.game_over:
            print("DEBUG: Game ended: Player lost.")
            return False  # Player lost
        elif self.game_won:
            print("DEBUG: Game ended: Player won all levels.")
            return True  # Player won all levels
        else:
            print("DEBUG: Game ended: User quit.")
            return False  # User quit


def run_game_loop(
    screen, initial_level_number, player_projectile_img, enemy_projectile_img
):
    """
    Fungsi pembantu untuk memulai instance GameLoop.
    Ini adalah titik masuk utama untuk menjalankan permainan.
    """
    game = GameLoop(
        screen, initial_level_number, player_projectile_img, enemy_projectile_img
    )
    return game.run()
