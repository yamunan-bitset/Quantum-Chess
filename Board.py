import pygame
from time import time

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)

        self.board = []
        self.squares = [[]]

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

        t0 = time()
        for i in range(8):
            for j in range(8):
                self.squares[i][j].draw()
            self.screen.blit(self.font.render(numbers[i], True, (183, 183, 183)), (2, i * 60 + 40))
            self.screen.blit(self.font.render(letters[i], True, (183, 183, 183)), (i * 60 + 40, 500))
        t1 = time()

        render_dt = t1 - t0
        self.screen.blit(self.font.render(f"{render_dt=} s", True, (183, 183, 183)), (500, 15))



class Square:
    def __init__(self, surface, rect, colour):
        self.surface = surface
        self.colour = colour
        self.rect = pygame.Rect(rect)
        self.selected = False

    def draw(self):
        pygame.draw.rect(self.surface, self.colour, self.rect)

