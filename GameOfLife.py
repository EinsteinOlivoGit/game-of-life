import pygame
import numpy as np
import time

pygame.init()
width, height = 1200, 700

screen = pygame.display.set_mode((width, height))

bg = 43, 43, 43

screen.fill(bg)

nx, ny = 43, 25

dimCW = width / nx
dimCH = height / ny

game_state = np.zeros((nx, ny))

game_state[21, 21] = 1
game_state[22, 22] = 1
game_state[22, 23] = 1
game_state[21, 23] = 1
game_state[20, 23] = 1

pause = False

while True:

    new_game_state = np.copy(game_state)
    screen.fill(bg)
    time.sleep(0.1)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN:
            pause = not pause
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
            new_game_state[celX, celY] = not mouseClick[2]

    for y in range(0, ny):
        for x in range(0, nx):
            if not pause:
                n_neigh = game_state[(x - 1) % nx, (y - 1) % ny] + \
                          game_state[(x - 1) % nx, y % ny] + \
                          game_state[(x - 1) % nx, (y + 1) % ny] + \
                          game_state[x % nx, (y - 1) % ny] + \
                          game_state[x % nx, (y + 1) % ny] + \
                          game_state[(x + 1) % nx, (y - 1) % ny] + \
                          game_state[(x + 1) % nx, y % ny] + \
                          game_state[(x + 1) % nx, (y + 1) % ny]

                # Regla #1: Si una célula está muerta y tiene tres vecinas vivas, nace.
                if game_state[x, y] == 0 and n_neigh == 3:
                    new_game_state[x, y] = 1
                # Regla #2: Si una célula está viva y tiene menos de dos más de tres vecinas vivas, muere.
                elif game_state[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    new_game_state[x, y] = 0
                # Regla #1: Si una célula está viva y tiene dos o tres vecinas vivas, sobrevive
                else:
                    pass

            square = [(x * dimCW, y * dimCH),
                      ((x+1) * dimCW, y * dimCH),
                      ((x+1) * dimCW, (y+1) * dimCH),
                      (x * dimCW, (y+1) * dimCH)]
            if new_game_state[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), square, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), square, 0)

    game_state = np.copy(new_game_state)

    pygame.display.flip()
