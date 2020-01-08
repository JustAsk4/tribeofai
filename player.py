import math
import os
import pygame
import random
from pygame.math import Vector2

import explosion
import setup

player_side_choice = {'left': -1, 'right': 1}


class Player(pygame.sprite.Sprite):
    def __init__(self, my_name, start_side, my_mass, sprite_file, speed_xy=[0, 0]):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(setup.img_folder, sprite_file)).convert(), (50, 50))
        self.original_image = self.image
        self.mini_img = pygame.transform.rotate(pygame.transform.scale(self.original_image, (25, 19)), 180)
        self.mini_img.set_colorkey(setup.BLACK)

        self.image.set_colorkey(setup.BLACK)
        self.rect = self.image.get_rect()
        self.side_LR = player_side_choice.get(start_side)
        self.coords = (random.randrange((4 + self.side_LR * 2) / 8 * setup.WIDTH,
                                        (4 + self.side_LR * 4) / 8 * setup.WIDTH,
                                        step=self.side_LR) * setup.zoom_scale,
                       random.randrange(setup.HEIGHT) * setup.zoom_scale)
        self.rect.center = list(a1 / setup.zoom_scale for a1 in self.coords)

        self.name = my_name
        self.mass = my_mass
        self.speed_xy = speed_xy
        self.max_speed_XY = (100, 100)
        self.speed_scale = 1 / 1
        self.acceleration = [0, 0]
        self.force_vector = [0, 0]
        self.direction = Vector2(0, 1)  # A unit vector pointing upward.
        self.angle = 0
        self.last_shot_time = 0
        self.lives = 3
        self.cross = False
        self.hidden = False
        self.hide_timer = 0

    def check_explosion(self):
        if self.distance_to_planet() < 500:
            explosion.Explode_player(self)

    def lost_life(self):
        if self.lives > 1:
            self.lives -= 1
        else:
            print(f'-rip- {self.name} lost this round.')
            self.lives = 0
        self.hide()

    def hide(self):
        self.hidden = True
        self.image = pygame.transform.scale(self.image, (1, 1))
        self.hide_timer = pygame.time.get_ticks()
        self.coords = (setup.WIDTH * setup.zoom_scale + 50, setup.HEIGHT * setup.zoom_scale + 50)
        self.speed_xy = (0, 0)

    def unhide(self):
        self.hidden = False
        self.image = self.original_image
        self.coords = (
            random.randrange((4 + self.side_LR * 2) / 8 * setup.WIDTH,
                             (4 + self.side_LR * 4) / 8 * setup.WIDTH,
                             step=self.side_LR) * setup.zoom_scale,
            random.randrange(setup.HEIGHT) * setup.zoom_scale)

    def draw_lives(self, surf):
        for i in range(self.lives):
            img_rect = self.mini_img.get_rect()
            img_rect.x = (4 + self.side_LR * 3.5) / 8 * setup.WIDTH + 30 * self.side_LR * i
            img_rect.y = 5
            surf.blit(self.mini_img, img_rect)

    def check_cross_boundary(self):
        'check for crossing screen boundaries'
        if self.rect.left > setup.WIDTH:
            self.rect.right = 0
            self.cross = True
        if self.rect.right < 0:
            self.rect.left = setup.WIDTH
            self.cross = True
        if self.rect.top > setup.HEIGHT:
            self.rect.bottom = 0
            self.cross = True
        if self.rect.bottom < 0:
            self.rect.top = setup.HEIGHT
            self.cross = True

    def distance_to_planet(self):
        return math.sqrt(sum([(setup.central_planet.coords[i] - self.coords[i]) ** 2 for i in range(2)]))

    def force_size(self):
        if self.distance_to_planet() < setup.central_planet.min_orbit:
            return 0.01
        else:
            return setup.GRAVITY * self.mass * setup.central_planet.mass / (self.distance_to_planet() ** 2)

    def change_acceleration_vector(self):
        self.force_vector = [(coord_planet - coord_my) / self.distance_to_planet() * self.force_size()
                             for coord_planet, coord_my in zip(setup.central_planet.coords, self.coords)]
        self.direction = Vector2(0, 1)
        self.direction.rotate_ip(self.angle)
        self.acceleration = [self.acceleration[1] * current_direction + new_force / self.mass
                             for current_direction, new_force in zip(self.direction, self.force_vector)]

    def change_speed_vector(self):
        self.speed_xy = [current_speed + accel for current_speed, accel in zip(self.speed_xy, self.acceleration)]
        self.speed_xy = [(max(0, min(abs(current_speed), max_speed)) * math.copysign(1, current_speed))
                         for current_speed, max_speed in zip(self.speed_xy, self.max_speed_XY)]


    def update(self):
        self.check_explosion()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.unhide()

        self.change_acceleration_vector()
        self.change_speed_vector()

        if not self.hidden:
            self.coords = [(a1 + a2 / self.speed_scale) for a1, a2 in zip(self.coords, self.speed_xy)]
            self.rect.center = list(coord / setup.zoom_scale for coord in self.coords)
            self.image = pygame.transform.rotate(self.original_image, -self.angle)

        self.draw_lives(setup.screen)
        self.check_cross_boundary()

        if self.cross and not self.hidden:
            self.coords = [a1 * setup.zoom_scale for a1 in self.rect.center]
            self.cross = False
