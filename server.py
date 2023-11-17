import socket
import json
import threading
from settings import *

from opentelemetry.instrumentation.wsgi import collect_request_attributes
from opentelemetry.propagate import extract
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace import (
    SpanKind,
    get_tracer_provider,
    set_tracer_provider,
)

# Opentelementry and Jaeger

set_tracer_provider(TracerProvider())
tracer = get_tracer_provider().get_tracer(__name__)

get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)
server.listen(1) 


def client_listen(client_socket, client_address):
    global NUM_CLIENTS
    while True:
        file_data = client_socket.recv(MAX_SIZE_BYTES).decode(ENCODING)
        
        try:
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
            print(f"\033[91m Client {client_address[-1]} has disconnected\033[0m")
            # print(file_data)
            if file_data.lower() in EXIT:
                break

    client_socket.close()
    NUM_CLIENTS -= 1
    if NUM_CLIENTS == 0:
        print("No clients connected, therefore closing server...")
        server.close()
    # print(c)
    
    
def main():
    global NUM_CLIENTS
    server.listen()
    with tracer.start_as_current_span(
        "server_request",
        kind=SpanKind.SERVER,
    ):
        print(f"Server is listening on {HOST}:{PORT}")
        try:
            while True:
                if threading.active_count() - 1 < MAX_CLIENTS:
                    
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
    
