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
            to_remove = []
            for i in range(0, len(clients), 2):
                try:
                    move = clients[i].recv(1024)
                except:
                    to_remove.append(clients[i])
                else:
                    recv = pickle.loads(move)
                    print(f"Received {recv=}")
                try:
                    clients[i + 1].send(move)
                except:
                    to_remove.append(clients[i + 1])
                else:
                    print(f"Sent {recv=}")

                try:
                    move = clients[i + 1].recv(1024)
                except:
                    to_remove.append(clients[i + 1])
                else:
                    recv = pickle.loads(move)
                    print(f"Received {recv=}")
                try:
                    clients[i].send(move)
                except:
                    to_remove.append(clients[i])
                else:
                    print(f"Sent {recv=}")


def connect():
    print("Server listening")
    client, addr = s.accept()
    print(f"{client.__str__()=} joined Server at {addr=}")
    client.send(pickle.dumps("b" if len(clients) % 2 == 1 else "w"))
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
