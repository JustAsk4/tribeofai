#
# My first real game project with Python
# (c) JustAsk 2019-2020
#
import setup
from setup import *

setup.initialize()
# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # keep loop running at the right speed
    clock.tick(setup.FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        running = False
    setup.watch_keyboard(keystate)

    # Update

    setup.all_sprites.update()

    # Draw / render
    setup.screen.fill(setup.BLACK)
    setup.screen.blit(setup.background, setup.background_rect)
    setup.all_sprites.draw(setup.screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame
