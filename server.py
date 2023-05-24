import socket
import pickle
import os
import pygame
pygame.init()

from Chess import Pieces, Board


logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis Server")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

board = Board(screen)

startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pieces = Pieces(screen, startpos)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1729))
s.listen(1)
client_socket, addr = s.accept()
print(f"Connected with {addr=}")


def send(move):
    client_socket.send(pickle.dumps(move))


def recv():
    try:
        move = pickle.loads(s.recv(1024))
    except:
        move = None
    return move


ignore = False

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            pos = pygame.mouse.get_pos()
            button = pygame.mouse
            pieces.mouse_pos = pos
            index = board.select(pos, pieces)
            if not pieces.select(*index):
                board.unselect()
                ignore = True
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            if not ignore:
                pos = pygame.mouse.get_pos()
                button = pygame.mouse
                pieces.mouse_pos = pos
                index = board.drop(pos)
                flag = None
                if pieces.promotion:
                    flag = board.get_promotions(pieces.analysis.turn)
                #send([*pieces.selected, *index])
                if not pieces.drop(*index, flag=flag):
                    board.unselect()
                send(pieces.board)
            else:
                ignore = False

    if pieces.analysis.turn == "b":
        move = recv()
        if move is not None:
            print(f"Received {move=}")
            """
            index = board.auto_select(move[0], move[1], pieces)
            pieces.select(*index)
            index = board.auto_drop(move[0], move[1])
            # TODO: Promotion
            flag = None
            if pieces.promotion:
                flag = board.get_promotions(pieces.analysis.turn)
            if not pieces.drop(*index, flag=flag):
                board.unselect()
            """
            pieces.board = move
            pieces.analysis.board = move

    screen.fill((36, 34, 30))
    board.render(pieces.analysis)
    pieces.mouse_pos = pygame.mouse.get_pos()
    board.mouse_pos = pygame.mouse.get_pos()
    pieces.render()
    pygame.display.update()

s.close()
