import pygame
from math import floor

from . import Pieces


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 30)

        self.squares = [[]]

        self.selected = None
        self.selected2 = None
        self.mouse_pos = None

        self.legal = []

        self.draw = False
        self.white_offers_draw = False
        self.black_offers_draw = False
        self.white_resign = False
        self.black_resign = False
        self.white_aborted = False
        self.black_aborted = False

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

    def render(self, analysis):
        letters = "abcdefgh"
        numbers = "12345678"

        for i in range(8):
            for j in range(8):
                self.squares[i][j].check = False
                if analysis.board[i][j] == 10:
                    if analysis.w_king_in_check:
                        self.squares[i][j].check = True
                    else:
                        self.squares[i][j].check = False
                elif analysis.board[i][j] == 4:
                    if analysis.b_king_in_check:
                        self.squares[i][j].check = True
                    else:
                        self.squares[i][j].check = False

                self.squares[i][j].draw()
            self.screen.blit(self.font.render(numbers[i], True, (183, 183, 183)), (2, i * 60 + 40))
            self.screen.blit(self.font.render(letters[i], True, (183, 183, 183)), (i * 60 + 40, 500))

        if self.mouse_pos is not None:
            x = floor((self.mouse_pos[0] - 15) / 60) * 60
            y = floor(self.mouse_pos[1] / 60) * 60
            if 0 <= x / 60 <= 7 and 0 <= y / 60 <= 7:
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x + 15, y + 15, 60, 60), 2)

        analysis.evaluate()
        self.screen.blit(self.font.render("Eval: " + str(round(analysis.evaluation, 2)), True, (183, 183, 183)), (540, 15))

        if analysis.turn == "w":
            pygame.draw.circle(self.screen, (255, 255, 255), (520, 475), 10)
        else:
            pygame.draw.circle(self.screen, (255, 255, 255), (520, 25), 11)
            pygame.draw.circle(self.screen, (0, 0, 0), (520, 25), 10)

        if analysis.check_mate:
            colour = ""
            if analysis.turn == "b":
                colour = "White won, 1-0"
            else:
                colour = "Black won, 0-1"

            self.screen.blit(self.font.render("Check mate", True, (183, 183, 183)), (540, 50))
            self.screen.blit(self.font.render(colour, True, (183, 183, 183)), (540, 75))

        if analysis.stale_mate:
            self.screen.blit(self.font.render("Stale mate", True, (183, 183, 183)), (540, 50))
            self.screen.blit(self.font.render("Draw 1/2-1/2", True, (183, 183, 183)), (540, 75))

        if self.white_offers_draw:
            self.screen.blit(self.font.render("White offers draw", True, (183, 183, 183)), (540, 100))

        if self.black_offers_draw:
            self.screen.blit(self.font.render("Black offers draw", True, (183, 183, 183)), (540, 125))

        if self.draw or (self.white_offers_draw and self.black_offers_draw):
            self.screen.blit(self.font.render("Draw offer accepted", True, (183, 183, 183)), (540, 50))
            self.screen.blit(self.font.render("Draw 1/2-1/2", True, (183, 183, 183)), (540, 75))

        if self.white_resign:
            self.screen.blit(self.font.render("White resigned", True, (183, 183, 183)), (540, 50))
            self.screen.blit(self.font.render("Black won, 0-1", True, (183, 183, 183)), (540, 75))

        if self.black_resign:
            self.screen.blit(self.font.render("Black resigned", True, (183, 183, 183)), (540, 50))
            self.screen.blit(self.font.render("White won, 1-0", True, (183, 183, 183)), (540, 75))

        if self.white_aborted:
            self.screen.blit(self.font.render("White left the match", True, (183, 183, 183)), (540, 50))
            self.screen.blit(self.font.render("Black won, 0-1", True, (183, 183, 183)), (540, 75))

        if self.black_aborted:
            self.screen.blit(self.font.render("Black left the match", True, (183, 183, 183)), (540, 50))
            self.screen.blit(self.font.render("White won, 1-0", True, (183, 183, 183)), (540, 75))

    def get_promotions(self, colour):
        flag = None

        promotion_surface = pygame.Surface((1000, 800))

        while True:
            event = pygame.event.wait()
            pos = pygame.mouse.get_pos()
            x = floor((pos[0] - 15) / 60)
            y = floor((pos[1] - 30) / 60)
            if event.type == pygame.MOUSEBUTTONUP:
                if x == 0 and y == 8:
                    flag = "q"
                    break
                elif x == 1 and y == 8:
                    flag = "r"
                    break
                elif x == 2 and y == 8:
                    flag = "k"
                    break
                elif x == 3 and y == 8:
                    flag = "b"
                    break
                else:
                    continue
            if event.type == pygame.QUIT:
                exit(0)

            promotion_surface.fill((36, 34, 30))

            if x == 0 and y == 8:
                pygame.draw.rect(promotion_surface, (50, 120, 100), pygame.Rect(15, 515, 60, 60))
            elif x == 1 and y == 8:
                pygame.draw.rect(promotion_surface, (50, 120, 100), pygame.Rect(75, 515, 60, 60))
            elif x == 2 and y == 8:
                pygame.draw.rect(promotion_surface, (50, 120, 100), pygame.Rect(135, 515, 60, 60))
            elif x == 3 and y == 8:
                pygame.draw.rect(promotion_surface, (50, 120, 100), pygame.Rect(195, 515, 60, 60))

            if colour == "w":
                promotion_surface.blit(Pieces.piece_imgs[11], (15, 515))
                promotion_surface.blit(Pieces.piece_imgs[7], (75, 515))
                promotion_surface.blit(Pieces.piece_imgs[8], (135, 515))
                promotion_surface.blit(Pieces.piece_imgs[9], (195, 515))
            else:
                promotion_surface.blit(Pieces.piece_imgs[5], (15, 515))
                promotion_surface.blit(Pieces.piece_imgs[1], (75, 515))
                promotion_surface.blit(Pieces.piece_imgs[2], (135, 515))
                promotion_surface.blit(Pieces.piece_imgs[3], (195, 515))

            self.screen.blit(promotion_surface, (0, 0))

            pygame.display.update()

        return flag

    def select(self, pos, pieces):
        x = floor((pos[1]) / 60)
        y = floor((pos[0] - 15) / 60)

        if x < 0 or x > 7 or y < 0 or y > 7:
            return None, None

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

    def auto_select(self, x, y, pieces):
        if self.selected is not None and self.selected2 is not None:
            self.squares[self.selected[0]][self.selected[1]].selected = False
            self.squares[self.selected2[0]][self.selected2[1]].selected = False

        self.selected2 = None

        self.squares[x][y].selected = True
        self.selected = (x, y)

        return self.selected

    def unselect(self):
        if self.selected is not None:
            self.squares[self.selected[0]][self.selected[1]].selected = False
            self.selected = None
        if self.selected2 is not None:
            self.squares[self.selected2[0]][self.selected2[1]].selected = False
            self.selected2 = None

    def drop(self, pos):
        x = floor((pos[1] - 15) / 60)
        y = floor((pos[0]) / 60)

        if x > 7 or y > 7 or x < 0 or y < 0:
            self.squares[self.selected[0]][self.selected[1]].selected = False
            return None, None

        for i in self.legal:
            self.squares[i[0]][i[1]].moveable = False

        self.legal = []

        self.squares[x][y].selected = True
        self.selected2 = (x, y)

        return self.selected2

    def auto_drop(self, x, y):
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
        self.check = False
        self.moveable = False

    def draw(self):
        if self.selected:
            self.curr_colour = (42, 64, 83)
        else:
            self.curr_colour = self.colour

        if self.check:
            self.curr_colour = (92, 11, 6)

        pygame.draw.rect(self.surface, self.curr_colour, self.rect)

        if self.moveable:
            image = pygame.Surface([60, 60], pygame.SRCALPHA, 32)
            image = image.convert_alpha()
            image.fill((152, 105, 29, 150))
            self.surface.blit(image, (self.rect.x, self.rect.y))
