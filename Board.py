import pygame
from math import floor


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)

        self.squares = [[]]

        self.selected = None
        self.selected2 = None

        self.legal = []

        for i in range(8):
            self.squares.append([])
            for j in range(8):
                self.squares[i].append(
                    Square(
                        self.screen,
                        (j * 60 + 15, i * 60 + 15, 60, 60),
                        (89, 147, 93) if (i + j) % 2 == 1 else (241, 246, 178)
                    )
                )

    def render(self):
        letters = "abcdefgh"
        numbers = "12345678"

        for i in range(8):
            for j in range(8):
                self.squares[i][j].draw()
            self.screen.blit(self.font.render(numbers[i], True, (183, 183, 183)), (2, i * 60 + 40))
            self.screen.blit(self.font.render(letters[i], True, (183, 183, 183)), (i * 60 + 40, 500))

    def select(self, pos, pieces):
        x = floor(pos[1] / 60)
        y = floor(pos[0] / 60)

        if self.selected is not None and self.selected2 is not None:
            self.squares[self.selected[0]][self.selected[1]].selected = False
            self.squares[self.selected2[0]][self.selected2[1]].selected = False

        self.selected2 = None

        self.squares[x][y].selected = True
        self.selected = (x, y)

        self.legal = pieces.analysis.legal_moves(x, y)
        for i in self.legal:
            self.squares[i[0]][i[1]].moveable = True

        return self.selected

    def unselect(self):
        if self.selected is not None:
            self.squares[self.selected[0]][self.selected[1]].selected = False
            self.selected = None
        if self.selected2 is not None:
            self.squares[self.selected2[0]][self.selected2[1]].selected = False
            self.selected2 = None


    def drop(self, pos):
        x = floor(pos[1] / 60)
        y = floor(pos[0] / 60)

        if x > 8 or y > 8:
            self.squares[self.selected[0]][self.selected[1]].selected = False
            return None, None

        for i in self.legal:
            self.squares[i[0]][i[1]].moveable = False

        self.legal = []

        self.squares[x][y].selected = True
        self.selected2 = (x, y)

        return self.selected2


class Square:
    def __init__(self, surface, rect, colour):
        self.surface = surface
        self.colour = colour
        self.curr_colour = self.colour
        self.rect = pygame.Rect(rect)
        self.selected = False
        self.moveable = False

    def draw(self):
        if self.selected:
            self.curr_colour = (42, 64, 83)
        else:
            self.curr_colour = self.colour

        if self.moveable:
            self.curr_colour = (208, 77, 0)
        else:
            self.curr_colour = self.colour

        pygame.draw.rect(self.surface, self.curr_colour, self.rect)
