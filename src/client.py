import socket
import os, pickle

from ioutils import *


class Client:
    def __init__(self, host, ports, buffer_size = 1024):
        self.host = host
        self.ports = ports
        self.buffer_size = buffer_size

        self.iteration()

    def get_socket(self):
        sock = socket.socket()
        find = 0
        for port in self.ports:
            try:
                sock.connect((socket.gethostname(), port))
                print('Conected to port:', port)
                find = 1
                break
            except Exception as e:
                print(f'Could not connect to {self.host}:{port}')
                continue
        return sock if find else None
    
    def handle_callback(self, sock):
        msg_back = b''
        while True:
            aux = sock.recv(self.buffer_size)
            msg_back += aux
            if not aux or len(aux) < self.buffer_size:
                print(f'Received {len(msg_back)} bytes')
                break
        return msg_back

    def iteration(self):
        while True:
            print('\n\nWhat do you want to do? (type the option number)')
            print('1. Deposit \n2. Retrieve \n3. Edit  \n4. Delete \n5. Show all files \n6. Exit')
            op = input()
            if op == '1':
                print('Enter file name: (please type the full path if the file is not in the current directory)')
                file_path = input()
                file_path = os.path.abspath(file_path)

                file_name = os.path.basename(file_path)
                print(f'Enter tolerance (1 - {len(self.ports)}):')
                tolerance = int(input())
                bytes = get_bytes(file_path)

                data = {'op': 'deposit', 'file_name': file_name, 'tolerance': tolerance, 'data': bytes}
                data = pickle.dumps(data)

                sock = self.get_socket()

                if sock == None:
                    print('Could not connect to any port')
                    continue
                
                sock.send(data)
                msg_back = self.handle_callback(sock)
                try:
                    msg_back = pickle.loads(msg_back)
                    print(f'File {file_name} deposited successfully with tolerance {tolerance}')
                except Exception as e:
                    print(f'Could not decode data, error: {e}')
                    continue

                sock.close()
            
            elif op == '6':
                break

            elif op == '2':
                print('Enter the file name:')
                file_name = input()

                data = {'op': 'retrieve', 'file_name': file_name}
                data = pickle.dumps(data)

                sock = self.get_socket()
                
                if sock == None:
                    print('Could not connect to any port')
                    continue

                sock.send(data)
                msg_back = self.handle_callback(sock)
                try:
                    msg_back = pickle.loads(msg_back)
                    print(f'File {file_name} - {msg_back}')
                except Exception as e:
                    print(f'Could not decode data, error: {e}')
                    continue

                sock.close()

            elif op == '3':
                print('Enter the file name:')
                file_name = input()
                print(f'Enter the new level of tolerance. (1 - {len(self.ports)}):')
                tolerance = int(input())

                data = {'op': 'edit', 'file_name': file_name, 'tolerance': tolerance}
                data = pickle.dumps(data)

                sock = self.get_socket()

                if sock == None:
                    print('Could not connect to any port')
                    continue

                sock.send(data)
                msg_back = self.handle_callback(sock)       
                try:
                    msg_back = pickle.loads(msg_back)
                    print(f'File {file_name} - {msg_back}')
                except Exception as e:
                    print(f'Could not decode data, error: {e}')
                    continue
            
            elif op == '4':
                print('Enter the file name to exclude:')
                file_name = input()

                data = {'op': 'edit', 'file_name': file_name, 'tolerance': 0}
                data = pickle.dumps(data)

                sock = self.get_socket()

                if sock == None:
                    print('Could not connect to any port')
                    continue

                sock.send(data)
                msg_back = self.handle_callback(sock)
                try:
                    msg_back = pickle.loads(msg_back)
                    print(f'File {file_name} - {msg_back}')
                except Exception as e:
                    print(f'Could not decode data, error: {e}')
                    continue
            
            elif op == '5':
                show_indexes()
