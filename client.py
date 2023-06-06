import socket
import pickle
import os
import sys
import pygame

from Chess import Pieces, Board
from receiver_thread import Receiver
from Widgets import Button

SERVER_IP = "127.0.0.1"

socket.getaddrinfo(SERVER_IP, 1729)
pygame.init()

logo = pygame.image.load(os.path.join("texture", "black", "knight.png"))
pygame.display.set_icon(logo)
pygame.display.set_caption("Chess Analysis Client")
screen = pygame.display.set_mode((1000, 800))
screen.fill((36, 34, 30))

board = Board(screen)

draw = Button(screen, (50, 200, 100), (100, 200, 100), (50, 50, 100), board.font, "Draw", (183, 183, 183), 15, 530, 75, 30)
resign = Button(screen, (50, 200, 100), (100, 200, 100), (50, 50, 100), board.font, "Resign", (183, 183, 183), 130, 530, 75, 30)

startpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
pieces = Pieces(screen, startpos)

#m_colour = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((SERVER_IP, 1729))

m_colour = pickle.loads(s.recv(1024))

recv_thread = Receiver(s)
recv_thread.start()

ignore = False
prev_recv_move = None
playing = True

while True:
    move = recv_thread.move
    if move != prev_recv_move:
        if isinstance(move, str):
            if recv_thread.draw:
                board.white_offers_draw = False
                board.black_offers_draw = False
                board.draw = True
                playing = False
            elif recv_thread.offer_draw_white:
                board.white_offers_draw = True
            elif recv_thread.offer_draw_white:
                board.black_offers_draw = True

            if recv_thread.resign_black:
                board.black_resign = True
                playing = False

            if recv_thread.resign_white:
                board.white_resign = True
                playing = False

    if playing:
        if pieces.analysis.turn == m_colour:
            event = pygame.event.wait()
            pos = pygame.mouse.get_pos()
            button = pygame.mouse

            if draw.handle_event(event, pos):
                s.send(pickle.dumps("draw_offer_" + m_colour))
                if m_colour == "b":
                    board.black_offers_draw = True
                else:
                    board.white_offers_draw = True
            if resign.handle_event(event, pos):
                s.send(pickle.dumps("resign_" + m_colour))
                if m_colour == "b":
                    board.black_resign = True
                else:
                    board.white_resign = True
                playing = False

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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
                            s.send(pickle.dumps([*selected, *index, pieces.analysis.flag]))

                    else:
                        ignore = False

        else:
            move = recv_thread.move
            if move != prev_recv_move:
                if isinstance(move, str):
                    if recv_thread.draw:
                        board.white_offers_draw = False
                        board.black_offers_draw = False
                        board.draw = True
                        playing = False
                    elif recv_thread.offer_draw_white:
                        board.white_offers_draw = True
                    elif recv_thread.offer_draw_white:
                        board.black_offers_draw = True

                    if recv_thread.resign_black:
                        board.black_resign = True
                        playing = False

                    if recv_thread.resign_white:
                        board.white_resign = True
                        playing = False
                else:
                    if move is not None:
                        print(f"Received {move=}")

                        board.auto_select(move[0], move[1], pieces)
                        pieces.select(move[0], move[1])
                        board.auto_drop(move[2], move[3])
                        pieces.drop(move[2], move[3], lambda colour: move[4])

                        prev_recv_move = move

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                button = pygame.mouse

                if draw.handle_event(event, pos):
                    s.send(pickle.dumps("draw_offer_" + m_colour))
                    if m_colour == "b":
                        board.black_offers_draw = True
                    else:
                        board.white_offers_draw = True
                if resign.handle_event(event, pos):
                    s.send(pickle.dumps("resign_" + m_colour))
                    if m_colour == "b":
                        board.black_resign = True
                    else:
                        board.white_resign = True
                    playing = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    screen.fill((36, 34, 30))
    board.render(pieces.analysis)
    pieces.mouse_pos = pygame.mouse.get_pos()
    board.mouse_pos = pygame.mouse.get_pos()
    pieces.render()
    draw.render()
    resign.render()
    pygame.display.update()
