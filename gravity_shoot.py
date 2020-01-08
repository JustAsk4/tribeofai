#
# My first real-time graphics game project with Python
# (c) JustAsk 2019-2020
#
import setup
from setup import *


def game_loop():
    clock.tick(setup.FPS)
    global game_running
    global lives_left
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        game_running = False
    setup.watch_keyboard(keystate)

    for check_player in setup.players:
        if check_player.lives == 0 and lives_left:
            lives_left = False
            setup.total_score[1 - setup.players.index(check_player)] += 1

    setup.screen.fill(setup.BLACK)
    setup.screen.blit(setup.background, setup.background_rect)
    setup.all_sprites.update()

    setup.all_sprites.draw(setup.screen)
    pygame.display.flip()


clock = pygame.time.Clock()
game_running = True
setup.initialize()
while game_running:
    setup.create_players()
    lives_left = True

    while game_running and (lives_left or explosion.fire_explosion.alive()):
        game_loop()

    if game_running:
        setup.score_display()



pygame.quit()
