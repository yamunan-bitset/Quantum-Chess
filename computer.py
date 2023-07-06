import os
import pygame

from Chess import Pieces, Board
from Widgets import Button, Label

pygame.init()

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))


def main():
    font = pygame.font.SysFont(None, 30)
    label = Label(screen, font, "Please select your side", (183, 183, 183), 200, 50, 600, 50)
    black = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "Black", (183, 183, 183), 200, 200, 600, 50)
    white = Button(screen, (180, 20, 10), (180, 80, 10), (10, 75, 20), font, "White", (183, 183, 183), 200, 300, 600, 50)
    colour = None

    while True:
        event = pygame.event.wait()
        pos = pygame.mouse.get_pos()
        if black.handle_event(event, pos):
            colour = "b"
        if white.handle_event(event, pos):
            colour = "w"

        if colour is not None:
            break

        screen.fill((36, 34, 30))
        label.render()
        black.render()
        white.render()
        pygame.display.update()

    play(colour)


def play(colour):
    board = Board(screen)

    startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    pieces = Pieces(screen, "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -")

    ignore = False
    playing = True

    while True:
        if playing:
            if pieces.analysis.turn == colour:
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
            else:
                move = pieces.analysis.find_best(4, 0, 100)[1]
                if move is not None:
                    move = [*move[:2], *move[2]]
                    board.auto_select(move[0], move[1], pieces)
                    pieces.select(move[0], move[1])
                    board.auto_drop(move[2], move[3])
                    pieces.drop(move[2], move[3], lambda colour: move[4])

            if pieces.analysis.check_mate or pieces.analysis.stale_mate:
                playing = False
        else:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break


        screen.fill((36, 34, 30))
        board.render(pieces.analysis)
        pieces.mouse_pos = pygame.mouse.get_pos()
        board.mouse_pos = pygame.mouse.get_pos()
        pieces.render()
        pygame.display.update()


if __name__ == "__main__":
    play("w")
