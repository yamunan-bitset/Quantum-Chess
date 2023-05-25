import sys
import os
import pygame
pygame.init()

from time import time
from copy import deepcopy

sys.path.insert(0, "..")
from Chess import Pieces
from Chess import Board


logo = pygame.image.load(os.path.join("..", "texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

board = Board(screen)

startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pos2 = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -"
pos3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -"
pos4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
pos5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
pos6 = "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10"

#######
DEPTH = 3
POS = startpos
#######

pieces = Pieces(screen, POS)


def depth_test(n, mboard, turn, log=False):
    if n == 0:
        return 1

    if log:
        print(f"Depth {n=}, No of Nodes", end=" ")

    legal_moves = []
    for x in range(8):
        for y in range(8):
            if mboard[x][y] is not None:
                if (turn == "w" and mboard[x][y] >= 6) or (turn == "b" and mboard[x][y] < 6):
                    pieces.analysis.turn = turn
                    moves = pieces.analysis.legal_moves(x, y)
                    if moves == []:
                        continue
                    for i in moves:
                        legal_moves.append((x, y, i))

    nodes = 0
    for move in legal_moves:
        _board = deepcopy(mboard)
        mboard = pieces.analysis.depth(*move, board=mboard)
        board.board = mboard
        pieces.board = mboard
        pieces.analysis.board = mboard
        screen.fill((36, 34, 30))
        board.render(pieces.analysis)
        pieces.render()
        pygame.display.update()
        # pygame.event.wait()
        nodes += depth_test(n - 1, mboard, "b" if turn == "w" else "w")
        mboard = _board
        board.board = _board
        pieces.board = _board
        pieces.analysis.board = _board

    if log:
        print(f"{nodes=}")

    return nodes


screen.fill((36, 34, 30))

t0 = time()
depth_test(DEPTH, Pieces.load_fen(POS), "w", log=True)
t1 = time()
print(f"Time taken: {t1 - t0} s")
