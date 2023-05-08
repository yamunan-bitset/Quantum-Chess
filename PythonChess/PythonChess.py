"""
from StockfishAPI import test
test()
"""
import pygame
pygame.init()

from Board import Board

import threading

logo = pygame.image.load("texture\\black\\knight.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess")

screen = pygame.display.set_mode((800, 640))
screen.fill((100, 100, 100))

font = pygame.font.SysFont(None, 36)

board = Board(screen, 8, 8)
thread = threading.Thread(target=board.c_play, daemon=True)
thread.start()

win_open = True
while win_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            board.quit = True
            board.thread.kill()
            thread.join()
            win_open = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            button = pygame.mouse
            board.select(pos)

    screen.fill((100, 100, 100))

    board.render()
    
    evaluation = font.render("Eval: " + board.thread.pos_eval, True, (50, 50, 200))
    screen.blit(evaluation, (640, 0))
    
    pygame.display.update()

