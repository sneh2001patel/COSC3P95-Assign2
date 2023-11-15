import socket
import threading
from settings import *

# connect client with server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

def send_data(data):
    client_data = data.encode(ENCODING)
    client.send(client_data)

def messaging_client():
    while True:
        client_data = input()
        send_data(data=client_data)
        if client_data.lower() in EXIT:
            break
    client.close()
    quit()
messaging_client()        