import socket
import threading
from settings import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

def client_listen(client_socket, client_address):
    while True:
        data = client_socket.recv(MAX_SIZE_BYTES).decode(ENCODING)
        print(f'{client_address}:{data}')
        if data.lower() in EXIT:
            break
    
    client_socket.close()
    

def main():
    server.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=client_listen, args=(client_socket, client_address))
        thread.start()
        print(f"Number of Connections: {threading.active_count() - 1}")
    server.close()
        
if __name__ == '__main__':
    main()
    
