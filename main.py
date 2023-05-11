import sys

import pygame
from pygame.locals import *
import constants

pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Killers Plants")

#Variable que decide cuando se acaba el juego
gameOver = True

while gameOver:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("a - izquierda")
            if event.key == pygame.K_d:
                print("d - derecha")
            if event.key == pygame.K_w:
                print("w - arriba")
            if event.key == pygame.K_s:
                print("s - abajo")
    pygame.display.update()
