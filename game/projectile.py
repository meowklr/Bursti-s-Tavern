import pygame

from game.constants import PROJECTILE_MAX_BOUNCES, PROJECTILE_RADIUS


class Projectile:
    def __init__(self, position, direction, image, speed, food_name): 
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction)
        self.image = image 
        self.food_name = food_name 
        self.speed = speed 
        self.radius = PROJECTILE_RADIUS #rayon utilisé pour les collisions
        self.bounce_count = 0
        self.max_bounces = PROJECTILE_MAX_BOUNCES 
        self.active = True #indique si le projectile est encore en jeu
        self.rotation = 0
        self.rotation_speed = 540 #vitesse de rotation

    def update(self, collision_checker, delta_time): #déplace le projectile et gère ses rebonds
        movement = self.direction * self.speed * delta_time 

        next_position = self.position.copy() #horizontal
        next_position.x += movement.x

        if collision_checker(next_position, self.radius): #avance si la prochaine position est libre
            self.position.x = next_position.x
        else:
            self.direction.x *= -1 #inverse la direction sur l'axe horizontal
            self.bounce_count += 1 #compte le rebond

        next_position = self.position.copy() #vertical
        next_position.y += movement.y

        if collision_checker(next_position, self.radius): #avance si la prochaine position est libre
            self.position.y = next_position.y
        else:
            self.direction.y *= -1 #inverse la direction sur l'axe vertical
            self.bounce_count += 1 #compte le rebond

        if self.bounce_count >= self.max_bounces: #termine le projectile après trop de rebonds
            self.active = False

        self.rotation = (self.rotation + self.rotation_speed * delta_time) % 360 #fait tourner l'aliment

    def is_finished(self): #indique si le projectile doit disparaître
        return not self.active

    def draw(self, screen): #affiche le projectile avec sa rotation actuelle
        rotated_image = pygame.transform.rotate(
            self.image,
            self.rotation,
        )
        projectile_rectangle = rotated_image.get_rect(
            center=self.position
        )
        screen.blit(rotated_image, projectile_rectangle)