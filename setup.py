import pygame, os
import player, planet

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

zoom_scale = 10




# initialize pygame and create window
def initialize():
    pygame.init()
    pygame.mixer.init()
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gravity Shoot (JK2020)")
    clock = pygame.time.Clock()

    # set up asset folders
    game_folder = os.path.dirname(__file__)
    global img_folder
    img_folder = os.path.join(game_folder, "img")
    print(img_folder)
    # Load all game graphics

    global background
    global background_rect
    global planet_img
    background = pygame.transform.scale(
        pygame.image.load(os.path.join(img_folder, "black.png")).convert(), (WIDTH, HEIGHT)    )
    background_rect = background.get_rect()
    player_img = pygame.image.load( os.path.join(img_folder, "playerShip1_blue.png") ).convert()
    planet_img = pygame.image.load( os.path.join(img_folder, "meteorBrown_big3.png") ).convert()



    global player1
    global player2
    global central_planet
    global all_sprites
    all_sprites = pygame.sprite.Group()
    player1 = player.Player(startX=WIDTH / 4 * 3 * zoom_scale, startY=HEIGHT / 2 + 50 * zoom_scale, my_mass=20, sprite_file="playerShip1_blue.png")
    player2 = player.Player(startX=WIDTH / 4 * 1 * zoom_scale, startY=HEIGHT / 2 - 50 * zoom_scale, my_mass=20, sprite_file="playerShip1_red.png")
    central_planet = planet.Planet(WIDTH / 2 * zoom_scale, HEIGHT / 2 * zoom_scale)

    all_sprites.add(player1)
    all_sprites.add(player2)
    all_sprites.add(central_planet)



def watch_keyboard(keystate):
    player1.acceleration = [0, 0]
    if keystate[pygame.K_LEFT]:
        player1.acceleration[0] = -1
    if keystate[pygame.K_RIGHT]:
        player1.acceleration[0] = 1
    if keystate[pygame.K_UP]:
        player1.acceleration[1] = -1
    if keystate[pygame.K_DOWN]:
        player1.acceleration[1] = 1

    player2.acceleration = [0, 0]
    if keystate[pygame.K_a]:
        player2.acceleration[0] = -1
    if keystate[pygame.K_d]:
        player2.acceleration[0] = 1
    if keystate[pygame.K_w]:
        player2.acceleration[1] = -1
    if keystate[pygame.K_s]:
        player2.acceleration[1] = 1

    if keystate[pygame.K_RIGHTBRACKET]:
        central_planet.mass *= 1.05
        print(central_planet.mass)
    if keystate[pygame.K_LEFTBRACKET]:
        central_planet.mass /= 1.05
        print(central_planet.mass)

    # if keystate[pygame.K_KP_PLUS] & (zoom_scale < 15):
    #     zoom_scale = zoom_scale + 1
    #     all_sprites.image = pygame.transform.scale( all_sprites.image, (5*zoom_scale, 5*zoom_scale) )
    # if keystate[pygame.K_KP_MINUS] & (zoom_scale > 2):
    #     zoom_scale -= 1
    #     all_sprites.image = pygame.transform.scale( all_sprites.image, (5*zoom_scale, 5*zoom_scale) )

