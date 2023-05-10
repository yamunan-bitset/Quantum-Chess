import os
import pygame
from pprint import pprint

import Analysis

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

        self.selected = None
        self.mouse_pos = None

        print(f"Loading fen {fen}")
        self.board = Pieces.load_fen(fen)
        self.analysis = Analysis.Analysis(self.board)
        pprint(self.board)

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
                    if self.selected != (i, j):
                        self.screen.blit(piece_imgs[self.board[i][j]], (j * 60 + 15, i * 60 + 15))
                    else:
                        self.screen.blit(piece_imgs[self.board[i][j]], (self.mouse_pos[0] - 30, self.mouse_pos[1] - 30))

    def select(self, i, j):
        if self.board[i][j] is not None:
            self.selected = (i, j)
            return True
        return False

    def drop(self, i, j):
        if i is not None and j is not None:
            self.board = self.analysis.move(*self.selected, i, j)
            self.selected = None
            if not self.analysis.move_made:
                return False
            return True

        self.selected = None
        return False

