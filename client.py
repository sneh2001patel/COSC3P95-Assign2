import os
import json
import socket
import threading
from settings import *

from opentelemetry import trace
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer_provider().get_tracer(__name__)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(SERVER_ADDR)
except:
    print("ERROR")
client_accept = True


def send_file(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    if 5120 <= file_size <= 104857600:
        file_data = {
            "file_name": file_name,
            "file_size": file_size
        }
        
        data = json.dumps(file_data).encode(ENCODING)
        client.send(data)

        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client.send(data)
                
        print("\033[92mFile sent successfully\033[0m")
    else:
        if file_size > 104857600:
            print(f"\033[91mFile exceeds more than 100MB\033[0m")
        else:
            print(f"\033[91mFile is too small (less than than 5Kb) \033[0m")
            

def messaging_client():
    if client:
        while client_accept:
            client_data = input("Enter the path of the file to upload or enter 'exit' to quit: ")
            if client_data == "":
                # print("\033[91mThis text will be printed in red.\033[0m")

                print("\033[91mInvalid Input try again\033[0m")
            elif client_data.lower() in EXIT:
                break
            else:
                try:
                    with tracer.start_as_current_span("client"):
                        with tracer.start_as_current_span("client-server"):
                            send_file(client_data)
                except:
                    print("\033[91mFile does not exist try again.\033[0m")
        client.close()
        quit()
messaging_client()        