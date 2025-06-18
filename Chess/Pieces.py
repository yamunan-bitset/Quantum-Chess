import os
import pygame

pygame.mixer.init()

from . import Analysis

try:
    piece_imgs = [
        pygame.image.load(os.path.join("texture", "black", "pawn.png")),  # 0
        pygame.image.load(os.path.join("texture", "black", "rook.png")),  # 1
        pygame.image.load(os.path.join("texture", "black", "knight.png")),  # 2
        pygame.image.load(os.path.join("texture", "black", "bishop.png")),  # 3
        pygame.image.load(os.path.join("texture", "black", "king.png")),  # 4
        pygame.image.load(os.path.join("texture", "black", "queen.png")),  # 5
        pygame.image.load(os.path.join("texture", "white", "pawn.png")),  # 6
        pygame.image.load(os.path.join("texture", "white", "rook.png")),  # 7
        pygame.image.load(os.path.join("texture", "white", "knight.png")),  # 8
        pygame.image.load(os.path.join("texture", "white", "bishop.png")),  # 9
        pygame.image.load(os.path.join("texture", "white", "king.png")),  # 10
        pygame.image.load(os.path.join("texture", "white", "queen.png")),  # 11
    ]
except FileNotFoundError:
    try:
        piece_imgs = [
            pygame.image.load(os.path.join("..", "texture", "black", "pawn.png")),  # 0
            pygame.image.load(os.path.join("..", "texture", "black", "rook.png")),  # 1
            pygame.image.load(os.path.join("..", "texture", "black", "knight.png")),  # 2
            pygame.image.load(os.path.join("..", "texture", "black", "bishop.png")),  # 3
            pygame.image.load(os.path.join("..", "texture", "black", "king.png")),  # 4
            pygame.image.load(os.path.join("..", "texture", "black", "queen.png")),  # 5
            pygame.image.load(os.path.join("..", "texture", "white", "pawn.png")),  # 6
            pygame.image.load(os.path.join("..", "texture", "white", "rook.png")),  # 7
            pygame.image.load(os.path.join("..", "texture", "white", "knight.png")),  # 8
            pygame.image.load(os.path.join("..", "texture", "white", "bishop.png")),  # 9
            pygame.image.load(os.path.join("..", "texture", "white", "king.png")),  # 10
            pygame.image.load(os.path.join("..", "texture", "white", "queen.png")),  # 11
        ]
    except FileNotFoundError as e:
        print("Error: Wrong working directory", end="\n\n")
        print(e)


class Pieces:
    def __init__(self, screen, fen):
        self.screen = screen

        self.selected = None
        self.mouse_pos = None

        self.board = Pieces.load_fen(fen)
        self.superpos = Pieces.load_fen("8/8/8/8/8/8/8/8 w HAha - 0 1")
        self.analysis = Analysis(self.board, self.superpos)

        self.move = pygame.mixer.Sound(os.path.join("sfx", "move-self.mp3"))
        self.check = pygame.mixer.Sound(os.path.join("sfx", "move-check.mp3"))
        self.castle = pygame.mixer.Sound(os.path.join("sfx", "castle.mp3"))
        self.capture = pygame.mixer.Sound(os.path.join("sfx", "capture.mp3"))
        self.promotion = pygame.mixer.Sound(os.path.join("sfx", "promote.mp3"))
        self.game_end = pygame.mixer.Sound(os.path.join("sfx", "game-end.mp3"))

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
                if self.superpos[i][j] is not None:
                    self.screen.blit(piece_imgs[self.superpos[i][j]], (j * 60 + 15, i * 60 + 15))

                        
    def select(self, i, j):
        if i is None or j is None:
            return False
        if self.board[i][j] is not None:
            self.selected = (i, j)
            return True
        return False

    def drop(self, i, j, p):
        if i is not None and j is not None:
            self.board = self.analysis.move(*self.selected, i, j, promotion_f=p)
            self.selected = None
            if not self.analysis.move_made:
                return False

            if self.analysis.check_mate or self.analysis.stale_mate:
                pygame.mixer.Sound.play(self.game_end)
            elif self.analysis.b_king_in_check or self.analysis.w_king_in_check:
                pygame.mixer.Sound.play(self.check)
            elif self.analysis.promotion:
                pygame.mixer.Sound.play(self.promotion)
            elif self.analysis.captured:
                pygame.mixer.Sound.play(self.capture)
            elif self.analysis.castled:
                pygame.mixer.Sound.play(self.castle)
            else:
                pygame.mixer.Sound.play(self.move)

            return True

        self.selected = None
        return False
