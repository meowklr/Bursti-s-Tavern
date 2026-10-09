from pathlib import Path
import random

import pygame

from game.assets import load_game_assets, load_sound, start_music
from game.client import Client
from game.collisions import can_move_to, can_projectile_move_to
from game.constants import FOOD_NAMES
from game.map import (ENTRANCES, PLAYABLE_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, SEATING_POSITIONS, TILE_SIZE, find_grid_path, FOOD_PICKUP_POSITIONS, grid_to_position)
from game.map_render import draw_debug_grid, draw_foods
from game.leaderboard import Leaderboard
from game.player import Player
from ui.hud import HUD


class Game:
    #valeurs par defaut de la physique du jeu
    WIDTH = SCREEN_WIDTH
    HEIGHT = SCREEN_HEIGHT
    FPS = 60
    PROJECTILE_SPEED = 480
    DEBUG_GRID = False
    CLIENT_SPAWN_DELAY = 5
    MAX_SEATED_CLIENTS = 5

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT)) #taille fenetre
        pygame.display.set_caption("Bursti's Tavern") #nom de la fenetre

        self.clock = pygame.time.Clock()
        self.food_label_font = pygame.font.Font(None, 28) #police pour les titres des aliments
        self.client_order_font = pygame.font.Font(None, 22) #police pour les commandes des clients
        self.project_folder = Path(__file__).resolve().parent.parent 
        self.leaderboard = Leaderboard(
            self.project_folder / "data" / "leaderboard.json",
        )

        #charger les assets 
        self.sounds = {
            name: load_sound(self.project_folder, filename)
            for name, filename in {
                "throw": "throw.mp3",
                "pickup": "pickup-item.mp3",
                "impact": "impacthit.mp3",
            }.items()
        }
        for sound in self.sounds.values():
            sound.set_volume(0.45)
        start_music(self.project_folder, "musicloop.mp3") #lancer la musique
        assets = load_game_assets(self.project_folder)
        self.background = assets["background"]
        self.food_images = assets["food_images"]

        self.player = Player(
            position=pygame.Vector2(self.WIDTH // 2, PLAYABLE_HEIGHT // 2), #spawn du joueur au milieu en 2d
            idle_images=assets["idle_images"], 
            throw_images=assets["throw_images"],
            food_images=self.food_images,
            projectile_speed=self.PROJECTILE_SPEED,
            collision_checker=can_move_to,
        )
        self.client_image = assets["client_image"]

        self.projectiles = [] 
        self.clients = []
        self.available_seats = set(SEATING_POSITIONS) - set(ENTRANCES) #pour ne pas que les clients s'asseoientt aux entrées
        self.available_foods = set(FOOD_PICKUP_POSITIONS)

        self.score_value = 0
        self.spawn_timer = 0
        self.elapsed_time = 0 
        self.game_started = False
        self.paused = False
        self.player_name = ""
        self.score_saved = False

        self.hud = HUD()

        self.game_over = False
        self.running = True

    def handle_events(self):
        #gestion des evenements du jeu
        mouse_position = pygame.Vector2(pygame.mouse.get_pos()) #postion de la souris

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_started and not self.game_over:
                        self.paused = not self.paused #mettre le jeu en pause / reprendre
                    else:
                        self.running = False

                elif event.key == pygame.K_RETURN and not self.game_started:
                    self.game_started = True #demarrer le jeu

                elif self.game_over and event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1] #corriger son pseudo

                elif (event.key == pygame.K_r and self.paused and not self.game_over):
                    self.restart() #recommnencer

                elif (event.key == pygame.K_r and self.game_over and event.mod & pygame.KMOD_CTRL):
                    self.restart() #recommencer avec controle r pour prendre en compte le r dans le pseudo

                elif self.game_over and event.key == pygame.K_RETURN:
                    self.save_score() #enregistrer dans le leaderboard

            if self.game_over and event.type == pygame.TEXTINPUT:
                if (event.text.isascii() and event.text.isalnum() and len(self.player_name) < 12):
                    self.player_name += event.text #rentrer son pseduo sans pouvoir injecter du code

            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_started and not self.paused and not self.game_over):
                projectile = self.player.shoot(mouse_position) #tirer si le joueur a de la nourriture
                if projectile:
                    self.projectiles.append(projectile) #ajouter le projectile à la liste pour le dessiner
                    self.sounds["throw"].play()

    def update(self, delta_time): #delta time pour garder les memes mouvements en changeant les fps
        if not self.game_started or self.paused or self.game_over: 
            return

        self.elapsed_time += delta_time #temps de jeu survécu

        self.player.update(pygame.Vector2(pygame.mouse.get_pos()), delta_time) #mettre a jour le joueur

        self.update_projectiles(delta_time)
        self.check_food_pickup()
        self.update_clients(delta_time)
        self.spawn_clients(delta_time)
        self.handle_client_collisions()

        if self.count_seated_clients() >= self.MAX_SEATED_CLIENTS: #detecter le game over
            self.game_over = True
            pygame.key.start_text_input()

    def check_food_pickup(self):
        if self.player.carried_food is not None: #detecter si le joueur a un item
            return 

        player_cell = (int(self.player.get_feet_position().x // TILE_SIZE), int(self.player.get_feet_position().y // TILE_SIZE)) #coordonnées de la hitbox du joueur

        for food_name, pickup_position in FOOD_PICKUP_POSITIONS.items():
            if (food_name in self.available_foods and player_cell == pickup_position): #verfie que le joueur est au bon endroit et que l'item a spwan
                self.player.carried_food = food_name
                self.available_foods.remove(food_name)
                self.sounds["pickup"].play()
                return

    def update_projectiles(self, delta_time):
        for projectile in self.projectiles:
            projectile.update(can_projectile_move_to, delta_time)

        active_projectiles = []
        for projectile in self.projectiles:
            if projectile.is_finished():
                self.available_foods.add(projectile.food_name) #detecter si le projectile a despawn et fait respawn l'item 
            else:
                active_projectiles.append(projectile) #ajouter le projectile lancé a la liste de projectiles lancés pour les afficher

        self.projectiles = active_projectiles #update les projectiles pour ne pas afficher ceux qui ont despawn

    def spawn_clients(self, delta_time):
        if not self.available_seats: 
            return

        self.spawn_timer += delta_time #temps depuis le dernier spawn de client
        delay = max(2, self.CLIENT_SPAWN_DELAY - self.elapsed_time // 30) #dimineur le delai de spawn toutes les 30 secondes et au minimum de 2 secondes
        if self.spawn_timer < delay: 
            return

        self.spawn_timer = 0
        entrance = random.choice(ENTRANCES)
        seat = random.choice(tuple(self.available_seats))
        self.available_seats.remove(seat) #eviter que le client s'assoit a une place occupée
        order = random.choice(FOOD_NAMES)
        path_to_seat = find_grid_path(entrance, seat) #chemin jusqu'a la table sans se prendre de collision
        path_to_entrance = find_grid_path(seat, entrance) #chemin jusqu'aux sorties sans se prendre de collision
        if not path_to_seat or not path_to_entrance: #si le client est bloqué il despawn et libere la place prevue
            self.available_seats.add(seat)
            return

        client = Client(
            position=grid_to_position(*entrance), #endroit de spawn du client
            seat_cell=seat, #place attibuée 
            image=self.client_image,
            order=order,
            path_to_seat=path_to_seat, #chemin prevu pour la place
            path_to_entrance=path_to_entrance, #chemin prevu pour la sortie
        )
        self.clients.append(client) #ajouter le client a la liste pour l'afficher

    def update_clients(self, delta_time):
        for client in self.clients:
            client.update(delta_time) 

        clients_that_left = [client for client in self.clients if client.has_left()] #detecter les clients qui partent pour les enlever de la liste

        for client in clients_that_left:
            self.clients.remove(client) #enlever de la liste
            self.available_seats.add(client.seat_cell) #liberer la place

    def count_seated_clients(self):
        return sum(client.is_seated for client in self.clients) #compter les clients assis

    def handle_client_collisions(self):
        projectiles_to_remove = [] #liste des projectiles qui ont touché un client les faire despawn

        for projectile in self.projectiles: 
            for client in self.clients:
                if not client.is_seated or not client.collides_with(projectile): #ne rien faire si le client n'est pas assis ou si l'item ne le touche pas
                    continue
                if client.order != projectile.food_name: #ne rien faire si le client n'a pas commandé l'item lancé
                    continue

                #si le client a commandé l'item et qu'il est assis
                client.serve() 
                projectiles_to_remove.append(projectile) #ajouter l'item a la liste des items a faire despawn
                self.available_foods.add(projectile.food_name) #ajouter l'item a la liste des items disponibles
                self.sounds["impact"].play()
                self.score_value += 100
                break

        self.projectiles = [projectile for projectile in self.projectiles if projectile not in projectiles_to_remove] #faire despawn les projectiles qui ont touché le client

    def restart(self):
        #recommencer le jeu en remettant tout a zero
        self.projectiles.clear()
        self.clients.clear()
        self.available_seats = set(SEATING_POSITIONS) - set(ENTRANCES)
        self.available_foods = set(FOOD_PICKUP_POSITIONS)
        self.player.carried_food = None
        self.score_value = 0
        self.spawn_timer = 0
        self.elapsed_time = 0
        self.player_name = ""
        self.score_saved = False
        self.game_started = True
        self.paused = False
        self.game_over = False

    def save_score(self):
        if self.score_saved or not self.player_name: #ne pas sauvegarder si deja sauvegardé ou si pas de pseudo
            return
        self.leaderboard.add(self.player_name, self.score_value)
        self.score_saved = True
        pygame.key.stop_text_input()

    def draw(self):
        #afficher les elements du jeu
        self.screen.blit(self.background, (0, 0))

        if not self.game_started: #afficher l'ecran de demarrage
            self.hud.draw_start_screen(self.screen) 
        elif self.game_over: #afficher l'ecran de game over
            self.hud.draw_game_over(
                self.screen,
                self.score_value,
                self.elapsed_time,
                self.count_seated_clients(),
                self.player_name,
                self.leaderboard.entries,
            )
        else: #sinon on est dans le jeu donc afficher le jeu
            if self.DEBUG_GRID: #afficher la grille de debug pour voir les collisions si acitvée
                draw_debug_grid(self.screen)

            draw_foods(self.screen, self.food_images, self.available_foods, self.food_label_font) #afficher aliments 

            for projectile in self.projectiles:
                projectile.draw(self.screen) #afficher les projectiles

            for client in self.clients:
                client.draw(self.screen, self.client_order_font) #afficher les clients

            self.player.draw_aiming_indicator(self.screen,pygame.mouse.get_pos()) #afficher la fleche pour viser
            self.player.draw(self.screen)
            self.hud.draw(self.screen, self.score_value, self.elapsed_time, self.count_seated_clients(), PLAYABLE_HEIGHT) #playable height pour ne pas que le hud recouvre le jeu
            if self.paused:
                self.hud.draw_pause(self.screen) #afficher menu pause

        pygame.display.flip() #mettre a jour l'affichage

    def run(self):
        while self.running:
            self.handle_events()
            delta_time = self.clock.tick(self.FPS) / 1000 #convertir le temps en secondes avec les fps pour garder les memes mouvements
            self.update(delta_time) #delta time sert a garder les memes mouvements en changeant les fps
            self.draw()