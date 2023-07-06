from copy import deepcopy


def partition(array, array2, low, high):
    # choose the rightmost element as pivot
    pivot = array[high]
    i = low - 1

    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            (array[i], array[j]) = (array[j], array[i])
            (array2[i], array2[j]) = (array2[j], array2[i])

    (array[i + 1], array[high]) = (array[high], array[i + 1])
    (array2[i + 1], array2[high]) = (array2[high], array2[i + 1])
    return i + 1


def quick_sort(array, array2, low, high):
    if low < high:
        pi = partition(array, array2, low, high)
        quick_sort(array, array2, low, pi - 1)
        quick_sort(array, array2, pi + 1, high)
    array.reverse()
    array2.reverse()


class Analysis:
    def __init__(self, board):
        self.board = board

        self.turn = "w"
        self.flag = ""

        self.move_made = False
        self.prev_move = None

        self.b_rook1_moved = False
        self.w_rook1_moved = False
        self.b_rook2_moved = False
        self.w_rook2_moved = False
        self.b_king_moved = False
        self.w_king_moved = False

        self.w_king_in_check = False
        self.b_king_in_check = False

        self.check_mate = False
        self.stale_mate = False

        self.promotion = False
        self.captured = False
        self.castled = False

        self.evaluation = 0
        self.evaluate()

    def evaluate(self, turn=None, board=None):
        default = False
        if board is None:
            board = self.board
            default = True
        if turn is None:
            turn = self.turn
            default = True

        evaluation = 0
        for i in board:
            for j in i:
                if j is not None:
                    evaluation += Analysis.get_value(j, negative=True)

        evaluation += self.evaluate_endgame(evaluation, turn=turn, board=board)

        if default:
            self.evaluation = evaluation
        return evaluation

    def evaluate_endgame(self, piece_sum, turn=None, board=None):
        if board is None:
            board = self.board
        if turn is None:
            turn = self.turn

        evaluation = 0.0
        opp_king = 4 if turn == "w" else 10
        m_king = 4 if turn == "b" else 10
        opp_rank = 0
        opp_file = 0
        m_rank = 0
        m_file = 0
        weightage = 0
        for x, i in enumerate(board):
            for y, j in enumerate(i):
                if j is not None:
                    if j == opp_king:
                        opp_rank = x
                        opp_file = y
                    if j == m_king:
                        m_rank = x
                        m_file = y

                    if turn == "w" and j < 6:
                        weightage += j
                    elif turn == "b" and j >= 6:
                        weightage += j

        evaluation += (max(3 - opp_file, opp_file - 4) + max(3 - opp_rank, opp_rank - 4)) / 100
        evaluation += (14 - abs(m_file - opp_file) + abs(m_rank - opp_rank)) / 100

        weightage = 100 / weightage
        if piece_sum != 0:
            weightage *= piece_sum/abs(piece_sum)
        else:
            weightage = 0

        return evaluation * weightage

    @staticmethod
    def get_value(piece, negative=False):
        if piece == 0:
            if negative:
                return -1
            return 1
        elif piece == 1:
            if negative:
                return -5
            return 5
        elif piece == 2 or piece == 3:
            if negative:
                return -3
            return 3
        elif piece == 5:
            if negative:
                return -9
            return 9
        elif piece == 6:
            return 1
        elif piece == 7:
            return 5
        elif piece == 8 or piece == 9:
            return 3
        elif piece == 11:
            return 9
        else:
            # king
            return 0

    def order_best_moves(self, legal_moves, board=None):
        if board is None:
            board = self.board

        move_approx_ranks = [0] * len(legal_moves)
        for i, move in enumerate(legal_moves):
            _board = deepcopy(board)
            self.depth(*move, board=_board)
            move_approx_ranks[i] = self.evaluate(board=_board)
            moving_piece = board[move[0]][move[1]]
            capture_piece = board[move[2][0]][move[2][1]]

            if capture_piece is not None:
                move_approx_ranks[i] += Analysis.get_value(capture_piece) * 10 - Analysis.get_value(moving_piece)
            if len(move[2]) == 3:
                if move[2][2][1] == "q":
                    move_approx_ranks[i] += 9
                elif move[2][2][1] == "r":
                    move_approx_ranks[i] += 5
                else:
                    move_approx_ranks[i] += 3
            # TODO: Added more constrains, eg low rank piece (pawn) attack square, ...

        quick_sort(move_approx_ranks, legal_moves, 0, len(move_approx_ranks) - 1)

    def search_captures(self, depth, alpha, beta, board=None):
        if board is None:
            board = self.board
        _eval = self.evaluate(board=board)
        if _eval >= beta:
            return beta
        if _eval > alpha:
            alpha = _eval

        if depth == 0:
            return alpha

        capture_moves = []
        for x in range(8):
            for y in range(8):
                if board[x][y] is not None:
                    if (self.turn == "w" and board[x][y] >= 6) or (self.turn == "b" and board[x][y] < 6):
                        moves = self.legal_moves(x, y)
                        if moves == []:
                            continue
                        for i in moves:
                            _board = deepcopy(board)
                            sum0 = 0
                            for k in _board:
                                for j in k:
                                    if j is not None:
                                        sum0 += j + 1
                            self.depth(x, y, i, board=_board)
                            sum1 = 0
                            for k in _board:
                                for j in k:
                                    if j is not None:
                                        sum1 += j + 1

                            if sum1 != sum0:
                                capture_moves.append((x, y, i))

        self.order_best_moves(capture_moves, board=board)
        for move in capture_moves:
            _board = deepcopy(board)
            self.depth(*move, board=_board)
            _eval = -self.search_captures(depth - 1, -beta, -alpha)
            if _eval >= beta:
                return beta
            if _eval > alpha:
                alpha = _eval

        return alpha


    def find_best(self, depth, alpha, beta, board=None):
        if board is None:
            board = deepcopy(self.board)

        legal_moves = []
        for x in range(8):
            for y in range(8):
                if board[x][y] is not None:
                    if (self.turn == "w" and board[x][y] >= 6) or (self.turn == "b" and board[x][y] < 6):
                        moves = self.legal_moves(x, y)
                        if moves == []:
                            continue
                        for i in moves:
                            legal_moves.append((x, y, i))

        if len(legal_moves) == 0:
            return [None, None]
        self.order_best_moves(legal_moves, board=board)
        best_move = legal_moves[0]
        if depth == 0:
            return [self.search_captures(depth, alpha, beta, board=board), best_move]

        for move in legal_moves:
            _board = deepcopy(board)
            self.depth(*move, board=_board)
            _eval = -self.find_best(depth - 1, -beta, -alpha)[0]
            if _eval >= beta:
                return [beta, best_move]
            if _eval > alpha:
                alpha = _eval
                best_move = move

        return [alpha, best_move]

    def pseudo_legal_moves(self, i, j, board=None, ignore_turn=False):
        moves = []

        if board is None:
            board = self.board

        if board[i][j] is None:
            return moves

        if not ignore_turn:
            if board[i][j] < 6 and self.turn == "w":
                return moves
            if board[i][j] >= 6 and self.turn == "b":
                return moves

        if board[i][j] == 0:
            # black pawn

            if board[i + 1][j] is None:
                if i + 1 == 7:
                    moves.append((i + 1, j, "pq"))
                    moves.append((i + 1, j, "pr"))
                    moves.append((i + 1, j, "pk"))
                    moves.append((i + 1, j, "pb"))
                else:
                    moves.append((i + 1, j))
            if i == 1:
                if board[i + 1][j] is None and board[i + 2][j] is None:
                    moves.append((i + 2, j))
            if j != 7 and board[i + 1][j + 1] is not None and board[i + 1][j + 1] >= 6:
                if i + 1 == 7:
                    moves.append((i + 1, j + 1, "pq"))
                    moves.append((i + 1, j + 1, "pr"))
                    moves.append((i + 1, j + 1, "pk"))
                    moves.append((i + 1, j + 1, "pb"))
                else:
                    moves.append((i + 1, j + 1))
            if j != 0 and board[i + 1][j - 1] is not None and board[i + 1][j - 1] >= 6:
                if i + 1 == 7:
                    moves.append((i + 1, j - 1, "pq"))
                    moves.append((i + 1, j - 1, "pr"))
                    moves.append((i + 1, j - 1, "pk"))
                    moves.append((i + 1, j - 1, "pb"))
                else:
                    moves.append((i + 1, j - 1))
            if self.prev_move is not None:
                if board[self.prev_move[2]][self.prev_move[3]] == 6 and self.prev_move[0] == 6 and self.prev_move[
                    2] == 4 and i == 4:
                    if self.prev_move[3] == j + 1:
                        moves.append((i + 1, j + 1, "epr"))
                    elif self.prev_move[3] == j - 1:
                        moves.append((i + 1, j - 1, "epl"))

        if board[i][j] == 6:
            # white pawn
            if board[i - 1][j] is None:
                if i - 1 == 0:
                    moves.append((i - 1, j, "pq"))
                    moves.append((i - 1, j, "pr"))
                    moves.append((i - 1, j, "pk"))
                    moves.append((i - 1, j, "pb"))
                else:
                    moves.append((i - 1, j))
            if i == 6:
                if board[i - 1][j] is None and board[i - 2][j] is None:
                    moves.append((i - 2, j))
            if j != 0 and board[i - 1][j - 1] is not None and board[i - 1][j - 1] < 6:
                if i - 1 == 0:
                    moves.append((i - 1, j - 1, "pq"))
                    moves.append((i - 1, j - 1, "pr"))
                    moves.append((i - 1, j - 1, "pk"))
                    moves.append((i - 1, j - 1, "pb"))
                else:
                    moves.append((i - 1, j - 1))
            if j != 7 and board[i - 1][j + 1] is not None and board[i - 1][j + 1] < 6:
                if i - 1 == 0:
                    moves.append((i - 1, j + 1, "pq"))
                    moves.append((i - 1, j + 1, "pr"))
                    moves.append((i - 1, j + 1, "pk"))
                    moves.append((i - 1, j + 1, "pb"))
                else:
                    moves.append((i - 1, j + 1))
            if self.prev_move is not None:
                if board[self.prev_move[2]][self.prev_move[3]] == 0 and self.prev_move[0] == 1 and self.prev_move[
                    2] == 3 and i == 3:
                    if self.prev_move[3] == j + 1:
                        moves.append((i - 1, j + 1, "epr"))
                    elif self.prev_move[3] == j - 1:
                        moves.append((i - 1, j - 1, "epl"))

        if board[i][j] == 1:
            # black rook
            for _j in range(7 - j):
                if board[i][j + _j + 1] is not None:
                    if board[i][j + _j + 1] >= 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if board[i][j - _j - 1] is not None:
                    if board[i][j - _j - 1] >= 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if board[i + _i + 1][j] is not None:
                    if board[i + _i + 1][j] >= 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if board[i - _i - 1][j] is not None:
                    if board[i - _i - 1][j] >= 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

        if board[i][j] == 7:
            # white rook
            for _j in range(7 - j):
                if board[i][j + _j + 1] is not None:
                    if board[i][j + _j + 1] < 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if board[i][j - _j - 1] is not None:
                    if board[i][j - _j - 1] < 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if board[i + _i + 1][j] is not None:
                    if board[i + _i + 1][j] < 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if board[i - _i - 1][j] is not None:
                    if board[i - _i - 1][j] < 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

        if board[i][j] == 3:
            # black bishop
            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if board[i + k + 1][j + k + 1] is not None:
                    if board[i + k + 1][j + k + 1] >= 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if board[i - k - 1][j - k - 1] is not None:
                    if board[i - k - 1][j - k - 1] >= 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if board[i + k + 1][j - k - 1] is not None:
                    if board[i + k + 1][j - k - 1] >= 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if board[i - k - 1][j + k + 1] is not None:
                    if board[i - k - 1][j + k + 1] >= 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        if board[i][j] == 9:
            # white bishop
            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if board[i + k + 1][j + k + 1] is not None:
                    if board[i + k + 1][j + k + 1] < 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if board[i - k - 1][j - k - 1] is not None:
                    if board[i - k - 1][j - k - 1] < 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if board[i + k + 1][j - k - 1] is not None:
                    if board[i + k + 1][j - k - 1] < 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if board[i - k - 1][j + k + 1] is not None:
                    if board[i - k - 1][j + k + 1] < 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        if board[i][j] == 5:
            # black queen
            for _j in range(7 - j):
                if board[i][j + _j + 1] is not None:
                    if board[i][j + _j + 1] >= 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if board[i][j - _j - 1] is not None:
                    if board[i][j - _j - 1] >= 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if board[i + _i + 1][j] is not None:
                    if board[i + _i + 1][j] >= 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if board[i - _i - 1][j] is not None:
                    if board[i - _i - 1][j] >= 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if board[i + k + 1][j + k + 1] is not None:
                    if board[i + k + 1][j + k + 1] >= 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if board[i - k - 1][j - k - 1] is not None:
                    if board[i - k - 1][j - k - 1] >= 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if board[i + k + 1][j - k - 1] is not None:
                    if board[i + k + 1][j - k - 1] >= 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if board[i - k - 1][j + k + 1] is not None:
                    if board[i - k - 1][j + k + 1] >= 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        if board[i][j] == 11:
            # white queen
            for _j in range(7 - j):
                if board[i][j + _j + 1] is not None:
                    if board[i][j + _j + 1] < 6:
                        moves.append((i, j + _j + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j + _j + 1))

            for _j in range(j):
                if board[i][j - _j - 1] is not None:
                    if board[i][j - _j - 1] < 6:
                        moves.append((i, j - _j - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i, j - _j - 1))

            for _i in range(7 - i):
                if board[i + _i + 1][j] is not None:
                    if board[i + _i + 1][j] < 6:
                        moves.append((i + _i + 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i + _i + 1, j))

            for _i in range(i):
                if board[i - _i - 1][j] is not None:
                    if board[i - _i - 1][j] < 6:
                        moves.append((i - _i - 1, j))
                        break
                    else:
                        break
                else:
                    moves.append((i - _i - 1, j))

            for k in range(7):
                if i + k == 7 or j + k == 7:
                    break

                if board[i + k + 1][j + k + 1] is not None:
                    if board[i + k + 1][j + k + 1] < 6:
                        moves.append((i + k + 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j + k + 1))

            for k in range(7):
                if i - k == 0 or j - k == 0:
                    break

                if board[i - k - 1][j - k - 1] is not None:
                    if board[i - k - 1][j - k - 1] < 6:
                        moves.append((i - k - 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j - k - 1))

            for k in range(7):
                if i + k == 7 or j - k == 0:
                    break

                if board[i + k + 1][j - k - 1] is not None:
                    if board[i + k + 1][j - k - 1] < 6:
                        moves.append((i + k + 1, j - k - 1))
                        break
                    else:
                        break
                else:
                    moves.append((i + k + 1, j - k - 1))

            for k in range(7):
                if i - k == 0 or j + k == 7:
                    break

                if board[i - k - 1][j + k + 1] is not None:
                    if board[i - k - 1][j + k + 1] < 6:
                        moves.append((i - k - 1, j + k + 1))
                        break
                    else:
                        break
                else:
                    moves.append((i - k - 1, j + k + 1))

        if board[i][j] == 4:
            # black king
            if not self.b_king_moved and not self.b_rook1_moved:
                if board[0][5] is None and board[0][6] is None:
                    moves.append((0, 7, "b0-0"))
            if not self.b_king_moved and not self.b_rook2_moved:
                if board[0][3] is None and board[0][2] is None and board[0][1] is None:
                    moves.append((0, 0, "b0-0-0"))

            if i + 1 <= 7:
                if board[i + 1][j] is None:
                    moves.append((i + 1, j))
                else:
                    if board[i + 1][j] >= 6:
                        moves.append((i + 1, j))

            if i - 1 >= 0:
                if board[i - 1][j] is None:
                    moves.append((i - 1, j))
                else:
                    if board[i - 1][j] >= 6:
                        moves.append((i - 1, j))

            if j + 1 <= 7:
                if board[i][j + 1] is None:
                    moves.append((i, j + 1))
                else:
                    if board[i][j + 1] >= 6:
                        moves.append((i, j + 1))

            if j - 1 >= 0:
                if board[i][j - 1] is None:
                    moves.append((i, j - 1))
                else:
                    if board[i][j - 1] >= 6:
                        moves.append((i, j - 1))

            if i + 1 <= 7 and j + 1 <= 7:
                if board[i + 1][j + 1] is None:
                    moves.append((i + 1, j + 1))
                else:
                    if board[i + 1][j + 1] >= 6:
                        moves.append((i + 1, j + 1))

            if i + 1 <= 7 and j - 1 >= 0:
                if board[i + 1][j - 1] is None:
                    moves.append((i + 1, j - 1))
                else:
                    if board[i + 1][j - 1] >= 6:
                        moves.append((i + 1, j - 1))

            if i - 1 >= 0 and j - 1 >= 0:
                if board[i - 1][j - 1] is None:
                    moves.append((i - 1, j - 1))
                else:
                    if board[i - 1][j - 1] >= 6:
                        moves.append((i - 1, j - 1))

            if i - 1 >= 0 and j + 1 <= 7:
                if board[i - 1][j + 1] is None:
                    moves.append((i - 1, j + 1))
                else:
                    if board[i - 1][j + 1] >= 6:
                        moves.append((i - 1, j + 1))

        if board[i][j] == 10:
            # white king
            if not self.w_king_moved and not self.w_rook1_moved:
                if board[7][5] is None and board[7][6] is None:
                    moves.append((7, 7, "w0-0"))
            if not self.w_king_moved and not self.w_rook2_moved:
                if board[7][3] is None and board[7][2] is None and board[7][1] is None:
                    moves.append((7, 0, "w0-0-0"))

            if i + 1 <= 7:
                if board[i + 1][j] is None:
                    moves.append((i + 1, j))
                else:
                    if board[i + 1][j] < 6:
                        moves.append((i + 1, j))

            if i - 1 >= 0:
                if board[i - 1][j] is None:
                    moves.append((i - 1, j))
                else:
                    if board[i - 1][j] < 6:
                        moves.append((i - 1, j))

            if j + 1 <= 7:
                if board[i][j + 1] is None:
                    moves.append((i, j + 1))
                else:
                    if board[i][j + 1] < 6:
                        moves.append((i, j + 1))

            if j - 1 >= 0:
                if board[i][j - 1] is None:
                    moves.append((i, j - 1))
                else:
                    if board[i][j - 1] < 6:
                        moves.append((i, j - 1))

            if i + 1 <= 7 and j + 1 <= 7:
                if board[i + 1][j + 1] is None:
                    moves.append((i + 1, j + 1))
                else:
                    if board[i + 1][j + 1] < 6:
                        moves.append((i + 1, j + 1))

            if i + 1 <= 7 and j - 1 >= 0:
                if board[i + 1][j - 1] is None:
                    moves.append((i + 1, j - 1))
                else:
                    if board[i + 1][j - 1] < 6:
                        moves.append((i + 1, j - 1))

            if i - 1 >= 0 and j - 1 >= 0:
                if board[i - 1][j - 1] is None:
                    moves.append((i - 1, j - 1))
                else:
                    if board[i - 1][j - 1] < 6:
                        moves.append((i - 1, j - 1))

            if i - 1 >= 0 and j + 1 <= 7:
                if board[i - 1][j + 1] is None:
                    moves.append((i - 1, j + 1))
                else:
                    if board[i - 1][j + 1] < 6:
                        moves.append((i - 1, j + 1))

        if board[i][j] == 2:
            # black knight
            if i + 1 <= 7 and j + 2 <= 7:
                if board[i + 1][j + 2] is None:
                    moves.append((i + 1, j + 2))
                else:
                    if board[i + 1][j + 2] >= 6:
                        moves.append((i + 1, j + 2))

            if i - 1 >= 0 and j + 2 <= 7:
                if board[i - 1][j + 2] is None:
                    moves.append((i - 1, j + 2))
                else:
                    if board[i - 1][j + 2] >= 6:
                        moves.append((i - 1, j + 2))

            if i + 2 <= 7 and j + 1 <= 7:
                if board[i + 2][j + 1] is None:
                    moves.append((i + 2, j + 1))
                else:
                    if board[i + 2][j + 1] >= 6:
                        moves.append((i + 2, j + 1))

            if i + 2 <= 7 and j - 1 >= 0:
                if board[i + 2][j - 1] is None:
                    moves.append((i + 2, j - 1))
                else:
                    if board[i + 2][j - 1] >= 6:
                        moves.append((i + 2, j - 1))
            if i - 2 >= 0 and j + 1 <= 7:
                if board[i - 2][j + 1] is None:
                    moves.append((i - 2, j + 1))
                else:
                    if board[i - 2][j + 1] >= 6:
                        moves.append((i - 2, j + 1))

            if i + 1 <= 7 and j - 2 >= 0:
                if board[i + 1][j - 2] is None:
                    moves.append((i + 1, j - 2))
                else:
                    if board[i + 1][j - 2] >= 6:
                        moves.append((i + 1, j - 2))
            if i - 2 >= 0 and j - 1 >= 0:
                if board[i - 2][j - 1] is None:
                    moves.append((i - 2, j - 1))
                else:
                    if board[i - 2][j - 1] >= 6:
                        moves.append((i - 2, j - 1))

            if i - 1 >= 0 and j - 2 >= 0:
                if board[i - 1][j - 2] is None:
                    moves.append((i - 1, j - 2))
                else:
                    if board[i - 1][j - 2] >= 6:
                        moves.append((i - 1, j - 2))

        if board[i][j] == 8:
            # white knight
            if i + 1 <= 7 and j + 2 <= 7:
                if board[i + 1][j + 2] is None:
                    moves.append((i + 1, j + 2))
                else:
                    if board[i + 1][j + 2] < 6:
                        moves.append((i + 1, j + 2))

            if i - 1 >= 0 and j + 2 <= 7:
                if board[i - 1][j + 2] is None:
                    moves.append((i - 1, j + 2))
                else:
                    if board[i - 1][j + 2] < 6:
                        moves.append((i - 1, j + 2))

            if i + 2 <= 7 and j + 1 <= 7:
                if board[i + 2][j + 1] is None:
                    moves.append((i + 2, j + 1))
                else:
                    if board[i + 2][j + 1] < 6:
                        moves.append((i + 2, j + 1))

            if i + 2 <= 7 and j - 1 >= 0:
                if board[i + 2][j - 1] is None:
                    moves.append((i + 2, j - 1))
                else:
                    if board[i + 2][j - 1] < 6:
                        moves.append((i + 2, j - 1))
            if i - 2 >= 0 and j + 1 <= 7:
                if board[i - 2][j + 1] is None:
                    moves.append((i - 2, j + 1))
                else:
                    if board[i - 2][j + 1] < 6:
                        moves.append((i - 2, j + 1))

            if i + 1 <= 7 and j - 2 >= 0:
                if board[i + 1][j - 2] is None:
                    moves.append((i + 1, j - 2))
                else:
                    if board[i + 1][j - 2] < 6:
                        moves.append((i + 1, j - 2))
            if i - 2 >= 0 and j - 1 >= 0:
                if board[i - 2][j - 1] is None:
                    moves.append((i - 2, j - 1))
                else:
                    if board[i - 2][j - 1] < 6:
                        moves.append((i - 2, j - 1))

            if i - 1 >= 0 and j - 2 >= 0:
                if board[i - 1][j - 2] is None:
                    moves.append((i - 1, j - 2))
                else:
                    if board[i - 1][j - 2] < 6:
                        moves.append((i - 1, j - 2))

        return moves

    def depth(self, i, j, move, board=None):
        if board is None:
            board = deepcopy(self.board)

        if None in move:
            return board

        if "w0-0" in move:
            board[7][4] = None
            board[7][5] = 7
            board[7][6] = 10
            board[7][7] = None

        elif "w0-0-0" in move:
            board[7][4] = None
            board[7][3] = 7
            board[7][2] = 10
            board[7][1] = None
            board[7][0] = None

        elif "b0-0" in move:
            board[0][4] = None
            board[0][5] = 1
            board[0][6] = 4
            board[0][7] = None

        elif "b0-0-0" in move:
            board[0][4] = None
            board[0][3] = 1
            board[0][2] = 4
            board[0][1] = None
            board[0][0] = None

        elif "epr" in move:
            temp = board[i][j]
            board[i][j + 1] = None
            board[move[0]][move[1]] = temp
            board[i][j] = None

        elif "epl" in move:
            temp = board[i][j]
            board[i][j - 1] = None
            board[move[0]][move[1]] = temp
            board[i][j] = None

        elif "pq" in move:
            temp = board[i][j]
            board[move[0]][move[1]] = temp
            board[i][j] = None
            if board[move[0]][move[1]] == 0 and move[0] == 7:
                board[move[0]][move[1]] = 5
            if board[move[0]][move[1]] == 6 and move[0] == 0:
                board[move[0]][move[1]] = 11

        elif "pr" in move:
            temp = board[i][j]
            board[move[0]][move[1]] = temp
            board[i][j] = None
            if board[move[0]][move[1]] == 0 and move[0] == 7:
                board[move[0]][move[1]] = 1
            if board[move[0]][move[1]] == 6 and move[0] == 0:
                board[move[0]][move[1]] = 7

        elif "pk" in move:
            temp = board[i][j]
            board[move[0]][move[1]] = temp
            board[i][j] = None
            if board[move[0]][move[1]] == 0 and move[0] == 7:
                board[move[0]][move[1]] = 2
            if board[move[0]][move[1]] == 6 and move[0] == 0:
                board[move[0]][move[1]] = 8

        elif "pb" in move:
            temp = board[i][j]
            board[move[0]][move[1]] = temp
            board[i][j] = None
            if board[move[0]][move[1]] == 0 and move[0] == 7:
                board[move[0]][move[1]] = 3
            if board[move[0]][move[1]] == 6 and move[0] == 0:
                board[move[0]][move[1]] = 9

        else:
            temp = board[i][j]
            board[move[0]][move[1]] = temp
            board[i][j] = None

        return board

    def check_for_king_in_check(self, i, j, board=None):
        if board is None:
            board = self.board

        opp_moves = []
        if board[i][j] is not None and (board[i][j] == 10 or board[i][j] == 4):
            for x in range(8):
                for y in range(8):
                    if board[x][y] is not None:
                        if board[i][j] == 10:
                            if board[x][y] < 6:
                                opp_moves.append(self.pseudo_legal_moves(x, y, board=board, ignore_turn=True))
                        else:
                            if board[x][y] >= 6:
                                opp_moves.append(self.pseudo_legal_moves(x, y, board=board, ignore_turn=True))

            for m in opp_moves:
                if (i, j) in m or (i, j, "w0-0") in m or (i, j, "b0-0") in m or (i, j, "w0-0-0") in m or (
                        i, j, "b0-0-0") in m or (i, j, "epr") in m or (i, j, "epl") in m or (i, j, "pq") in m or (
                        i, j, "pr") in m or (i, j, "pb") in m or (i, j, "pk") in m:
                    return True

        return False

    def check_for_castle(self, moves, board=None):
        if board is None:
            board = self.board

        illegal = []
        for move in moves:
            opp_moves = []
            for x in range(8):
                for y in range(8):
                    if board[x][y] is not None:
                        if board[move[0]][move[1]] == 10:
                            if board[x][y] < 6:
                                opp_moves.append(self.pseudo_legal_moves(x, y, board=board, ignore_turn=True))
                        elif board[move[0]][move[1]] == 4:
                            if board[x][y] >= 6:
                                opp_moves.append(self.pseudo_legal_moves(x, y, board=board, ignore_turn=True))

            if board[move[0]][move[1]] == 10:
                if "w0-0" in move:
                    for m in opp_moves:
                        if (7, 4) in m or (7, 5) in m or (7, 6) in m:
                            if move in moves:
                                illegal.append(move)

                elif "w0-0-0" in move:
                    for m in opp_moves:
                        if (7, 4) in m or (7, 3) in m or (7, 2) in m or (7, 1) in m:
                            if move in moves:
                                illegal.append(move)
            else:
                if "b0-0" in move:
                    for m in opp_moves:
                        if (0, 4) in m or (0, 5) in m or (0, 6) in m:
                            if move in moves:
                                illegal.append(move)

                elif "b0-0-0" in move:
                    for m in opp_moves:
                        if (0, 4) in m or (0, 3) in m or (0, 2) in m or (0, 1) in m:
                            if move in moves:
                                illegal.append(move)

        for move in illegal:
            if move in moves:
                moves.remove(move)

        return moves

    def check_for_resolve_check(self, i, j, moves):
        illegal = []
        for move in moves:
            board = self.depth(i, j, move)

            for x in range(8):
                for y in range(8):
                    if board[x][y] is not None:
                        if (self.turn == "w" and board[x][y] == 10) or (self.turn == "b" and board[x][y] == 4):
                            if self.check_for_king_in_check(x, y, board=board):
                                illegal.append(move)

        for move in illegal:
            if move in moves:
                moves.remove(move)

        return moves

    def legal_moves(self, i, j, ignore_turn=False):
        legal_moves = self.pseudo_legal_moves(i, j, ignore_turn=ignore_turn)
        legal_moves = self.check_for_castle(legal_moves)
        legal_moves = self.check_for_resolve_check(i, j, legal_moves)

        return legal_moves

    def move(self, i0, j0, i1, j1, legal_moves=None, promotion_f=None):
        if legal_moves is None:
            legal_moves = self.legal_moves(i0, j0)

        self.promotion = False
        self.captured = False
        self.castled = False
        sum0 = 0
        for i in self.board:
            for j in i:
                if j is not None:
                    sum0 += j + 1

        for moves in legal_moves:
            if moves[0] == i1 and moves[1] == j1:
                if len(moves) == 3:
                    if "p" in moves[2] and "e" not in moves[2]:
                        if promotion_f is not None:
                            self.flag = promotion_f(self.turn)
                    else:
                        self.flag = ""
                else:
                    self.flag = ""
                break

        if (i1, j1) in legal_moves:
            temp = self.board[i0][j0]
            self.board[i1][j1] = temp
            self.board[i0][j0] = None

            if self.board[i1][j1] == 1:
                if i0 == 0 and j0 == 0:
                    if not self.b_rook1_moved:
                        self.b_rook1_moved = True

                if i0 == 0 and j0 == 7:
                    if not self.b_rook2_moved:
                        self.b_rook2_moved = True

            if self.board[i1][j1] == 7:
                if i0 == 7 and j0 == 0:
                    if not self.w_rook1_moved:
                        self.w_rook1_moved = True

                if i0 == 7 and j0 == 7:
                    if not self.w_rook2_moved:
                        self.w_rook2_moved = True

            if self.board[i1][j1] == 4:
                if not self.b_king_moved:
                    self.b_king_moved = True

            if self.board[i1][j1] == 10:
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

            self.castled = True
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

            self.castled = True
            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "b0-0") in legal_moves:
            self.board[0][4] = None
            self.board[0][5] = 1
            self.board[0][6] = 4
            self.board[0][7] = None

            self.b_rook1_moved = True
            self.b_king_moved = True

            self.castled = True
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

            self.castled = True
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

        elif (i1, j1, "pq") in legal_moves and self.flag == "q":
            temp = self.board[i0][j0]
            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 5
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 11

            self.promotion = True
            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "pr") in legal_moves and self.flag == "r":
            temp = self.board[i0][j0]
            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 1
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 7

            self.promotion = True
            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "pk") in legal_moves and self.flag == "k":
            temp = self.board[i0][j0]
            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 2
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 8

            self.promotion = True
            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        elif (i1, j1, "pb") in legal_moves and self.flag == "b":
            temp = self.board[i0][j0]
            self.board[i1][j1] = temp
            self.board[i0][j0] = None
            if self.board[i1][j1] == 0 and i1 == 7:
                self.board[i1][j1] = 3
            if self.board[i1][j1] == 6 and i1 == 0:
                self.board[i1][j1] = 9

            self.promotion = True
            self.prev_move = (i0, j0, i1, j1)
            self.move_made = True

        else:
            self.move_made = False

        if self.move_made:
            if self.turn == "w":
                self.turn = "b"
            else:
                self.turn = "w"

        total_legal_white_moves = []
        total_legal_black_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    if self.board[i][j] >= 6:
                        total_legal_white_moves.append(self.legal_moves(i, j, ignore_turn=True))
                        if self.board[i][j] == 10:
                            if self.check_for_king_in_check(i, j):
                                self.w_king_in_check = True
                            else:
                                self.w_king_in_check = False
                    else:
                        total_legal_black_moves.append(self.legal_moves(i, j, ignore_turn=True))
                        if self.board[i][j] == 4:
                            if self.check_for_king_in_check(i, j):
                                self.b_king_in_check = True
                            else:
                                self.b_king_in_check = False

        black_list = []
        for i in total_legal_black_moves:
            for j in i:
                black_list.append(j)
        white_list = []
        for i in total_legal_white_moves:
            for j in i:
                white_list.append(j)

        sum1 = 0
        for i in self.board:
            for j in i:
                if j is not None:
                    sum1 += j + 1
        if sum0 != sum1:
            if not self.promotion:
                self.captured = True

        if self.turn == "w":
            if len(white_list) == 0:
                if self.w_king_in_check:
                    self.check_mate = True
                else:
                    self.stale_mate = True
        else:
            if len(black_list) == 0:
                if self.b_king_in_check:
                    self.check_mate = True
                else:
                    self.stale_mate = True

        if sum1 == 16:
            self.stale_mate = True

        return self.board
