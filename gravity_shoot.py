#
# My first real-time graphics game project with Python
# (c) JustAsk 2019-2020
#
import setup
from setup import *

setup.initialize()
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(setup.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        running = False
    setup.watch_keyboard(keystate)

    for check_player in setup.players:
        if check_player.lives == 0 and not explosion.fire_explosion.alive():
            running = False

    setup.screen.fill(setup.BLACK)
    setup.screen.blit(setup.background, setup.background_rect)
    setup.all_sprites.update()

    setup.all_sprites.draw(setup.screen)
    pygame.display.flip()

pygame.quit()
