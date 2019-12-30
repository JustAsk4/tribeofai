import pygame, os, math
import setup, planet


class Player(pygame.sprite.Sprite):
    def __init__(self, startX, startY, my_mass, sprite_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(setup.img_folder, sprite_file)).convert(), (50, 50)
        )
        self.image.set_colorkey(setup.BLACK)
        self.rect = self.image.get_rect()
        self.coords = [startX, startY]
        self.rect.center = list(a1 / setup.zoom_scale for a1 in self.coords)

        self.mass = my_mass
        self.speed_XY = [0, 0]
        self.max_speed_XY = [100, 100]
        self.speed_scale = 1 / 1
        self.acceleration = [0, 0]
        self.force = [0, 0]
        self.cross = False



    def distance_to_planet(self):
        return math.sqrt(
            (setup.central_planet.coords[0] - self.coords[0]) ** 2 +
            (setup.central_planet.coords[1] - self.coords[1]) ** 2
        )


    def force_size(self):
        if self.distance_to_planet() < setup.central_planet.min_orbit:
            return 0
        else:
            return setup.GRAVITY * self.mass * setup.central_planet.mass / (self.distance_to_planet() ** 2)

    def update(self):
        # change acceleration vector
        self.force = [(coord_planet - coord_my) / self.distance_to_planet() * self.force_size()
                       for coord_planet, coord_my in zip(setup.central_planet.coords, self.coords)]
        self.acceleration = [current_accel + new_force/self.mass
                             for current_accel, new_force in zip(self.acceleration, self.force)]

        self.speed_XY = [current_speed+current_accel for current_speed, current_accel in zip(self.speed_XY, self.acceleration)]
        # calculated new speed, but limit by maxmin
        self.speed_XY = [(max(0, min(abs(current_speed), max_speed)) * math.copysign(1, current_speed))
                         for current_speed, max_speed in zip(self.speed_XY, self.max_speed_XY)]

        self.coords = [(a1 + a2 / self.speed_scale) for a1, a2 in zip(self.coords, self.speed_XY)]
        self.rect.center = list(coord / setup.zoom_scale for coord in self.coords)

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

        if self.cross:
            self.coords = [a1 * setup.zoom_scale for a1 in self.rect.center]
            self.cross = False
