
class Analysis:
    def __init__(self, board):
        self.board = board

        self.turn = "w"

        self.move_made = False
        self.prev_move = None

        # TODO: Castling into check
        self.b_rook1_moved = False
        self.w_rook1_moved = False
        self.b_rook2_moved = False
        self.w_rook2_moved = False
        self.b_king_moved = False
        self.w_king_moved = False

        self.evaluation = 0
        self.evaluate()

    def evaluate(self):
        self.evaluation = 0
        for i in self.board:
            for j in i:
                if j is not None:
                    if j == 0:
                        self.evaluation -= 1
                    elif j == 1:
                        self.evaluation -= 5
                    elif j == 2 or j == 3:
                        self.evaluation -= 3
                    elif j == 5:
                        self.evaluation -= 9
                    elif j == 6:
                        self.evaluation += 1
                    elif j == 7:
                        self.evaluation += 5
                    elif j == 8 or j == 9:
                        self.evaluation += 3
                    elif j == 11:
                        self.evaluation += 9


    def legal_moves(self, i, j):
        moves = []

        if self.board[i][j] is None:
            return moves

        if self.board[i][j] < 6 and self.turn == "w":
            return moves
        if self.board[i][j] >= 6 and self.turn == "b":
            return moves

        # TODO: Pieces movements: Ensure pieces don't cause check
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

        if self.board[i][j] == 1:
            # black rook
            for _j in range(7 - j):
                if self.board[i][j + _j + 1] is not None:
                    if self.board[i][j + _j + 1] >= 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if self.board[i][j - _j - 1] is not None:
                    if self.board[i][j - _j - 1] >= 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if self.board[i + _i + 1][j] is not None:
                    if self.board[i + _i + 1][j] >= 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if self.board[i - _i - 1][j] is not None:
                    if self.board[i - _i - 1][j] >= 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

        if self.board[i][j] == 7:
            # white rook
            for _j in range(7 - j):
                if self.board[i][j + _j + 1] is not None:
                    if self.board[i][j + _j + 1] < 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if self.board[i][j - _j - 1] is not None:
                    if self.board[i][j - _j - 1] < 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if self.board[i + _i + 1][j] is not None:
                    if self.board[i + _i + 1][j] < 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if self.board[i - _i - 1][j] is not None:
                    if self.board[i - _i - 1][j] < 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

        if self.board[i][j] == 3:
            # black bishop
            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if self.board[i + k + 1][j + k + 1] is not None:
                    if self.board[i + k + 1][j + k + 1] >= 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if self.board[i - k - 1][j - k - 1] is not None:
                    if self.board[i - k - 1][j - k - 1] >= 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if self.board[i + k + 1][j - k - 1] is not None:
                    if self.board[i + k + 1][j - k - 1] >= 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if self.board[i - k - 1][j + k + 1] is not None:
                    if self.board[i - k - 1][j + k + 1] >= 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        if self.board[i][j] == 9:
            # white bishop
            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if self.board[i + k + 1][j + k + 1] is not None:
                    if self.board[i + k + 1][j + k + 1] < 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if self.board[i - k - 1][j - k - 1] is not None:
                    if self.board[i - k - 1][j - k - 1] < 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if self.board[i + k + 1][j - k - 1] is not None:
                    if self.board[i + k + 1][j - k - 1] < 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if self.board[i - k - 1][j + k + 1] is not None:
                    if self.board[i - k - 1][j + k + 1] < 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        if self.board[i][j] == 5:
            # black queen
            for _j in range(7 - j):
                if self.board[i][j + _j + 1] is not None:
                    if self.board[i][j + _j + 1] >= 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if self.board[i][j - _j - 1] is not None:
                    if self.board[i][j - _j - 1] >= 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if self.board[i + _i + 1][j] is not None:
                    if self.board[i + _i + 1][j] >= 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if self.board[i - _i - 1][j] is not None:
                    if self.board[i - _i - 1][j] >= 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if self.board[i + k + 1][j + k + 1] is not None:
                    if self.board[i + k + 1][j + k + 1] >= 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if self.board[i - k - 1][j - k - 1] is not None:
                    if self.board[i - k - 1][j - k - 1] >= 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if self.board[i + k + 1][j - k - 1] is not None:
                    if self.board[i + k + 1][j - k - 1] >= 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if self.board[i - k - 1][j + k + 1] is not None:
                    if self.board[i - k - 1][j + k + 1] >= 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        if self.board[i][j] == 11:
            # white queen
            for _j in range(7 - j):
                if self.board[i][j + _j + 1] is not None:
                    if self.board[i][j + _j + 1] < 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if self.board[i][j - _j - 1] is not None:
                    if self.board[i][j - _j - 1] < 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if self.board[i + _i + 1][j] is not None:
                    if self.board[i + _i + 1][j] < 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if self.board[i - _i - 1][j] is not None:
                    if self.board[i - _i - 1][j] < 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if self.board[i + k + 1][j + k + 1] is not None:
                    if self.board[i + k + 1][j + k + 1] < 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if self.board[i - k - 1][j - k - 1] is not None:
                    if self.board[i - k - 1][j - k - 1] < 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if self.board[i + k + 1][j - k - 1] is not None:
                    if self.board[i + k + 1][j - k - 1] < 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if self.board[i - k - 1][j + k + 1] is not None:
                    if self.board[i - k - 1][j + k + 1] < 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        # TODO: King movements: Check, Checkmate, Castle into checks, Run into checks, In front of king
        if self.board[i][j] == 4:
            # black king
            if not self.b_king_moved and not self.b_rook1_moved:
                if self.board[0][5] is None and self.board[0][6] is None:
                    moves.append((0, 7, "b0-0"))
            if not self.b_king_moved and not self.b_rook2_moved:
                if self.board[0][3] is None and self.board[0][2] is None and self.board[0][1] is None:
                    moves.append((0, 0, "b0-0-0"))

            if i + 1 <= 7:
                if self.board[i + 1][j] is None:
                    moves.append((i + 1, j))
                else:
                    if self.board[i + 1][j] >= 6:
                        moves.append((i + 1, j))

            if i - 1 >= 0:
                if self.board[i - 1][j] is None:
                    moves.append((i - 1, j))
                else:
                    if self.board[i - 1][j] >= 6:
                        moves.append((i - 1, j))

            if j + 1 <= 7:
                if self.board[i][j + 1] is None:
                    moves.append((i, j + 1))
                else:
                    if self.board[i][j + 1] >= 6:
                        moves.append((i, j + 1))

            if j - 1 >= 0:
                if self.board[i][j - 1] is None:
                    moves.append((i, j - 1))
                else:
                    if self.board[i][j - 1] >= 6:
                        moves.append((i, j - 1))

            if i + 1 <= 7 and j + 1 <= 7:
                if self.board[i + 1][j + 1] is None:
                    moves.append((i + 1, j + 1))
                else:
                    if self.board[i + 1][j + 1] >= 6:
                        moves.append((i + 1, j + 1))

            if i + 1 <= 7 and j - 1 >= 0:
                if self.board[i + 1][j - 1] is None:
                    moves.append((i + 1, j - 1))
                else:
                    if self.board[i + 1][j - 1] >= 6:
                        moves.append((i + 1, j - 1))

            if i - 1 >= 0 and j - 1 >= 0:
                if self.board[i - 1][j - 1] is None:
                    moves.append((i - 1, j - 1))
                else:
                    if self.board[i - 1][j - 1] >= 6:
                        moves.append((i - 1, j - 1))

            if i - 1 >= 0 and j + 1 <= 7:
                if self.board[i - 1][j + 1] is None:
                    moves.append((i - 1, j + 1))
                else:
                    if self.board[i - 1][j + 1] >= 6:
                        moves.append((i - 1, j + 1))

        if self.board[i][j] == 10:
            # white king
            if not self.w_king_moved and not self.w_rook1_moved:
                if self.board[7][5] is None and self.board[7][6] is None:
                    moves.append((7, 7, "w0-0"))
            if not self.w_king_moved and not self.w_rook2_moved:
                if self.board[7][3] is None and self.board[7][2] is None and self.board[7][1] is None:
                    moves.append((7, 0, "w0-0-0"))

            if i + 1 <= 7:
                if self.board[i + 1][j] is None:
                    moves.append((i + 1, j))
                else:
                    if self.board[i + 1][j] < 6:
                        moves.append((i + 1, j))

            if i - 1 >= 0:
                if self.board[i - 1][j] is None:
                    moves.append((i - 1, j))
                else:
                    if self.board[i - 1][j] < 6:
                        moves.append((i - 1, j))

            if j + 1 <= 7:
                if self.board[i][j + 1] is None:
                    moves.append((i, j + 1))
                else:
                    if self.board[i][j + 1] < 6:
                        moves.append((i, j + 1))

            if j - 1 >= 0:
                if self.board[i][j - 1] is None:
                    moves.append((i, j - 1))
                else:
                    if self.board[i][j - 1] < 6:
                        moves.append((i, j - 1))

            if i + 1 <= 7 and j + 1 <= 7:
                if self.board[i + 1][j + 1] is None:
                    moves.append((i + 1, j + 1))
                else:
                    if self.board[i + 1][j + 1] < 6:
                        moves.append((i + 1, j + 1))

            if i + 1 <= 7 and j - 1 >= 0:
                if self.board[i + 1][j - 1] is None:
                    moves.append((i + 1, j - 1))
                else:
                    if self.board[i + 1][j - 1] < 6:
                        moves.append((i + 1, j - 1))

            if i - 1 >= 0 and j - 1 >= 0:
                if self.board[i - 1][j - 1] is None:
                    moves.append((i - 1, j - 1))
                else:
                    if self.board[i - 1][j - 1] < 6:
                        moves.append((i - 1, j - 1))

            if i - 1 >= 0 and j + 1 <= 7:
                if self.board[i - 1][j + 1] is None:
                    moves.append((i - 1, j + 1))
                else:
                    if self.board[i - 1][j + 1] < 6:
                        moves.append((i - 1, j + 1))

        if self.board[i][j] == 2:
            # black knight
            if i + 1 <= 7 and j + 2 <= 7:
                if self.board[i + 1][j + 2] is None:
                    moves.append((i + 1, j + 2))
                else:
                    if self.board[i + 1][j + 2] >= 6:
                        moves.append((i + 1, j + 2))

            if i - 1 >= 0 and j + 2 <= 7:
                if self.board[i - 1][j + 2] is None:
                    moves.append((i - 1, j + 2))
                else:
                    if self.board[i - 1][j + 2] >= 6:
                        moves.append((i - 1, j + 2))

            if i + 2 <= 7 and j + 1 <= 7:
                if self.board[i + 2][j + 1] is None:
                    moves.append((i + 2, j + 1))
                else:
                    if self.board[i + 2][j + 1] >= 6:
                        moves.append((i + 2, j + 1))

            if i + 2 <= 7 and j - 1 >= 0:
                if self.board[i + 2][j - 1] is None:
                    moves.append((i + 2, j - 1))
                else:
                    if self.board[i + 2][j - 1] >= 6:
                        moves.append((i + 2, j - 1))
            if i - 2 >= 0 and j + 1 <= 7:
                if self.board[i - 2][j + 1] is None:
                    moves.append((i - 2, j + 1))
                else:
                    if self.board[i - 2][j + 1] >= 6:
                        moves.append((i - 2, j + 1))

            if i + 1 <= 7 and j - 2 >= 0:
                if self.board[i + 1][j - 2] is None:
                    moves.append((i + 1, j - 2))
                else:
                    if self.board[i + 1][j - 2] >= 6:
                        moves.append((i + 1, j - 2))
            if i - 2 >= 0 and j - 1 >= 0:
                if self.board[i - 2][j - 1] is None:
                    moves.append((i - 2, j - 1))
                else:
                    if self.board[i - 2][j - 1] >= 6:
                        moves.append((i - 2, j - 1))

            if i - 1 >= 0 and j - 2 >= 0:
                if self.board[i - 1][j - 2] is None:
                    moves.append((i - 1, j - 2))
                else:
                    if self.board[i - 1][j - 2] >= 6:
                        moves.append((i - 1, j - 2))

        if self.board[i][j] == 8:
            # white knight
            if i + 1 <= 7 and j + 2 <= 7:
                if self.board[i + 1][j + 2] is None:
                    moves.append((i + 1, j + 2))
                else:
                    if self.board[i + 1][j + 2] < 6:
                        moves.append((i + 1, j + 2))

            if i - 1 >= 0 and j + 2 <= 7:
                if self.board[i - 1][j + 2] is None:
                    moves.append((i - 1, j + 2))
                else:
                    if self.board[i - 1][j + 2] < 6:
                        moves.append((i - 1, j + 2))

            if i + 2 <= 7 and j + 1 <= 7:
                if self.board[i + 2][j + 1] is None:
                    moves.append((i + 2, j + 1))
                else:
                    if self.board[i + 2][j + 1] < 6:
                        moves.append((i + 2, j + 1))

            if i + 2 <= 7 and j - 1 >= 0:
                if self.board[i + 2][j - 1] is None:
                    moves.append((i + 2, j - 1))
                else:
                    if self.board[i + 2][j - 1] < 6:
                        moves.append((i + 2, j - 1))
            if i - 2 >= 0 and j + 1 <= 7:
                if self.board[i - 2][j + 1] is None:
                    moves.append((i - 2, j + 1))
                else:
                    if self.board[i - 2][j + 1] < 6:
                        moves.append((i - 2, j + 1))

            if i + 1 <= 7 and j - 2 >= 0:
                if self.board[i + 1][j - 2] is None:
                    moves.append((i + 1, j - 2))
                else:
                    if self.board[i + 1][j - 2] < 6:
                        moves.append((i + 1, j - 2))
            if i - 2 >= 0 and j - 1 >= 0:
                if self.board[i - 2][j - 1] is None:
                    moves.append((i - 2, j - 1))
                else:
                    if self.board[i - 2][j - 1] < 6:
                        moves.append((i - 2, j - 1))

            if i - 1 >= 0 and j - 2 >= 0:
                if self.board[i - 1][j - 2] is None:
                    moves.append((i - 1, j - 2))
                else:
                    if self.board[i - 1][j - 2] < 6:
                        moves.append((i - 1, j - 2))

        return moves

    def move(self, i0, j0, i1, j1):
        legal_moves = self.legal_moves(i0, j0)
        if (i1, j1) in legal_moves:
            if self.board[i1][j1] == 1:
                if i1 == 0 and j1 == 0:
                    self.b_rook2_moved = True
                elif i1 == 0 and j1 == 7:
                    self.b_rook1_moved = True
            if self.board[i1][j1] == 7:
                if i1 == 7 and j1 == 0:
                    self.w_rook2_moved = True
                elif i1 == 7 and j1 == 7:
                    self.w_rook1_moved = True

            temp = self.board[i0][j0]
            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 5
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 11

            if self.board[i0][j0] == 1:
                if i0 == 0 and j0 == 0:
                    if not self.b_rook1_moved:
                        self.b_rook1_moved = True

                if i0 == 0 and j0 == 7:
                    if not self.b_rook2_moved:
                        self.b_rook2_moved = True

            if self.board[i0][j0] == 7:
                if i0 == 7 and j0 == 0:
                    if not self.w_rook1_moved:
                        self.w_rook1_moved = True

                if i0 == 7 and j0 == 7:
                    if not self.w_rook2_moved:
                        self.w_rook2_moved = True

            if self.board[i0][j0] == 4:
                if i0 == 0 and j0 == 4:
                    if not self.b_king_moved:
                        self.b_king_moved = True

            if self.board[i0][j0] == 10:
                if i0 == 7 and j0 == 4:
                    if not self.w_king_moved:
                        self.w_king_moved = True

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "w0-0") in legal_moves:
            self.board[7][4] = None
            self.board[7][5] = 7
            self.board[7][6] = 10
            self.board[7][7] = None

            self.w_rook2_moved = True
            self.w_king_moved = True

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "w0-0-0") in legal_moves:
            self.board[7][4] = None
            self.board[7][3] = 7
            self.board[7][2] = 10
            self.board[7][1] = None
            self.board[7][0] = None

            self.w_rook1_moved = True
            self.w_king_moved = True

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "b0-0") in legal_moves:
            self.board[0][4] = None
            self.board[0][5] = 1
            self.board[0][6] = 4
            self.board[0][7] = None

            self.b_rook2_moved = True
            self.b_king_moved = True

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "b0-0-0") in legal_moves:
            self.board[0][4] = None
            self.board[0][3] = 1
            self.board[0][2] = 4
            self.board[0][1] = None
            self.board[0][0] = None

            self.b_rook2_moved = True
            self.b_king_moved = True

            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "epr") in legal_moves:
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

        elif (i1, j1, "epl") in legal_moves:
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

        if self.move_made:
            if self.turn == "w":
                self.turn = "b"
            else:
                self.turn = "w"

        self.evaluate()

        return self.board
