import os
import pygame
import time

import explosion
import planet
import player
import shots

WIDTH = 1400
HEIGHT = 800
FPS = 60
GRAVITY = 6.6740831 / 10 ** 1  # *10^−11 #m3⋅kg−1⋅s−2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

global zoom_scale
zoom_scale = 10
min_time_between_shots = 0.5


def initialize():
    pygame.init()
    pygame.mixer.init()
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Gravity Shoot (JK2020)')

    # set up image folders
    game_folder = os.path.dirname(__file__)
    global img_folder
    img_folder = os.path.join(game_folder, 'img')
    print(f'{img_folder} loaded.')
    print(f'Controls: ←↑→↓ with RCTRL    and    AWSD with LSHIFT')

    # load all game graphics
    global background
    background = pygame.transform.scale(pygame.image.load(
        os.path.join(img_folder, 'black.png')).convert(), (WIDTH, HEIGHT))
    global background_rect
    background_rect = background.get_rect()
    global planet_img
    planet_img = pygame.image.load(
        os.path.join(
            img_folder,
            'meteorBrown_big3.png')).convert()

    global all_sprites
    all_sprites = pygame.sprite.Group()
    global players
    players = []
    players.append(
        player.Player(
            'Player1',
            start_side='right',
            my_mass=20,
            sprite_file='playerShip1_blue.png'))
    players.append(
        player.Player(
            'Player2',
            start_side='left',
            my_mass=20,
            sprite_file='playerShip1_red.png'))
    global central_planet
    central_planet = planet.Planet(
        central_x=WIDTH / 2 * zoom_scale,
        central_y=HEIGHT / 2 * zoom_scale)

    all_sprites.add(players[0])
    all_sprites.add(players[1])
    all_sprites.add(central_planet)

    global shots_on_screen
    shots_on_screen = []
    explosion.initialize_animation()


def watch_keyboard(keystate):
    players[0].acceleration = [0, 0]
    if keystate[pygame.K_LEFT]:
        players[0].angle -= 3
    if keystate[pygame.K_RIGHT]:
        players[0].angle += 3
    if keystate[pygame.K_UP]:
        players[0].acceleration[1] = 1
    if keystate[pygame.K_DOWN]:
        players[0].acceleration[1] = -1
    if keystate[pygame.K_RCTRL]:
        if time.time() - players[0].last_shot_time > min_time_between_shots:
            shots.Shoot_from_player(players[0])

    players[1].acceleration = [0, 0]
    if keystate[pygame.K_a]:
        players[1].angle -= 3
    if keystate[pygame.K_d]:
        players[1].angle += 3
    if keystate[pygame.K_w]:
        players[1].acceleration[1] = 1
    if keystate[pygame.K_s]:
        players[1].acceleration[1] = -1
    if keystate[pygame.K_LSHIFT]:
        if time.time() - players[1].last_shot_time > min_time_between_shots:
            shots.Shoot_from_player(players[1])

    if keystate[pygame.K_RIGHTBRACKET]:
        central_planet.mass *= 1.05
        print(central_planet.mass)
    if keystate[pygame.K_LEFTBRACKET]:
        central_planet.mass /= 1.05
        print(central_planet.mass)
