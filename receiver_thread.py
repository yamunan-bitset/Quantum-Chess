import threading
import pickle
import socket


class Receiver(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)

        self.client_socket = client_socket

        self.quit = False

        self.move = None

    def kill(self):
        self.quit = True

    def run(self):
        while not self.quit:
            self.client_socket.settimeout(1)
            try:
                self.move = pickle.loads(self.client_socket.recv(1024))
                print(self.move)
            except:
                continue
