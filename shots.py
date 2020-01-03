import math
import os
import pygame
import time

import explosion
import setup


class Laser_shot(pygame.sprite.Sprite):
    def __init__(self, start_XY, my_mass, new_id_number, sprite_file, speed_XY, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(setup.img_folder, sprite_file)).convert(), (5, 15))
        self.image = pygame.transform.rotate(self.image, -angle)

        self.image.set_colorkey(setup.BLACK)
        self.rect = self.image.get_rect()
        self.coords = start_XY
        self.rect.center = list(a1 / setup.zoom_scale for a1 in self.coords)

        self.id_number = new_id_number
        self.mass = my_mass
        self.speed_XY = speed_XY
        self.max_speed_XY = [100, 100]
        self.speed_scale = 1 / 1
        self.acceleration = [0, 0]
        self.angle = angle
        self.cross = False

    def distance_to_planet(self):
        return math.sqrt(sum([(setup.central_planet.coords[i] - self.coords[i]) ** 2 for i in range(2)]))

    def distance_to_player(self, player):
        return math.sqrt(sum([(player.coords[i] - self.coords[i]) ** 2 for i in range(2)]))

    def check_explosion(self):
        if self.distance_to_planet() < 500:
            print(f'Planet hit.')
            self.expired_shot()

        for check_player in setup.players:
            if self.distance_to_player(check_player) < 300:
                print(f'Player {check_player.name} exploded.')
                self.expired_shot()
                explosion.Explode_player(check_player)

    def expired_shot(self):
        try:
            setup.all_sprites.remove(self)
            setup.shots_on_screen.remove(self)
        except:
            print(f'FAILED on index {self.id_number}')

    def check_cross_boundary(self):
        # check boundaries
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

    def force_size(self):
        if self.distance_to_planet() < setup.central_planet.min_orbit:
            return 0
        else:
            return setup.GRAVITY * self.mass * setup.central_planet.mass / (self.distance_to_planet() ** 2)

    def update(self):
        self.check_explosion()

        self.coords = [(a1 + a2 / self.speed_scale) for a1, a2 in zip(self.coords, self.speed_XY)]
        self.rect.center = list(coord / setup.zoom_scale for coord in self.coords)

        self.check_cross_boundary()
        if self.cross:
            self.expired_shot()


def Shoot_from_player(player):
    next_in_list = len(setup.shots_on_screen)
    if next_in_list < 15:
        setup.shots_on_screen.append(Laser_shot(
            start_XY=[player.coords[i] + player.direction[i] * 400 + player.speed_XY[i] * 1 for i in range(2)],
            my_mass=0.01, new_id_number=next_in_list, sprite_file="laserBlue07.png",
            speed_XY=[player.direction[i] * 100 + player.speed_XY[i] / 2 for i in range(2)],
            angle=player.angle))
        setup.all_sprites.add(setup.shots_on_screen[next_in_list])
        player.last_shot_time = time.time()
