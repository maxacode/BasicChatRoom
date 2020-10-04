#Features:
    #*Connect as a user to a chat and msg other people

#Feature to do
    #Colors for each user
    #Customizations
    #Logg all chat messages
    #Logg connection info

#importing socket and threading to work
import socket, threading

#Server Variables
port = 443
ip = '192.168.176.15'
format = 'ascii'
clients = []
handles = []
adminAccounts = {'admin':'adminpass','jane':'janepass'}

#Custom Messages Varaibles
disconnectMsg = "/close"
kickMsg = "/kick"
banMsg = "/ban"
promoteToAdmin = "/promote"
userConnInfo = "/info"
msgToSingleClient = "/msg"

#Functions with features.
def kickUser(name):
    if name in handles:
        nameIndex = handles.index(name)
        clientToKick = clients[nameIndex]
        clients.remove(clientToKick)
        clientToKick.send("YOu were kicked by an admin!".encode(format))
        clientToKick.close()
        handles.remove(name)
        broadcast(f'{name} was kicked by an admin'.encode(format))

def infoUser(origClient, name):
    if name in handles:
        nameIndex = handles.index(name)
        clientInfo = clients[nameIndex]
        info = clients(clientInfo)
        origClient.send(f"Info for user {name} is {info}".encode(format))
        broadcast(f'{origClient} got info about {name}'.encode(format))


#starting socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()

#Funciton t send messages to everyone
def broadcast(message):
    #sending a msg to all the clinets in teh client list
    for client in clients:
        client.send(message)
        #Printing messages to server console screen.
        print({str(message.decode(format))})

#Funciton t send messages to single user
def direct(client, message):
    #sending a msg to all the clinets in teh client list
    client.send(message)
    #Printing messages to server console screen.
    print({str(message.decode(format))})

#Fucntion to receive client messages
def handleMsg(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg in adminAccounts:
                if msg.decode(format).startswith('KICK'):
                    whoKick = msg.decode(format)[5:]
                    kickUser(whoKick)

                elif msg.decode(format).startswith('BAN'):
                    whoBan = msg.decode(format)[4:]
                    kickUser(whoBan)
                    #Adding handle to ban list
                    with open('Banned.txt','w') as file:
                        file.write(f'{whoBan}\n')
                    broadcast(f'{whoBan} was banned by {client}')

                elif msg.decode(format).startswith('INFO'):
                    whoInfo = msg.decode(format)[5:]
                    infoUser(client, whoInfo)


            broadcast(message)


        except:
            #Iff error happens we weill disconnect client and remove them from our list.
            index = clients.index(client)
            clients.remove(client)
            client.close()
            handle = handles[index]
            handles.remove(handle)

            broadcast(f'{str(handle)} : left the chat! '.encode(format))
            break

#FUnction to resive clients
def take():
    while True:
        #Recivng connection from clinet
        client, address = server.accept()
        print(f'!!!!!!!{str(client)} wth {str(address)}: has connected')

        #Asking for handle
        client.send('HANDLE'.encode(format))
        handle = client.recv(1024).decode(format)

        #Seeing if user bannded
        with open('Banned.txt','r') as file:
            banned = file.readlines()
        if handle+'\n' in banned:
            client.send('BANNED'.encode(format))
            client.close()
            continue

        #Seeing if user has admin rights
        if handle in adminAccounts:
            client.send("PASS".encode(format))
            password = client.recv(1024).decode(format)

            #Checking if password is right
            if password != adminAccounts[handle]:
                client.send("REFUSE".encode(format))
                client.close()
                continue


        #Adding new user info to our list
        handles.append(handle)
        clients.append(client)

        #printing to console the handle of user and telling eveyrone who joined. and telling client they are on the serve.r
        print(f'User with Handle: {str(handle)} connected')
        client.send(f'\nConnected to server with Handle: {str(handle)}'.encode(format))
        broadcast("{} joined!\n".format(handle).encode(format))

        #Starting the thread to handle Clients
        threadHandle = threading.Thread(target=handleMsg, args=(client,))
        threadHandle.start()


print(f"Starting Server on {ip,port}")
take()
