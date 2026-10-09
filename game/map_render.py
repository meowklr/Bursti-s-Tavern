import pygame

from game.constants import FOOD_LABELS
from game.map import (FOOD_POSITIONS, MAP, MAP_COLUMNS, MAP_ROWS, PLAYABLE_HEIGHT, SCREEN_WIDTH, SEATING_POSITIONS, TILE_SIZE, grid_to_position)


def draw_foods(screen, food_images, available_foods, label_font): #affiche les aliments disponibles sur la carte avec leur nom
    for food_name, positions in FOOD_POSITIONS.items():
        if food_name not in available_foods: #si l'aliment n'est pas disponible on skip
            continue

        image = food_images[food_name]
        label_text = FOOD_LABELS[food_name]
        label = label_font.render(label_text, False, (255, 238, 150))
        outline = label_font.render(label_text, False, (0, 0, 0))

        for column, row in positions:
            position = grid_to_position(column, row)
            rectangle = image.get_rect(center=position)
            label_rectangle = label.get_rect(
                midbottom=(round(position.x), rectangle.top - 4),
            )
            for offset_x, offset_y in (
                (-2, -2), (0, -2), (2, -2),
                (-2, 0), (2, 0),
                (-2, 2), (0, 2), (2, 2),
            ):
                screen.blit(outline, label_rectangle.move(offset_x, offset_y))
            screen.blit(label, label_rectangle)
            screen.blit(image, rectangle)


def draw_debug_grid(screen): #affiche la grille de la carte avec les murs les sièges et les aliments disponibles pour le debug suelement
    colors = {
        "#": (180, 40, 40, 80),
        "D": (40, 180, 80, 100),
    }
    food_colors = {
        "STEAK": (180, 100, 40, 130),
        "SALAD": (60, 180, 70, 130),
        "WATER": (50, 160, 220, 130),
    }
    overlay = pygame.Surface((SCREEN_WIDTH, PLAYABLE_HEIGHT), pygame.SRCALPHA)

    for row in range(MAP_ROWS):
        for column in range(MAP_COLUMNS):
            rectangle = pygame.Rect(
                column * TILE_SIZE,
                row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )
            color = colors.get(MAP[row][column])
            if color:
                pygame.draw.rect(overlay, color, rectangle)

    for column, row in SEATING_POSITIONS:
        rectangle = pygame.Rect(
            column * TILE_SIZE,
            row * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE,
        )
        pygame.draw.rect(overlay, (60, 120, 220, 100), rectangle)

    for food_name, positions in FOOD_POSITIONS.items():
        for column, row in positions:
            rectangle = pygame.Rect(
                column * TILE_SIZE,
                row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )
            pygame.draw.rect(overlay, food_colors[food_name], rectangle)

    screen.blit(overlay, (0, 0))
    line_color = (255, 255, 255, 100)
    for column in range(MAP_COLUMNS + 1):
        x = column * TILE_SIZE
        pygame.draw.line(screen, line_color, (x, 0), (x, PLAYABLE_HEIGHT))
    for row in range(MAP_ROWS + 1):
        y = row * TILE_SIZE
        pygame.draw.line(screen, line_color, (0, y), (SCREEN_WIDTH, y))

    font = pygame.font.Font(None, 16)
    for row in range(MAP_ROWS):
        for column in range(MAP_COLUMNS):
            label = font.render(f"{column},{row}", True, (255, 255, 255))
            screen.blit(label, (column * TILE_SIZE + 2, row * TILE_SIZE + 2))
