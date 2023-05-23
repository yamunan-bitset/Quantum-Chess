import os
import pygame
from pprint import pprint

import Analysis

piece_imgs = [
    pygame.image.load(os.path.join("texture", "black", "pawn.png")),    # 0
    pygame.image.load(os.path.join("texture", "black", "rook.png")),    # 1
    pygame.image.load(os.path.join("texture", "black", "knight.png")),  # 2
    pygame.image.load(os.path.join("texture", "black", "bishop.png")),  # 3
    pygame.image.load(os.path.join("texture", "black", "king.png")),    # 4
    pygame.image.load(os.path.join("texture", "black", "queen.png")),   # 5
    pygame.image.load(os.path.join("texture", "white", "pawn.png")),    # 6
    pygame.image.load(os.path.join("texture", "white", "rook.png")),    # 7
    pygame.image.load(os.path.join("texture", "white", "knight.png")),  # 8
    pygame.image.load(os.path.join("texture", "white", "bishop.png")),  # 9
    pygame.image.load(os.path.join("texture", "white", "king.png")),    # 10
    pygame.image.load(os.path.join("texture", "white", "queen.png")),   # 11
]


class Pieces:
    def __init__(self, screen, fen):
        self.screen = screen

        self.selected = None
        self.mouse_pos = None

        self.board = Pieces.load_fen(fen)
        self.analysis = Analysis.Analysis(self.board)

        self.promotion = False

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
        if i is None or j is None:
            return False
        if self.board[i][j] is not None:
            self.selected = (i, j)
            legal_moves = self.analysis.legal_moves(i, j)
            for move in legal_moves:
                for i in move:
                    if isinstance(i, str):
                        if "p" in i:
                            self.promotion = True
            return True
        return False

    def drop(self, i, j, flag=None):
        if i is not None and j is not None:
            self.board = self.analysis.move(*self.selected, i, j, flag=flag)
            self.selected = None
            if not self.analysis.move_made:
                return False

            self.promotion = False
            return True

        self.selected = None
        return False

