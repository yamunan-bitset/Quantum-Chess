import os
import pygame

from Chess import Pieces, Board

pygame.init()

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))


def main():
    board = Board(screen)

    startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    pieces = Pieces(screen, startpos)

    ignore = False

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                button = pygame.mouse
                pieces.mouse_pos = pos
                index = board.select(pos, pieces)
                if not pieces.select(*index):
                    board.unselect()
                    ignore = True
                else:
                    ignore = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if not ignore:
                    pos = pygame.mouse.get_pos()
                    button = pygame.mouse
                    pieces.mouse_pos = pos
                    index = board.drop(pos)
                    flag = None
                    if not pieces.drop(*index, board.get_promotions):
                        board.unselect()
                else:
                    ignore = False

        screen.fill((36, 34, 30))
        board.render(pieces.analysis)
        pieces.mouse_pos = pygame.mouse.get_pos()
        board.mouse_pos = pygame.mouse.get_pos()
        pieces.render()
        pygame.display.update()


if __name__ == "__main__":
    main()
