import pygame

from game.projectile import Projectile


class Player:
    def __init__(self, position, idle_images, throw_images, food_images, projectile_speed, collision_checker): #initialise les valeurs du joueur
        self.position = pygame.Vector2(position) 
        self.idle_images = idle_images 
        self.throw_images = throw_images 
        self.food_images = food_images 
        self.projectile_speed = projectile_speed
        self.movement_speed = 300 
        self.collision_checker = collision_checker #fonction de collision de la carte
        self.feet_collision_width = 22 #largeur de la hitbox des pieds
        self.feet_collision_height = 12 #hauteur de la hitbox des pieds
        self.feet_offset_y = (self.idle_images["right"].get_height() / 2 - self.feet_collision_height / 2) #pour centrer le rectangle de collision des pieds sur le joueur
        self.carried_food = None #aliment actuellement porté

        self.facing_direction = "right" #direction du personnage
        self.animation_frame = 0 #image actuelle de l'animation
        self.animation_timer = 0 #temps depuis le dernier changement d'image
        self.animation_speed = 0.14 #durée d'affichage d'une image
        self.is_throwing = False #indique si l'animation de lancer est active

    def shoot(self, target_position): #crée un projectile vers la souris
        if self.carried_food is None: #impossible de lancer sans aliment
            return None

        self.update_facing_direction(target_position)

        launch_position = self.get_feet_position() #lance le projectile depuis les pieds
        direction = target_position - launch_position #calcule la direction du lancer

        if direction.length() == 0: #évite une direction nulle
            return None

        self.is_throwing = True #démarre l'animation de lancer
        self.animation_frame = 0 #revient à la première image
        self.animation_timer = 0 #réinitialise le temps de l'animation
        food_name = self.carried_food #mémorise l'aliment à lancer
        self.carried_food = None #retire l'aliment des mains du joueur

        if not self.collision_checker(launch_position, 20, 20): #fait spawn le projectile plus loin si le joueur est trop proche d'un mur
            for distance in range(4, 65, 4):
                candidate = launch_position - direction.normalize() * distance
                if self.collision_checker(candidate, 20, 20):
                    launch_position = candidate
                    break

        direction = target_position - launch_position 
        if direction.length() == 0:
            return None

        return Projectile(
            position=launch_position,
            direction=direction.normalize(),
            image=self.food_images[food_name],
            speed=self.projectile_speed,
            food_name=food_name,
        ) #renvoie le projectile créé avec les paramètres bons

    def update_facing_direction(self, target_position): #change la direction du joueur en fonction de la position de la souris
        if target_position.x < self.position.x:
            self.facing_direction = "left"
        else:
            self.facing_direction = "right"

    def update(self, target_position, delta_time): #déplace le joueur et actualise l'animation
        keys = pygame.key.get_pressed() 
        movement = pygame.Vector2(0, 0) #déplacement demandé

        if keys[pygame.K_z] or keys[pygame.K_UP]: 
            movement.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: 
            movement.y += 1
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            movement.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
            movement.x += 1

        if movement.length_squared() > 0: #déplace seulement si une touche est pressée
            movement = movement.normalize() #évite une vitesse diagonale plus élevée
            movement *= self.movement_speed * delta_time 

            next_position = self.position.copy()
            next_position.x += movement.x

            if self.collision_checker( #vérifie la collision avant le déplacement horizontal
                self.get_feet_position(next_position),
                self.feet_collision_width,
                self.feet_collision_height,
            ):
                self.position.x = next_position.x

            next_position = self.position.copy()
            next_position.y += movement.y

            if self.collision_checker( #vérifie la collision avant le déplacement vertical
                self.get_feet_position(next_position),
                self.feet_collision_width,
                self.feet_collision_height,
            ):
                self.position.y = next_position.y

        self.update_facing_direction(target_position) #suit la position de la souris

        if not self.is_throwing: #aucune animation à actualiser
            return

        self.animation_timer += delta_time #avance dans le temps de l'animation

        if self.animation_timer < self.animation_speed: #attend avant de changer d'image
            return

        self.animation_timer = 0
        self.animation_frame += 1 #passe à l'image suivante

        if self.animation_frame >= len( #termine l'animation après la dernière image
            self.throw_images[self.facing_direction]
        ):
            self.is_throwing = False
            self.animation_frame = 0

    def get_feet_position(self, position=None): #renvoie la position des pieds du joueur
        if position is None:
            position = self.position

        return pygame.Vector2(
            position.x,
            position.y + self.feet_offset_y,
        )

    def draw(self, screen): #affiche le joueur et l'aliment porté
        if self.is_throwing:
            image = self.throw_images[self.facing_direction][
                self.animation_frame
            ]
        else:
            image = self.idle_images[self.facing_direction]

        player_rectangle = image.get_rect(center=self.position)
        screen.blit(image, player_rectangle)

        if self.carried_food is not None: #affiche l'aliment au-dessus du joueur
            food_image = self.food_images[self.carried_food]
            food_rectangle = food_image.get_rect(
                center=(self.position.x, self.position.y - 65),
            )
            screen.blit(food_image, food_rectangle)

    def draw_aiming_indicator(self, screen, target_position): #affiche la flèche de visée
        direction = pygame.Vector2(target_position) - self.get_feet_position() #direction vers la souris
        if direction.length_squared() == 0:
            return

        direction = direction.normalize()
        start = self.get_feet_position() + direction * 14
        tip = start + direction * 30
        perpendicular = pygame.Vector2(-direction.y, direction.x)
        base_center = tip - direction * 10
        left_point = base_center + perpendicular * 6
        right_point = base_center - perpendicular * 6

        pygame.draw.line(
            screen,
            (255, 235, 120),
            start,
            base_center,
            3,
        )
        pygame.draw.polygon(
            screen,
            (255, 235, 120),
            (tip, left_point, right_point),
        )
