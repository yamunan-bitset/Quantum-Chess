import socket
socket.getaddrinfo("127.0.0.1", 1729)

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
s.bind(("127.0.0.1", 1729))
s.listen(1)
client_socket, addr = s.accept()
print(f"Connected with {addr=}")


def send(move):
    client_socket.send(pickle.dumps(move))


def recv():
    try:
        move = pickle.loads(client_socket.recv(1024))
    except:
        return None
    else:
        return move


ignore = False

while True:
    if pieces.analysis.turn == "w":
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
                    selected = pieces.selected
                    if not pieces.drop(*index, flag=flag):
                        board.unselect()
                    else:
                        board.render(pieces.analysis)
                        pieces.render()
                        send([*selected, *index, flag])
                else:
                    ignore = False

    else:
        s.settimeout(0.1)
        move = recv()
        if move is not None:
            print(f"Received {move=}")

            board.auto_select(move[0], move[1], pieces)
            pieces.select(move[0], move[1])
            board.auto_drop(move[2], move[3])
            pieces.drop(move[2], move[3], flag=move[4])

    screen.fill((36, 34, 30))
    board.render(pieces.analysis)
    pieces.mouse_pos = pygame.mouse.get_pos()
    board.mouse_pos = pygame.mouse.get_pos()
    pieces.render()
    pygame.display.update()

s.close()
