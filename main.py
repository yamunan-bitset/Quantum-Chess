import os
import pygame

pygame.init()
print()

import Pieces
import Board

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

board = Board.Board(screen)
pieces = Pieces.Pieces(screen, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

win_open = True
while win_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_open = False
            break

    screen.fill((36, 34, 30))
    board.render()
    pieces.render()
    pygame.display.update()
