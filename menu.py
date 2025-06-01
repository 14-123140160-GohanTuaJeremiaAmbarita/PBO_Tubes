import pygame
from Game.game import *


def main_menu(screen):
    selected_level = 1
    running = True

    font_title = pygame.font.Font(None, 74)
    font_option = pygame.font.Font(None, 48)

    button_width = 180
    button_height = 60
    button_gap = 20

    level_buttons_rects = []
    level_names = ["Beginner", "Medium", "Hard"]

    start_y_levels = (
        HEIGHT // 2
        - (len(level_names) * (button_height + button_gap) - button_gap) // 2
    )

    for i, name in enumerate(level_names):
        rect = pygame.Rect(
            WIDTH // 2 - button_width // 2,
            start_y_levels + i * (button_height + button_gap),
            button_width,
            button_height,
        )
        level_buttons_rects.append(rect)

    start_button_rect = pygame.Rect(
        WIDTH // 2 - button_width // 2,
        level_buttons_rects[-1].y + button_height + button_gap * 2,
        button_width,
        button_height,
    )

    while running:
        screen.fill(WHITE)
        draw_text(screen, "CAT VS DOG", WIDTH // 2, HEIGHT // 4, 74, BLACK)

        for i, rect in enumerate(level_buttons_rects):
            level_num = i + 1
            color = RED if selected_level == level_num else BLACK
            pygame.draw.rect(screen, color, rect, 2, border_radius=10)
            draw_text(screen, level_names[i], rect.centerx, rect.centery, 40, color)

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
                for i, rect in enumerate(level_buttons_rects):
                    if rect.collidepoint(event.pos):
                        selected_level = i + 1

                if start_button_rect.collidepoint(event.pos):
                    return selected_level

        pygame.display.flip()
        pygame.time.Clock().tick(60)
