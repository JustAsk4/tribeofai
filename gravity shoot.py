#
# Pirmas mano zaidimas su Pythonu
# (c) JustAsk
#
import pygame
import random
import os
import math

WIDTH = 1400
HEIGHT = 800
FPS = 60
GRAVITY = 6.6740831  /10**1 #*10^−11 #m3⋅kg−1⋅s−2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Shoot (JK2017)")
clock = pygame.time.Clock()


# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
# Load all game graphics
background = pygame.transform.scale(   pygame.image.load(os.path.join(img_folder, 'black.png')).convert()  , (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_blue.png')).convert()
planet_img = pygame.image.load(os.path.join(img_folder, 'meteorBrown_big3.png')).convert()
zoomScale = 10


class Player(pygame.sprite.Sprite):
    def __init__(self, startX, startY, myMass, spriteFile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(  pygame.image.load(os.path.join(img_folder, spriteFile)).convert(),   (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coords = [startX, startY]
        self.rect.center = list(a1/zoomScale for a1 in self.coords)

        self.mass = myMass
        self.speedXY = [0, 0]
        self.maxSpeedXY = [100, 100]
        self.speedScale = 1/1
        self.acceleration = [0, 0]
        self.force = [0, 0]
        self.cross = False

    def update(self):
        #change acceleration vector



        # self.coords = self.rect.center
        distance = math.sqrt(  (centralPlanet.coords[0]-self.coords[0])**2 + (centralPlanet.coords[1]-self.coords[1])**2   )
        if distance < centralPlanet.minOrbit:
            forceSize = 0
        else:
            forceSize = GRAVITY * self.mass * centralPlanet.mass / (distance**2)

        self.force = [(a1-a2)/distance*forceSize for a1,a2 in zip(centralPlanet.coords, self.coords)]
        self.acceleration = [a1+a2/self.mass for a1,a2 in zip(self.acceleration, self.force)]

        #calc new speed, limit maxmin
        self.speedXY = [a1+a2 for a1,a2 in zip(self.speedXY, self.acceleration)]
        self.speedXY = [(max(0,   min( abs(a1),   a2 ))
                        * math.copysign(1, a1)) for a1,a2 in zip(self.speedXY, self.maxSpeedXY)]

        self.coords = [(a1+a2/self.speedScale) for a1,a2 in zip(self.coords, self.speedXY)]
        # self.rect.center = [(a1+a2/self.speedScale) for a1,a2 in zip(self.rect.center, self.speedXY)]

        # if [a1-a2 for a1,a2 in zip(centralPlanet.coords, self.coords)] == (0,0):


        # if ((centralPlanet.coords[0]-self.coords[0])==0):
        #     self.coords[0] = self.coords[0] + 1
        # if ((centralPlanet.coords[1]-self.coords[1])==0):
        #     self.coords[1] = self.coords[1] + 1

        self.rect.center = list(a1/zoomScale for a1 in self.coords)
        # self.coords = self.rect.center


        #check boundaries
        if self.rect.left > WIDTH:
            self.rect.right = 0
            self.cross = True
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.cross = True
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.cross = True
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
            self.cross = True

        if self.cross:
            self.coords = [a1*zoomScale for a1 in self.rect.center]
            self.cross = False







class Planet(pygame.sprite.Sprite):
    def __init__(self, startX, startY):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(planet_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coords = [startX, startY]
        self.rect.center = list(a1/zoomScale for a1 in self.coords)

        self.mass = 3 * 10**6  #5.972 × 10^24

        self.speedXY = [0, 0]
        self.maxSpeedXY = [25, 25]
        self.speedScale = 1
        self.acceleration = [0, 0]
        self.minOrbit = 800

    def update(self):
        #change acceleration vector
        self.acceleration = [0, 0]



def ListenKeyboard():
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
        centralPlanet.mass += 100000
        print (centralPlanet.mass)
    if keystate[pygame.K_LEFTBRACKET]:
        centralPlanet.mass -= 100000
        print (centralPlanet.mass)

    # if keystate[pygame.K_KP_PLUS] & (zoomScale < 15):
    #     zoomScale = zoomScale + 1
    #     all_sprites.image = pygame.transform.scale( all_sprites.image, (5*zoomScale, 5*zoomScale) )
    # if keystate[pygame.K_KP_MINUS] & (zoomScale > 2):
    #     zoomScale -= 1
    #     all_sprites.image = pygame.transform.scale( all_sprites.image, (5*zoomScale, 5*zoomScale) )
 

all_sprites = pygame.sprite.Group()
player1 = Player(WIDTH / 4*3 *zoomScale, HEIGHT / 2 +50  *zoomScale,  20, "playerShip1_blue.png")
player2 = Player(WIDTH / 4*1 *zoomScale, HEIGHT / 2 -50  *zoomScale,  20, "playerShip1_red.png")
centralPlanet = Planet(WIDTH / 2 *zoomScale, HEIGHT / 2   *zoomScale)

all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(centralPlanet)


# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        running = False
    ListenKeyboard()

    # Update

    all_sprites.update()




    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()




pygame
