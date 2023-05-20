from Analysis import Analysis
from Pieces import Pieces
from copy import deepcopy

engine = Analysis(Pieces.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))

actual_nodes = [1, 20, 400, 8902, 197281, 4865609, 119060324, 3195901860, 84998978956, 2439530234167, 69352859712417]
def depth_test(n, board, log=False):
    if n == 0:
        return 1

    if log:
        print(f"Depth {n=}, No of Nodes", end=" ")

    legal_moves = []
    for x in range(8):
        for y in range(8):
            if engine.board[x][y] is not None:
                moves = engine.legal_moves(x, y)
                if moves == []:
                    continue
                for i in moves:
                    legal_moves.append((x, y, i))

    nodes = 0
    for move in legal_moves:
        _board = deepcopy(board)
        board = engine.depth(*move, board=board)
        nodes += depth_test(n - 1, board)
        board = deepcopy(_board)

    if log:
        print(f"{nodes=}")

    return nodes


if __name__ == "__main__":
    print()
    depth_test(1, engine.board, log=True)
    depth_test(2, engine.board, log=True)
    depth_test(3, engine.board, log=True)
    depth_test(4, engine.board, log=True)
    depth_test(5, engine.board, log=True)
