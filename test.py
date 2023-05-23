from Analysis import Analysis
from Pieces import Pieces
from copy import deepcopy
from Board import Board
import os
import pygame

pygame.init()

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

board = Board(screen)

startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pos5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
pieces = Pieces(screen, pos5)
pieces.analysis.b_king_moved = True

startpos_actual_nodes = [1, 20, 400, 8902, 197281, 4865609, 119060324, 3195901860, 84998978956, 2439530234167, 69352859712417]
# Startpos test:
# depth 1, test node 20     ✔
# depth 2, test node 400    ✔
# depth 3, test node 8902   ✔
# depth 4, test node 197281 ✔

pos5_actual_nodes = [1, 44, 1486, 62379, 2103487, 89941194]
# Position 5 test:
# depth 1, test node 44     ✔
# depth 2, test node 1525   x
# depth 3, test node    x

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
        #pygame.time.wait(10)
        nodes += depth_test(n - 1, mboard, "b" if turn == "w" else "w")
        mboard = _board
        board.board = _board
        pieces.board = _board
        pieces.analysis.board = _board

    if log:
        print(f"{nodes=}")

    return nodes


screen.fill((36, 34, 30))

depth_test(2, Pieces.load_fen(pos5), "w", log=True)
