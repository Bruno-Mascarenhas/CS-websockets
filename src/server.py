from operator import index
import socket
import pickle
import sys
from tabnanny import check

from ioutils import *

class Server:
    def __init__(self, host, ports, role = 'support', buffer_size = 1024):
        self.host = host
        self.ports = ports
        for port in ports:
            try:
                self.port = port
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((socket.gethostname(), self.port))
                self.sock.listen(6)
                break
            except:
                self.sock = None
                print(f'Could not bind to {self.host}:{self.port}')
                continue
                
        if self.sock == None:
            print("Could not connect to any port")
            sys.exit()

        print(f"Connected to {socket.gethostname()[1]}:{self.port}")
        print(self.sock)

        self.buffer_size = buffer_size
        self.role = role

        while True:
            conn, addr = self.sock.accept()
            print(f"Connected to {addr}")

            data = b''
            while True:
                aux = conn.recv(self.buffer_size)
                data += aux
                if not aux or len(aux) < self.buffer_size:
                    print(f"Received {len(data)} bytes")
                    break
            
            try:
                data = pickle.loads(data)
            except Exception as e:
                conn.send(pickle.dumps(f'Could not decode data, error: {e}'))
                conn.close()
                continue
            """
            data = {'op': str
                    'file_name': str
                    'tolerance': int
                    'data': bytes}
            """            
            if data['op'] == 'deposit':
                try:
                    self.deposit(data['file_name'], data['data'], data['tolerance'])
                except Exception as e:
                    print(e)
                    conn.send(pickle.dumps(f'Could not deposit file, error: {e}'))
                    conn.close()
                    continue
                qtd = check_indexes(data['file_name'])
                qtd = sum([1 if x == '1' else 0 for x in qtd])
                conn.send(pickle.dumps(f'{qtd} File(s) deposited'))
                conn.close()

            elif data['op'] == 'retrieve':
                try:
                    self.retrieve(data['file_name'])
                    print('foi')
                except Exception as e:
                    print(e)
                    conn.send(pickle.dumps(f'Could not be retrieved, error: {e}'))
                    conn.close()
                    continue
                conn.send(pickle.dumps('retrieved'))
                conn.close()
            
            elif data['op'] == 'edit':
                try:
                    self.edit(data['file_name'], data['tolerance'])
                except Exception as e:
                    print(e)
                    conn.send(pickle.dumps(f'Could not be edited, error: {e}'))
                    conn.close()
                    continue
                conn.send(pickle.dumps('edited'))
                conn.close()        

    def deposit(self, file_name, data, tolerance):
        indexes = check_indexes(file_name)
        qtd = 0
        
        if indexes:
            qtd = sum([1 if x == '1' else 0 for x in indexes])
            if qtd >= tolerance:
                raise Exception(f'File already exists and has {qtd} copies')

        if qtd < tolerance and ((indexes is not None and indexes[self.ports.index(self.port)] == '') or indexes is None):
            save_file(file_name, self.port, data, 'server')
            write_indexes(file_name, self.ports.index(self.port), '1')
            print('writei')

        indexes = check_indexes(file_name)
        if qtd < tolerance:
            for i, port in enumerate(self.ports):
                if port != self.port and indexes[i] != '1' and qtd < tolerance:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((socket.gethostname(), port))
                        print(f"Connected to {socket.gethostname()[1]}:{port}")
                        sock.send(pickle.dumps({'op': 'deposit', 'file_name': file_name, 'data': data, 'tolerance': tolerance}))
                        sock.close()
                    except Exception as e:
                        print(f"Could not connect to {socket.gethostname()[1]}:{port}")
                        continue
        return
    
    def retrieve(self, file_name):
        indexes = check_indexes(file_name)

        if '1' in indexes:
            where = indexes.index('1')

        if where is None:
            raise Exception(f'File does not exist')

        save_file(file_name, self.ports[where], None, 'client')
        return

    def edit(self, file_name, tolerance):
        indexes = check_indexes(file_name)
        qtd = 0
        
        if indexes:
            qtd = sum([1 if x == '1' else 0 for x in indexes])  
        if qtd == 0 or indexes is None:
            raise Exception(f'File does not exist')
        elif qtd < tolerance:
            where = indexes.index('1')
            filepath = os.path.join(CURRENT_PATH, f'{DATABASE_PATH}/{self.ports[where]}/{file_name}')
            data = get_bytes(filepath)
            self.deposit(file_name, data, tolerance)
        elif qtd > tolerance:
            to_rem = qtd - tolerance
            nums = [i for i, x in enumerate(indexes) if x == '1']
            while to_rem > 0:
                where = nums[-1]
                nums.pop()
                filepath = os.path.join(CURRENT_PATH, f'{DATABASE_PATH}/{self.ports[where]}/{file_name}')
                os.remove(filepath)
                write_indexes(file_name, where, '')
                to_rem -= 1
        return
