from pathlib import Path

import pygame

IMAGE_SIZE = (70, 90) #taille des sprites joueur
FOOD_SIZE = (32, 32) #taille des sprites nourriture

def load_image(project_folder, *path_parts, size, preserve_aspect=False): #charger les images et les redimmensionner
    image_path = Path(project_folder).joinpath(*path_parts) #chemin de l'image
    image = pygame.image.load(str(image_path)) 

    try:
        image = image.convert_alpha() #sert a convertir l'image en alpha pour la transparence
    except pygame.error:
        image = image.convert() #convertir l'image normalement si pas de transparence

    if not preserve_aspect: #sert a redimmensionner l'image sans deformation
        return pygame.transform.scale(image, size)

    source_width, source_height = image.get_size()
    scale = min(size[0] / source_width, size[1] / source_height)
    scaled_size = (max(1, round(source_width * scale)), max(1, round(source_height * scale))) 
    image = pygame.transform.smoothscale(image, scaled_size) #redimmensionner l'image de maniere stylée

    canvas = pygame.Surface(size, pygame.SRCALPHA) #creer un canvas transparent pour centrer l'image redimmensionnée
    canvas.blit(image, image.get_rect(center=(size[0] // 2, size[1] // 2))) #centrer l'image sur le canvas
    return canvas


def load_sound(project_folder, filename): #charger les sons
    sound_path = Path(project_folder) / "assets" / "sounds" / filename
    return pygame.mixer.Sound(str(sound_path))


def start_music(project_folder, filename): #lancer la musique
    music_path = Path(project_folder) / "assets" / "sounds" / filename
    pygame.mixer.music.load(str(music_path))
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1) #joue la musique en boucle


def load_game_assets(project_folder):
    image = lambda filename, size: load_image(
        project_folder,
        "assets",
        "images",
        filename,
        size=size,
        preserve_aspect=True,
    )
    idle_images = {
        "left": image("left.png", IMAGE_SIZE),
        "right": image("right.png", IMAGE_SIZE),
    }
    throw_images = { #images de lancer mises dans l'ordre pour l'animation
        "left": [
            image(f"left throw {index}.png", IMAGE_SIZE)
            for index in range(1, 4)
        ],
        "right": [
            image(f"right throw {index}.png", IMAGE_SIZE)
            for index in range(1, 4)
        ],
    }
    food_images = {
        "STEAK": image("steak.png", FOOD_SIZE),
        "SALAD": image("salade.png", FOOD_SIZE),
        "WATER": image("eau.png", FOOD_SIZE),
    }
    return {
        "background": load_image(project_folder, "assets", "images", "background3.png", size=(1280, 640)),
        "idle_images": idle_images,
        "throw_images": throw_images,
        "food_images": food_images,
        "client_image": image("gobelin.png", (42, 42)),
    }

