import os
import pygame
import setup


def initialize_animation():
    global explosion_animation
    explosion_animation = []
    for i in range(9):
        filename = f'animatedExplosion0{i}.png'
        image = pygame.transform.scale(
            pygame.image.load(os.path.join(setup.img_folder, filename)).convert(), (75, 75))
        image.set_colorkey(setup.BLACK)
        explosion_animation.append(image)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, start_XY):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_animation[0]
        self.rect = self.image.get_rect()
        self.coords = start_XY
        self.rect.center = list(a1 / setup.zoom_scale for a1 in self.coords)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = setup.FPS * 1

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def Explode_player(player):
        global fire_explosion
        fire_explosion = Explosion(start_XY=player.coords)
        setup.all_sprites.add(fire_explosion)
        player.lost_life()
