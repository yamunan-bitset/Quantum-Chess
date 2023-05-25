import socket
import pickle
import os
import pygame

from Chess import Pieces, Board
from receiver_thread import Receiver

socket.getaddrinfo("127.0.0.1", 1729)
pygame.init()

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis Client")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

board = Board(screen)

startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pieces = Pieces(screen, startpos)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
s.connect(("127.0.0.1", 1729))


def recv():
    try:
        move = pickle.loads(s.recv(1024))
    except:
        move = None
    return move


def send(move):
    s.send(pickle.dumps(move))


recv_thread = Receiver(s)
recv_thread.start()

ignore = False
prev_recv_move = None

while True:
    if pieces.analysis.turn == "b":
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
                else:
                    ignore = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if not ignore:
                    pos = pygame.mouse.get_pos()
                    button = pygame.mouse
                    pieces.mouse_pos = pos
                    index = board.drop(pos)
                    selected = pieces.selected
                    if not pieces.drop(*index, board.get_promotions):
                        board.unselect()
                    else:
                        board.render(pieces.analysis)
                        pieces.render()
                        send([*selected, *index, pieces.analysis.flag])

                else:
                    ignore = False

    else:
        move = recv_thread.move
        if move != prev_recv_move:
            if move is not None:
                print(f"Received {move=}")

                board.auto_select(move[0], move[1], pieces)
                pieces.select(move[0], move[1])
                board.auto_drop(move[2], move[3])
                pieces.drop(move[2], move[3], lambda colour: move[4])

                prev_recv_move = move
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

    screen.fill((36, 34, 30))
    board.render(pieces.analysis)
    pieces.mouse_pos = pygame.mouse.get_pos()
    board.mouse_pos = pygame.mouse.get_pos()
    pieces.render()
    pygame.display.update()
