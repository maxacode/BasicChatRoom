#importing socket and threading to work
import socket, threading

headerSize = 64
serverPort = 443
serverIP = '192.168.176.15'
serverConn =(serverIP,serverPort)
decodeFormat = 'utf-8'
#starting socket
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind((serverIP, serverPort))
disconnectMsg = "/close"

#Funciton to handle cleint
def handle_client(conn,addr):
    connection = True
    while connection:
        msgLen = conn.resv(headerSize).decode(decodeFormat)
        mesLen = int(msgLen)
        msg = conn.resv(msgLen).decode(decodeFormat)
        connection = False if msg == disconnectMsg else True
        print(f"({addr}: {msg}")
    conn.send("Closing Connection".encode(decodeFormat))
    conn.close()
    print("Clossing Connecition")

#Starting the server.
def start():
    #Starting the listing fora client
    serverSock.listen()
    while True:
        #Recieving the connection from client
        conn, addr = serverSock.accept()
        print(f"New COnnection from: {conn, addr}")
        conn.send("Welcome!".encode(decodeFormat))
        #Starting the handle_client funct in a thread.
        threadHandleClient = threading.Thread(target=handle_client, args=(conn,addr))
        print(f"Active Connections: {threading.activeCount() - 1}")


print("Server is starting on: {}".format(serverConn))
start()