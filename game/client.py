import pygame

from game.constants import (CLIENT_FADE_DURATION, CLIENT_LEAVING_SPEED, CLIENT_RADIUS, CLIENT_SPEED, FOOD_LABELS)
from game.map import TILE_SIZE


class Client: #gere les valeurs de chaque client, leur position, leur état et leur animation
    def __init__(
        self,
        position,
        seat_cell,
        image,
        order,
        path_to_seat,
        path_to_entrance,
    ):
        self.position = pygame.Vector2(position)
        self.seat_cell = seat_cell
        self.image = image
        self.order = order
        self.path_to_seat = path_to_seat
        self.path_to_entrance = path_to_entrance
        self.path_index = 1 #commence à 1 car le client est déjà à la position 0
        self.speed = CLIENT_SPEED
        self.leaving_speed = CLIENT_LEAVING_SPEED
        self.fade_duration = CLIENT_FADE_DURATION
        self.fade_elapsed = 0
        self.state = "walking_to_table"
        self.radius = CLIENT_RADIUS

    @property #retourne True si le client est assis sous forme de variable avec @poperty
    def is_seated(self):
        return self.state == "seated"

    @property #retourne True si le client est en train de partir sous forme de variable avec @poperty
    def is_leaving(self):
        return self.state == "leaving"

    def update(self, delta_time):
        #met a jour la position du client en fonction de son état et de son chemin
        speed = self.speed
        if self.is_leaving:
            speed = self.leaving_speed
            path = self.path_to_entrance
            self.fade_elapsed += delta_time #fait diparaitre le client en fondu 
        else:
            path = self.path_to_seat

        if self.path_index >= len(path): #si le client a atteint sa place
            if self.is_leaving and self.fade_elapsed >= self.fade_duration: #fait despawn le cleitn
                self.state = "gone"
            elif not self.is_leaving:
                self.state = "seated"
            return

        target = pygame.Vector2(path[self.path_index]) #position cible du client
        target = target * TILE_SIZE + pygame.Vector2(TILE_SIZE / 2, TILE_SIZE / 2) #convertit la position de la grille en position de pixel

        distance = target - self.position
        if distance.length() <= speed * delta_time: #sert a faire avancer le client vers sa position cible
            self.position = target
            self.path_index += 1
            if self.path_index >= len(path): #si le client a atteint sa place
                if self.is_leaving and self.fade_elapsed >= self.fade_duration:
                    self.state = "gone" 
                elif not self.is_leaving:
                    self.state = "seated"
            return

        self.position += distance.normalize() * speed * delta_time #fait avancer le client

    def serve(self):
        if self.is_seated:
            self.state = "leaving"
            self.path_index = 1
            self.fade_elapsed = 0

    def has_left(self):
        return self.state == "gone"

    def collides_with(self, projectile):
        return self.position.distance_to(projectile.position) <= (self.radius + projectile.radius) #verifie si le projectile touche le client

    def draw(self, screen, font): #affiche le client sur l'écran
        rectangle = self.image.get_rect(center=self.position)
        if self.is_leaving:
            opacity = max(0, round(255 * (1 - self.fade_elapsed / self.fade_duration))) #fait disparaitre le client en fondu
            fading_image = self.image.copy()
            fading_image.set_alpha(opacity)
            screen.blit(fading_image, rectangle)
        else:
            screen.blit(self.image, rectangle)

        if self.is_leaving:
            return
        if not self.is_seated:
            return

        display_order = FOOD_LABELS[self.order]
        order_text = font.render(display_order, False, (255, 238, 150))
        outline = font.render(display_order, False, (0, 0, 0))
        text_rectangle = order_text.get_rect(midbottom=(round(self.position.x), rectangle.top - 3)) #affiche le texte de la commande du cleint

        for offset_x, offset_y in (
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1),
        ): #ajoute un contour au texte de la commande
            screen.blit(outline, text_rectangle.move(offset_x, offset_y))
        screen.blit(order_text, text_rectangle)
