from game.map import (PLAYABLE_HEIGHT, SCREEN_WIDTH, TILE_SIZE, is_walkable)


def can_move_to(position, width, height): #verifie si le joueur peut se déplacer à la position voulue
    left = int(position.x - width / 2) 
    right = int(position.x + width / 2 - 1)
    top = int(position.y - height / 2)
    bottom = int(position.y + height / 2 - 1)

    for pixel_x, pixel_y in (
        (left, top),
        (right, top),
        (left, bottom),
        (right, bottom),
    ):
        column = int(pixel_x // TILE_SIZE) #convertit la position de pixel en position de grille
        row = int(pixel_y // TILE_SIZE) #convertit la position de pixel en position de grille
        if not is_walkable(column, row): #verifie si la position de grille ,'est pas un mur
            return False

    return (top >= 0 and bottom < PLAYABLE_HEIGHT and left >= 0 and right < SCREEN_WIDTH) #true si la postion est correcte


def can_projectile_move_to(position, radius):
    return can_move_to(position, radius * 2, radius * 2) #true si le projectile peut se déplacer à la position voulue
