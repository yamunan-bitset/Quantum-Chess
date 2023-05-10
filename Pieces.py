import os
from time import time
import pygame
from pprint import pprint

piece_imgs = [
    pygame.image.load(os.path.join("texture", "black", "pawn.png")),
    pygame.image.load(os.path.join("texture", "black", "rook.png")),
    pygame.image.load(os.path.join("texture", "black", "knight.png")),
    pygame.image.load(os.path.join("texture", "black", "bishop.png")),
    pygame.image.load(os.path.join("texture", "black", "king.png")),
    pygame.image.load(os.path.join("texture", "black", "queen.png")),
    pygame.image.load(os.path.join("texture", "white", "pawn.png")),
    pygame.image.load(os.path.join("texture", "white", "rook.png")),
    pygame.image.load(os.path.join("texture", "white", "knight.png")),
    pygame.image.load(os.path.join("texture", "white", "bishop.png")),
    pygame.image.load(os.path.join("texture", "white", "king.png")),
    pygame.image.load(os.path.join("texture", "white", "queen.png")),
]


class Pieces:
    def __init__(self, screen, fen):
        self.screen = screen

        print(f"Loading fen {fen}")
        t0 = time()
        self.board = Pieces.load_fen(fen)
        t1 = time()
        print("Loaded fen: ")
        pprint(self.board)
        print(f"In {t1 - t0} s")

    @staticmethod
    def load_fen(fen):
        board = []
        for i in fen.split("/"):
            temp = []
            for j in i:
                if j == " ":
                    break
                if j in "12345678":
                    temp.extend([None] * int(j))
                else:
                    temp.append("prnbkqPRNBKQ".index(j))

            board.append(temp)
        return board

    def render(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    self.screen.blit(piece_imgs[self.board[i][j]], (j * 60 + 15, i * 60 + 15))


