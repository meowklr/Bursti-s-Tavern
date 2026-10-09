import pygame
from collections import deque


TILE_SIZE = 20
MAP_COLUMNS = 64
MAP_ROWS = 25
HUD_HEIGHT = 140

SCREEN_WIDTH = MAP_COLUMNS * TILE_SIZE
PLAYABLE_HEIGHT = MAP_ROWS * TILE_SIZE
SCREEN_HEIGHT = PLAYABLE_HEIGHT + HUD_HEIGHT

MAP = [
    "################################################################",
    "################################################################",
    "################################################################",
    "################################################################",
    "################################################################",
    "#####....############################################.......####",
    "###..........................................................###",
    "###..........................................................###",
    "###..###.................................................##..###",
    "##..#####...............................................####..##",
    "##..#####...............................................####..##",
    "##..#####...............................................####..##",
    "##..#####............#####............#####.............####..DD",
    "DD...................#####............#####...................DD",
    "DD...................#####............#####...................DD",
    "DD...................#####............#####...................##",
    "##...................#####............#####...................##",
    "##............................................................##",
    "##............................................................##",
    "####..........................................................##",
    "######..########....................................#####..##.##",
    "######..########............................####################",
    "#######.########............................####################",
    "################################################################",
    "################################################################",
]

ENTRANCES = [
    (0, 13),
    (0, 14),
    (63, 13),
    (63, 14),
]

SEATING_POSITIONS = [
    (4, 11),
    (8, 9),
    (8, 11),
    (21, 12),
    (21, 13),
    (21, 15),
    (25, 12),
    (25, 14),
    (25, 15),
    (38, 12),
    (38, 14),
    (38, 15),
    (42, 12),
    (42, 13),
    (42, 15),
    (56, 9),
    (56, 11),
]

FOOD_POSITIONS = {
    "STEAK": [
        (30, 4),
    ],
    "SALAD": [
        (39, 4),
    ],
    "WATER": [
        (50, 21),
    ],
}

FOOD_PICKUP_POSITIONS = {
    "STEAK": (30, 6),
    "SALAD": (39, 6),
    "WATER": (50, 20),
}


def is_walkable(column, row): #verifie si la position de grille est un mur ou pas
    if not (0 <= column < MAP_COLUMNS and 0 <= row < MAP_ROWS):
        return False

    return MAP[row][column] != "#"


def grid_to_position(column, row): #convertit la position de grille en position de pixel
    return pygame.Vector2(
        column * TILE_SIZE + TILE_SIZE / 2,
        row * TILE_SIZE + TILE_SIZE / 2,
    )


def find_grid_path(start, target): #trouve le chemin le plus court entre deux positions
    start = tuple(start)
    target = tuple(target)
    queue = deque([start])
    previous = {start: None}

    while queue:
        current = queue.popleft()
        if current == target:
            break

        column, row = current
        for neighbor in (
            (column + 1, row),
            (column - 1, row),
            (column, row + 1),
            (column, row - 1),
        ):
            if neighbor in previous:
                continue
            if neighbor != target and not is_walkable(*neighbor):
                continue
            if not (
                0 <= neighbor[0] < MAP_COLUMNS
                and 0 <= neighbor[1] < MAP_ROWS
            ):
                continue
            previous[neighbor] = current
            queue.append(neighbor)

    if target not in previous:
        return []

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    return list(reversed(path))
