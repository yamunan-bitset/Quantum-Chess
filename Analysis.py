
class Analysis:
    def __init__(self, board):
        self.board = board

        self.move_made = False

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

            self.move_made = True
        else:
            self.move_made = False

        return self.board
