import socket
import threading
import validators
from django.core.validators import URLValidator
#from urlparse import urlparse
from urllib.parse import urlparse
from django.core.exceptions import ValidationError
host = '127.0.0.1'
port = 55555
# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
def uri_validator(x):
    try:
        result = urlparse(x)
        #print('valid url')
        return all([result.scheme, result.netloc])
    except:
        return False
def broadcast(message):
    for client in clients:
        client.send(message)
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            #print('received an URL')
            broadcast(message)
            #print(client.recv(1024))
            uri_validator(message)
            if(uri_validator(message) == True):
                print('received url')
                reaction = client.recv(5)
                if (reaction == 5):
                    broadcast("{} loves this!".format(nickname).encode('ascii'))
                elif (reaction == 4):
                    broadcast("{} Okay with it!".format(nickname).encode('ascii'))
                else:
                    broadcast("{} hates this!".format(nickname).encode('ascii'))
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
