import sys
import pygame
import player as p
import utils
import random

pygame.init()

size = width, height = 1280, 720
black = 0, 0, 0
white = 255, 255, 255
red = 255, 100, 100

screen = pygame.display.set_mode(size)

view = [0, 0]
zoom = 1

player = p.Player(size)

clock = pygame.time.Clock()

font = pygame.font.SysFont("monospace", 16)
bigfont = pygame.font.SysFont("monospace", 64)

gamestate = "START"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if gamestate == "START":
                    gamestate = "PLAYING"
                if gamestate == "GAMEOVER":
                    player = p.Player(size)
                    gamestate = "PLAYING"
            if event.button == 4:
                zoom *= 1.1
            if event.button == 5:
                zoom /= 1.1

    """
    Updates and logic
    """
    dt = clock.tick() / 1000.0

    mov = pygame.mouse.get_rel()
    if (pygame.mouse.get_pressed()[0]):
        view[0] += mov[0] * 1 / zoom
        view[1] += mov[1] * 1 / zoom

    if gamestate == "PLAYING":
        player.update(dt)

    if gamestate == "GAMEOVER":
        player.update_gameover(dt)

    """
    Drawing
    """

    if (not pygame.key.get_pressed()[pygame.K_v]):
        screen.fill(black)

    # draw stars
    x = 0
    y = 0

    while x < width:
        while y < height:
            realx = int(view[0] + x)
            realy = int(view[1] + y)
            if utils.randint_seeded(realx * realy, 0, 100) > 90:
                pygame.draw.circle(screen, white, (realx, realy), 0)
            y += 20
        y = 0
        x += 20

    # screens
    if player.size > 75:
        gamestate = "GAMEOVER"
    if player.pos[0] < -player.size * 2 or player.pos[1] < -player.size * 2 or \
        player.pos[0] > width + player.size * 2 or player.pos[1] > height + player.size * 2:
        gamestate = "GAMEOVER"

    if gamestate == "START":
        game_name = "ASTEROID AVERSION"

        random.seed(pygame.time.get_ticks())
        if random.randint(0, 100) > 90:
            game_name_list = list(game_name)
            game_name_list[random.randint(0, len(game_name) - 1)] = random.choice(list("%_$?"))
            game_name = "".join(game_name_list)


        nametext = bigfont.render(game_name, 0, (20, 240, 10))
        screen.blit(nametext, (width / 2 - bigfont.size(game_name)[0] / 2, 200))

        start_str = "click anywhere to start"
        start_text = font.render(start_str, 0, (20, 240, 10))
        screen.blit(start_text, (width / 2 - font.size(start_str)[0] / 2, 300))

    if gamestate == "PLAYING":
        player.draw(screen, view, font)

    if gamestate == "GAMEOVER":
        player.draw(screen, view, font)

        gameover_str = "GAME OVER"
        gameover_text = bigfont.render(gameover_str, 0, (20, 240, 10))
        screen.blit(gameover_text, (width / 2 - bigfont.size(gameover_str)[0] / 2, 200))

        again = "Click to play again"
        again_text = font.render(again, 0, (20, 240, 10))
        screen.blit(again_text, (width / 2 - font.size(again)[0] / 2, 300))



    pygame.display.flip()
