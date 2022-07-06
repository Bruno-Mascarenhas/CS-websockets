import sys
from client import Client
from server import Server

PORTS = [6661, 6662, 6663, 6664]
HOST = 'localhost'
BUFFER_SIZE = 1024

kind = sys.argv[1]
if kind == 'server':
    server = Server(HOST, PORTS, BUFFER_SIZE)
elif kind == 'client':
    client = Client(HOST, PORTS, BUFFER_SIZE)
else:
    print('Invalid argument, please run python3 src/main.py server or src/python3 main.py client')