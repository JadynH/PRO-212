from glob import glob
from logging import handlers
import socket
from threading import Thread
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

IP_ADDRESS = '192.168.1.26'
PORT= 8050
SERVER = None
BUFFER_SIZE = 4096
clients = {}



is_dir_exists = os.path.isdir('shared_files')
print(is_dir_exists)
if(not is_dir_exists):
    os.makedirs('shared_files')





def acceptConnections():
    global SERVER
    global clients
    
    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client" : client,
            "address": addr,
            "connected_width": "",
            "file_name": "",
            "file_size" : 4096
        }
        print(f"Connection established width {client_name} : {addr}")
        
        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()


def setup():
    print("\n\t\t\t\t\t\t IP MESSENGER\n")

    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(100)

    print("\t\t\t\t SERVER IS WAITING FOR INCOMING CONNECTIONS...")
    print("\n")

    acceptConnections()

setup_thread = Thread(target=setup)
setup_thread.start()


def ftp():
    global IP_ADDRESS

    authorizer = DummyAuthorizer()
    authorizer.add_user("lftpd","lftpd",".",perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer


    ftp_server = FTPServer((IP_ADDRESS,21),handler)
    ftp_server.serve_forever()
setup_thread = Thread(target=setup)
setup_thread.start()
