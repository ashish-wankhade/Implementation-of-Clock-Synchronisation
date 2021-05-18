import socket
from datetime import *
from dateutil import parser
from timeit import *
import time

PORT = 8010
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
ADDRESS = client.getsockname()[1]

while True:
    message = input("\nTO ASK TIME PRESS '1' OR WRITE --->>> WHAT IS THE TIME?\n"
                    "FOR DISCONNECTING WRITE MESSAGE AS --->>> disconnect me\n"
                    "WRITE YOUR MESSAGE HERE - ")
    message = message.lower()
    time_at_msg_sent = default_timer()
    message_sent_at = datetime.now()

    client.send(str(message).encode(FORMAT))
    #sleep(2)
    print(f"MESSAGE SENT BY ME - {message} at {message_sent_at}")
    if message == "what is the time?" or message == "1":
        requested_time = parser.parse(client.recv(HEADER).decode())
        time_recieved = default_timer()
        #time_recieved_at = datetime.now()

        print(f'REQUESTED  TIME  = {requested_time}')
        #print(f'TIME RECIEVED AT = {time_recieved}')
        delay = time_recieved - time_at_msg_sent

        if delay:
            print(f'DELAY IN TIME IDENTIFIED WHICH IS = {delay}')
            client_coreected_time = requested_time + timedelta(seconds=delay / 2)
            print(f'SYNCHRONIZED CLIENT CLOCK TIME = {client_coreected_time}')
        else:
            print(f'NO NEED OF CLOCK SYNCHRONIZATION TO THIS CLIENTS TIME')

    if message == "disconnect me":
        print("DISCONNECTING...")
        break
