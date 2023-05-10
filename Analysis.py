
class Analysis:
    def __init__(self, board):
        self.board = board

        self.move_made = False
        self.prev_move = None

    def legal_moves(self, i, j):
        moves = []

        if self.board[i][j] == 0:
            # black pawn

            if self.board[i + 1][j] is None:
                moves.append((i + 1, j))
            if i == 1:
                if self.board[i + 2][j] is None:
                    moves.append((i + 2, j))
            if j != 7 and self.board[i + 1][j + 1] is not None and self.board[i + 1][j + 1] >= 6:
                moves.append((i + 1, j + 1))
            if j != 0 and self.board[i + 1][j - 1] is not None and self.board[i + 1][j - 1] >= 6:
                moves.append((i + 1, j - 1))
            if self.prev_move is not None:
                if self.board[self.prev_move[2]][self.prev_move[3]] == 6 and self.prev_move[0] == 6 and self.prev_move[2] == 4 and i == 4:
                    if self.prev_move[3] == j + 1:
                        moves.append((i + 1, j + 1, "epr"))
                    elif self.prev_move[3] == j - 1:
                        moves.append((i + 1, j - 1, "epl"))

        if self.board[i][j] == 6:
            # white pawn
            if self.board[i - 1][j] is None:
                moves.append((i - 1, j))
            if i == 6:
                if self.board[i - 2][j] is None:
                    moves.append((i - 2, j))
            if j != 0 and self.board[i - 1][j - 1] is not None and self.board[i - 1][j - 1] < 6:
                moves.append((i - 1, j - 1))
            if j != 7 and self.board[i - 1][j + 1] is not None and self.board[i - 1][j + 1] < 6:
                moves.append((i - 1, j + 1))
            if self.prev_move is not None:
                if self.board[self.prev_move[2]][self.prev_move[3]] == 0 and self.prev_move[0] == 1 and self.prev_move[2] == 3 and i == 3:
                    if self.prev_move[3] == j + 1:
                        moves.append((i - 1, j + 1, "epr"))
                    elif self.prev_move[3] == j - 1:
                        moves.append((i - 1, j - 1, "epl"))

        pass

        return moves

    def move(self, i0, j0, i1, j1):

        if (i1, j1) in self.legal_moves(i0, j0):
            temp = self.board[i0][j0]
            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 5
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 11

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "epr") in self.legal_moves(i0, j0):
            temp = self.board[i0][j0]

            self.board[i0][j0 + 1] = None

            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 5
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 11

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "epl") in self.legal_moves(i0, j0):
            temp = self.board[i0][j0]

            self.board[i0][j0 - 1] = None

            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 5
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 11

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True
        else:
            self.move_made = False

        return self.board
