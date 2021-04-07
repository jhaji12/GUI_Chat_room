# import socket library
# import threading library
import socket
import threading

# Choose a port that is free
PORT = 50000

#gethostbyname() function of socket module returns the IP address of a given host name.
SERVER = socket.gethostbyname(socket.gethostname())

# Address is stored as a tuple with server and port number
ADDRESS = (SERVER, PORT)

#format of encoding and decoding
FORMAT = "utf-8"

#Lists that will contains all the clients connected to the server and their names.
clients, names = [], []

# Create a new socket for the server where AF_INET is the type of Address(will return IPv4) and Sock_STREAM is the TCP socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#bind function is used to bind the address of the server to the socket
server.bind(ADDRESS)


# function to start the connection
def startChat():
    print("server is working on " + SERVER)

    # it will check for any new connection
    server.listen()

    while True:
        # accept connections from the client and returns a new connection to the client and  the address bound to it
        connection, addr = server.accept()
        connection.send("NAME".encode(FORMAT))

        # connection.recv function will have maximum of 1024 data that can be received in bytes from clients
        name = connection.recv(1024).decode(FORMAT)

        # append the name and client
        # to the respective list
        names.append(name)
        clients.append(connection)

        print(f"Name is :{name}")
       # print(f"Client is:{client}")
        # broadcast message
        broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))

        connection.send('Connection successful!'.encode(FORMAT))

        # Start the receiving thread
        thread = threading.Thread(target=receive,
                                  args=(connection, addr))
        thread.start()

        # no. of clients connected
        # to the server
        print(f"active connections {threading.activeCount() - 1}")


# this function will receive the message from client taking arguement as connection and address
def receive(connection, addr):
    print(f"New connection has been created {addr}")
    connected = True

    while connected:
        # recieve message from client
        message = connection.recv(1024)

        # broadcast message to all other clients
        broadcastMessage(message)

    # close the connection
    connection.close()


#broadcast messages function will send the receive message from server to each clients
def broadcastMessage(message):
    for client in clients:
        client.send(message)


# Function call to start the communication among users
startChat()