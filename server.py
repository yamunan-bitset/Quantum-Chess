import socket
import pickle


import threading

socket.getaddrinfo("", 1729)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1729))
s.listen(2)

clients = []
turn = "w"

def recv_send(turn):
    while True:
        if turn == "w":
            try:
                move = clients[0].recv(1024)
                recv = pickle.loads(move)
                print(f"Received {recv=}")
                clients[1].send(move)
                print(f"Sent {recv=}")
                turn = "b"
            except:
                continue
        else:
            try:
                move = clients[1].recv(1024)
                recv = pickle.loads(move)
                print(f"Received {recv=}")
                clients[0].send(move)
                print(f"Sent {recv=}")
                turn = "w"
            except:
                continue


def connect():
    print("Server listening")
    client, addr = s.accept()
    print(f"{client.__str__()=} joined Server at {addr=}")
    clients.append(client)

    thread = threading.Thread(target=recv_send, args=(turn,))
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
