import threading
import pickle
import socket


class Receiver(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)

        self.client_socket = client_socket

        self.quit = False

        self.resign_white = False
        self.resign_black = False
        self.offer_draw_white = False
        self.offer_draw_black = False
        self.draw = False

        self.move = None
        self.time = None

    def kill(self):
        self.quit = True

    def run(self):
        while not self.quit:
            self.client_socket.settimeout(1)
            try:
                self.move = pickle.loads(self.client_socket.recv(1024))

                if self.move == "resign_b":
                    self.resign_black = True
                elif self.move == "resign_w":
                    self.resign_white = True
                elif self.move == "draw_offer_b":
                    self.offer_draw_black = True
                    if self.offer_draw_white:
                        self.draw = True
                        self.quit = True
                elif self.move == "draw_offer_w":
                    self.offer_draw_white = True
                    if self.offer_draw_black:
                        self.draw = True
                        self.quit = True

                print(self.move)
            except:
                continue
