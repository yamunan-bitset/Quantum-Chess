import pygame
import os
from math import floor
from pprint import pprint

from StockfishAPI import get_next_fen, play_best, Eval

piece_imgs = {
    "bp": pygame.image.load("texture\\black\\pawn.png"),
    "bR": pygame.image.load("texture\\black\\rook.png"),
    "bN": pygame.image.load("texture\\black\\knight.png"),
    "bB": pygame.image.load("texture\\black\\bishop.png"),
    "bK": pygame.image.load("texture\\black\\king.png"),
    "bQ": pygame.image.load("texture\\black\\queen.png"),
    "wp": pygame.image.load("texture\\white\\pawn.png"),
    "wR": pygame.image.load("texture\\white\\rook.png"),
    "wN": pygame.image.load("texture\\white\\knight.png"),
    "wB": pygame.image.load("texture\\white\\bishop.png"),
    "wK": pygame.image.load("texture\\white\\king.png"),
    "wQ": pygame.image.load("texture\\white\\queen.png"),
}

for i in piece_imgs:
    piece_imgs[i] = pygame.transform.scale(piece_imgs[i], (80, 80))

l = "abcdefgh"

C_COLOUR = "b"
P_COLOUR = "w"

class Board:
    def __init__(self, surface, cols, rows):
        self.surface = surface
        self.squares = [[]]

        self.cols = cols
        self.rows = rows

        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.load_fen(self.fen)

        self.selected_square = (None, None)
        self.selected_square_2 = (None, None)
        self.moves = []
        self.half_move = False
        
        self.thread = Eval(self.fen)
        self.thread.start()

        self.check_square = (None, None)

        for i in range(self.cols):
            self.squares.append([])
            for j in range(self.rows):
                self.squares[i].append(
                    Square(
                        self.surface, 
                        (j * 80, i * 80, 80, 80), 
                        (226, 204, 180) if (i + j) % 2 == 0 else (159, 115, 95)
                    )
                )

    def render(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.squares[i][j].draw()
                
                if self.board[i][j] == "--":
                    continue
                
                if self.thread.pos_eval == "+":
                    if self.board[i][j] == self.fen.split(" ")[1] + "K":
                        self.squares[i][j].colour = (100, 0, 0)
                        self.check_square = (i, j)
                self.surface.blit(piece_imgs[self.board[i][j]], (j * 80, i * 80))

    def c_play(self):
        if self.fen.split(" ")[1] == C_COLOUR:
            c_move = play_best(self.fen, self.moves, 5000)
            self.moves.append(c_move)
            self.squares[self.selected_square[0]][self.selected_square[1]].colour = (226, 204, 180) if (self.selected_square[0] + self.selected_square[1]) % 2 == 0 else (159, 115, 95)
            self.squares[self.selected_square[0]][self.selected_square[1]].selected = False
            self.squares[self.selected_square_2[0]][self.selected_square_2[1]].colour = (226, 204, 180) if (self.selected_square_2[0] + self.selected_square_2[1]) % 2 == 0 else (159, 115, 95)
            self.squares[self.selected_square_2[0]][self.selected_square_2[1]].selected = False
            self.selected_square = (8 - int(c_move[1]), l.index(c_move[0]))
            self.selected_square_2 = (8 - int(c_move[3]), l.index(c_move[2]))
            self.squares[self.selected_square[0]][self.selected_square[1]].colour = (100, 255, 100)
            self.squares[self.selected_square[0]][self.selected_square[1]].selected = True
            self.squares[self.selected_square_2[0]][self.selected_square_2[1]].colour = (100, 255, 100)
            self.squares[self.selected_square_2[0]][self.selected_square_2[1]].selected = True
            move = get_next_fen(self.fen, self.moves)
            self.load_fen(move)
            if self.check_square != (None, None):
                self.squares[self.check_square[0]][self.check_square[1]].colour = (226, 204, 180) if (self.check_square[0] + self.check_square[1]) % 2 == 0 else (159, 115, 95)
            pprint(self.board)

            self.thread.load_fen(self.fen)
                    


    def select(self, position):
        x = floor(position[1]/80)
        y = floor(position[0]/80)

        if self.half_move:
            temp = l[y]
            temp += str(8 - x)
            self.squares[x][y].colour = (100, 255, 100)
            self.squares[x][y].selected = True
            self.selected_square_2 = (x, y)
            self.moves[len(self.moves)-1] += temp
            print(self.moves)
            move = get_next_fen(self.fen, self.moves)
            if move is None:
                self.squares[self.selected_square[0]][self.selected_square[1]].colour = (226, 204, 180) if (self.selected_square[0] + self.selected_square[1]) % 2 == 0 else (159, 115, 95)
                self.squares[self.selected_square[0]][self.selected_square[1]].selected = False
                self.squares[self.selected_square_2[0]][self.selected_square_2[1]].colour = (226, 204, 180) if (self.selected_square_2[0] + self.selected_square_2[1]) % 2 == 0 else (159, 115, 95)
                self.squares[self.selected_square_2[0]][self.selected_square_2[1]].selected = False
                self.selected_square = (None, None)
                self.selected_square_2 = (None, None)
                self.moves.pop()
                self.half_move = False
                return
            self.load_fen(move)
            if self.check_square != (None, None):
                self.squares[self.check_square[0]][self.check_square[1]].colour = (226, 204, 180) if (self.check_square[0] + self.check_square[1]) % 2 == 0 else (159, 115, 95)
            pprint(self.board)
            self.half_move = False
            self.thread.load_fen(self.fen)
        else:
            if self.squares[x][y].selected == False:
                if self.board[x][y] != "--":
                    #if self.board[x][y][0] == self.fen.split(" ")[1]:
                    if self.board[x][y][0] == P_COLOUR:
                        self.squares[x][y].selected = True
                        self.squares[x][y].colour = (100, 255, 100)
                        if self.selected_square != (None, None):
                            self.squares[self.selected_square[0]][self.selected_square[1]].colour = (226, 204, 180) if (self.selected_square[0] + self.selected_square[1]) % 2 == 0 else (159, 115, 95)
                            self.squares[self.selected_square[0]][self.selected_square[1]].selected = False
                        if self.selected_square_2 != (None, None):
                            self.squares[self.selected_square_2[0]][self.selected_square_2[1]].colour = (226, 204, 180) if (self.selected_square_2[0] + self.selected_square_2[1]) % 2 == 0 else (159, 115, 95)
                            self.squares[self.selected_square_2[0]][self.selected_square_2[1]].selected = False
                        self.selected_square = (x, y)
                        self.moves.append(l[y] + str(8 - x))
                        self.half_move = True
                        
            else:
                self.squares[x][y].colour = (159, 115, 95) if (x + y) % 2 == 0 else (226, 204, 180)
                self.squares[x][y].selected = False


    def unselect_all(self):
        for i in range(self.cols):
            for j in range(self.rows):
                self.squares[i][j].colour = (159, 115, 95) if (i + j) % 2 == 0 else (226, 204, 180)
                self.squares[i][j].selected = False

    def load_fen(self, fen):
        self.fen = fen

        self.board = []
        for row in self.fen.split('/'):
            brow = []
            for c in row:
                if c == " ":
                    break
                if c in '12345678':
                    brow.extend(['--'] * int(c))
                elif c == 'p':
                    brow.append('bp')
                elif c == 'P':
                    brow.append('wp')
                elif c > 'Z':
                    brow.append('b'+c.upper())
                else:
                    brow.append('w'+c)

            self.board.append(brow)
            

class Square:
    def __init__(self, surface, rect, colour):
        self.surface = surface
        self.colour = colour
        self.rect = pygame.Rect(rect)
        self.selected = False
        
    def draw(self):
        pygame.draw.rect(self.surface, self.colour, self.rect)




