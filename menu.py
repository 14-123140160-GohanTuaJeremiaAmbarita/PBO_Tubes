import pygame
from game import (
    WIDTH,
    HEIGHT,
    BLACK,
    WHITE,
    GREEN,
    draw_text,
)  # Import necessary constants and functions


def main_menu(screen):
    selected_level = 1  # Default to Level 1 (Beginner)
    running = True

    # Font for menu items
    font_title = pygame.font.Font(None, 74)
    font_option = pygame.font.Font(None, 48)

    # Button dimensions and spacing
    button_width = 180
    button_height = 60
    button_gap = 20

    # Calculate positions for the level buttons
    level_buttons_rects = []
    level_names = ["Beginner", "Medium", "Hard"]

    # Starting Y position for the first level button, centered vertically
    start_y_levels = (
        HEIGHT // 2
        - (len(level_names) * (button_height + button_gap) - button_gap) // 2
    )

    for i, name in enumerate(level_names):
        rect = pygame.Rect(
            WIDTH // 2 - button_width // 2,  # Center horizontally
            start_y_levels + i * (button_height + button_gap),
            button_width,
            button_height,
        )
        level_buttons_rects.append(rect)

    # Position for the START button, below the level options
    start_button_rect = pygame.Rect(
        WIDTH // 2 - button_width // 2,
        level_buttons_rects[-1].y
        + button_height
        + button_gap * 2,  # Below last level button
        button_width,
        button_height,
    )

    while running:
        screen.fill(WHITE)  # Simple white background for the menu

        # Draw Title
        draw_text(screen, "Gravity Warfare", WIDTH // 2, HEIGHT // 4, 74, BLACK)

        # Draw Level Buttons
        for i, rect in enumerate(level_buttons_rects):
            level_num = i + 1
            color = (
                GREEN if selected_level == level_num else BLACK
            )  # Green if selected, Black otherwise
            pygame.draw.rect(
                screen, color, rect, 2, border_radius=10
            )  # Draw only the border
            draw_text(screen, level_names[i], rect.centerx, rect.centery, 40, color)

        # Draw Start Button
        pygame.draw.rect(screen, GREEN, start_button_rect, border_radius=10)
        draw_text(
            screen,
            "START",
            start_button_rect.centerx,
            start_button_rect.centery,
            40,
            WHITE,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for level button clicks
                for i, rect in enumerate(level_buttons_rects):
                    if rect.collidepoint(event.pos):
                        selected_level = i + 1  # Update selected level

                # Check for START button click
                if start_button_rect.collidepoint(event.pos):
                    return selected_level  # Return the chosen level to start the game

        pygame.display.flip()
        pygame.time.Clock().tick(60)
