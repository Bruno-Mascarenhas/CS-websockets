import os

DATABASE_PATH = "../database"
CLIENT_PATH = "../files"
CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))

def check_file(file_name):
    if os.path.isfile(file_name):
        return True
    else:
        return False

def save_file(file_name, port, data, mode = 'server'):
    if mode == 'client':
        file_path = os.path.join(CURRENT_PATH, f'{CLIENT_PATH}/{file_name}')
    else:
        file_path = os.path.join(CURRENT_PATH, f'{DATABASE_PATH}/{port}/{file_name}')

    if mode == 'client':
        data = get_bytes(os.path.join(CURRENT_PATH, f'{DATABASE_PATH}/{port}/{file_name}'))

    if not check_file(file_path):
        with open(file_path, "wb") as f:
            f.write(data)
    return

def get_bytes(file_path):
    if check_file(file_path):
        return open(file_path, "rb").read()
    return

def delete_file(file_name, port):
    rel_path = os.path.join(CURRENT_PATH,f'{DATABASE_PATH}/{port}/{file_name}')
    if check_file(rel_path):
        os.remove(file_name)
    return

def check_indexes(file_name):
    rel_path = os.path.join(CURRENT_PATH,f'{DATABASE_PATH}/indexes.txt')
    indexes = open(rel_path).readlines()
    for index in indexes:
        line = index.split(';')
        if line[0] == file_name:
            return line[1:-1]
    return None

def write_indexes(file_name, port, value):
    rel_path = os.path.join(CURRENT_PATH,f'{DATABASE_PATH}/indexes.txt')
    if check_indexes(file_name) is not None:
        indexes = open(rel_path, 'r').readlines()
        where = -1
        for i, index in enumerate(indexes):
            line = index.split(';')
            if line[0] == file_name:
                where = i
                break
        aux = indexes[where].split(';')
        aux[port+1] = value
        indexes[where] = ';'.join(aux)
        with open(rel_path, 'w') as f:
            f.writelines(indexes)
    else:
        with open(rel_path, 'a') as f:
            aux = f'{file_name};;;;;\n'.split(';')
            aux[port+1] = value
            f.write(';'.join(aux))
    return

def remove_indexes(file_name):
    rel_path = os.path.join(CURRENT_PATH,f'{DATABASE_PATH}/indexes.txt')
    if check_indexes(file_name) is not None:
        indexes = open(rel_path, 'r').readlines()
        where = -1
        for i, index in enumerate(indexes):
            line = index.split(';')
            if line[0] == file_name:
                where = i
                break

        indexes.pop(where)
        with open(rel_path, 'w') as f:
            f.writelines(indexes)
    return

def show_indexes():
    rel_path = os.path.join(CURRENT_PATH,f'{DATABASE_PATH}/indexes.txt')
    find = 0
    if check_file(rel_path) is not None:
        indexes = open(rel_path, 'r').readlines()
        for index in indexes:
            line = index.split(';')
            if '1' in line:
                find = 1
                print(line[0])
    if find == 0 or check_file(rel_path) is None:
        print('No records found')
    return