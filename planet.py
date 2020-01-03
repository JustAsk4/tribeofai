import pygame
import setup


class Planet(pygame.sprite.Sprite):
    def __init__(self, central_x, central_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(setup.planet_img, (70, 70))
        self.image.set_colorkey(setup.BLACK)
        self.rect = self.image.get_rect()
        self.coords = [central_x, central_y]
        self.rect.center = list(coord / setup.zoom_scale for coord in self.coords)

        self.mass = 5.972 * 10 ** 6  # 5.972 × 10^24

        self.speed_XY = [0, 0]
        self.max_speed_XY = [25, 25]
        self.speed_scale = 1
        self.acceleration = [0, 0]
        self.min_orbit = 800

    def update(self):
        self.acceleration = [0, 0]
