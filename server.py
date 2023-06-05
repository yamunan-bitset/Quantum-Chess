import socket
import pickle

import threading

socket.getaddrinfo("", 1729)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1729))
s.listen(2)

clients = []
turn = "w"

def recv_send():
    while True:
        if len(clients) % 2 == 0:
            for i in range(0, len(clients), 2):
                try:
                    move = clients[i].recv(1024)
                    recv = pickle.loads(move)
                    print(f"Received {recv=}")
                    clients[i + 1].send(move)
                    print(f"Sent {recv=}")
                except:
                    continue
                try:
                    move = clients[i + 1].recv(1024)
                    recv = pickle.loads(move)
                    print(f"Received {recv=}")
                    clients[i].send(move)
                    print(f"Sent {recv=}")
                except:
                    continue

def connect():
    print("Server listening")
    client, addr = s.accept()
    print(f"{client.__str__()=} joined Server at {addr=}")
    clients.append(client)

    thread = threading.Thread(target=recv_send, args=())
    thread.start()


while True:
    try:
        connect()
    except KeyboardInterrupt:
        break
    except ConnectionRefusedError:
        break

for client in clients:
    client.close()

s.close()
