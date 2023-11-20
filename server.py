import socket
import json
import threading
from settings import *

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)
server.listen(1) 


def client_listen(client_socket, client_address):
    global NUM_CLIENTS
    while True:
         # Get the file name and size first
        file_data = client_socket.recv(MAX_SIZE_BYTES).decode(ENCODING)
        
        try:
            # its a json file so load that
            data = json.loads(file_data)
            file_name = data['file_name']
            file_size = data['file_size']
            print(f"Receving file from {client_address[-1]}")
            print(f"Filename: {file_name}, Size: {file_size} bytes")
            
            with open(f'output/new_{file_name}', 'wb') as file:
                while file_size > 0:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    file_size -= len(data)
            print(f"\033[92mFile received successfully from {client_address[-1]}\033[0m")

        except:
            # If the client inputted exit
            if file_data.lower() in EXIT:
                print(f"\033[91m Client {client_address[-1]} has disconnected\033[0m")
                break

    client_socket.close()
    NUM_CLIENTS -= 1
    # close server when no clients are on.
    if NUM_CLIENTS == 0:
        print("No clients connected, therefore closing server...")
        server.close()
    # print(c)
    
    
def main():
    global NUM_CLIENTS
    server.listen() # start listening on that port
    print(f"Server is listening on {HOST}:{PORT}")
    try:
        while True:
            # Ensure only a certain number of threads can be created (number of clients)
            if threading.active_count() - 1 < MAX_CLIENTS:
                # Create a thread per new client so that multiple clients can send files at the same time
                client_socket, client_address = server.accept()
                thread = threading.Thread(target=client_listen, args=(client_socket, client_address))
                thread.start()
                NUM_CLIENTS += 1
                
                print(f"Number of Connections: {threading.active_count() - 1}")
            else:
                client_socket, client_address = server.reject()
                # print("Server cannot accept new clients client limit has been reached")
    except:
        pass

        
if __name__ == '__main__':
   
    main()
    
