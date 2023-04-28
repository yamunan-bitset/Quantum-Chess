import pygame
pygame.init()

from Board import Board

logo = pygame.image.load("texture\\black\\knight.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess")

screen = pygame.display.set_mode((800, 640))
screen.fill((100, 100, 100))

board = Board(screen, 8, 8)

win_open = True
while win_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_open = False
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            button = pygame.mouse
            board.select(pos)

    board.render()

    pygame.display.update()

