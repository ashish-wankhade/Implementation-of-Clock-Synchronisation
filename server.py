import socket
import threading
import csv
from datetime import *
from time import *

PORT = 8010
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def clients(conn, addr, clients_conn):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        msg = conn.recv(HEADER).decode(FORMAT)
        time_at_msg_recv = datetime.now()
        print(f"[{addr}] just send {msg} at {time_at_msg_recv}")
        # time_at_msg_sent = conn.recv(HEADER).decode(FORMAT)

        if msg == "disconnect me":
            connected = False

        if msg == "what is the time?" or msg == "1":
            # requested_time = datetime.now()
            sleep(2)
            conn.send(str(datetime.now()).encode())
            print("REQUESTED TIME SENT TO CLIENT")

        # maintaining log file
        with open('log.csv', mode='a') as log:
            fieldnames = ['address', 'date', 'time', 'message']
            write = csv.DictWriter(log, fieldnames=fieldnames)
            address = str(addr[0]), str(addr[1])
            time_at_msg_recv = datetime.now()
            date = time_at_msg_recv.date()
            time = time_at_msg_recv.time()
            message = msg

            fill = {
                'address': address,
                'date': date,
                'time': time,
                'message': message
            }
            write.writerow(fill)

    print(f'Disconnected {addr}')
    clients_conn.remove(str(addr))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    clients_conn = []
    while True:
        conn, addr = server.accept()
        clients_conn.append(str(addr))
        thread = threading.Thread(target=clients, args=(conn, addr, clients_conn))
        thread.start()

        print(
            f"[ACTIVE CONNECTIONS] = {threading.activeCount() - 1}")  # -1 because one active thread is already running ie. start()


print("[STARTING] server is starting...")
start()
