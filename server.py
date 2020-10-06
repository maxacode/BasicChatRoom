    #Features:
        #*Connect as a user to a chat and msg other people

    #Feature to do
        #Colors for each user
        #Customizations
        #Logg all chat messages
        #Logg connection info
try:
    #importing socket and threading to work
    import socket, threading,time
    #from socket import *
    from threading import Thread

    #Server Variables
    #port = int(sys.argv[2])
    #ip = str(sys.argv[1])
    port = 444
    ip = '192.168.176.15'
    #ip = input("Enter an IP address of Server (192.168.1.2): ")
    #port = int(input("Input the Port Number (444): "))

    format = 'utf8'
    clients = []
    handles = []
    adminAccounts = {'admin':'adminpass','jane':'janepass'}

    #Custom Messages Varaibles
    disconnectMsg = "/close"
    kickMsg = "/kick"
    banMsg = "/ban"
    promoteMsg = "/promote"
    infoMs = "/info"
    msgMsg= "/msg"
    onlineMsg = "/online"
    helpMsg = "/help"
    regularCommands = ['/exit: To Exit the Program\n /help: For list of all commands\n /online: List of Who is Online']
    adminCommands = regularCommands + ['\n/kick: ''To kick a user temporarily \n /ban: To fully ban a username\n']
    #starting socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()

    #Functions with features.
    def kickUser(name,fromHandle):
        if name in handles:
            print("Starting Kick Process")
            nameIndex = handles.index(name)
            clientToKick = clients[nameIndex]
            clients.remove(clientToKick)
            clientToKick.send("YOu were kicked by an admin! \n Press (enter) to exit".encode(format))
            clientToKick.close()
            handles.remove(name)
            broadcast(f'{name} was kicked by an admin'.encode(format))

        else:
            print("Name not in hanldes")
            fromHandle.send("User not Online".encode(format))
    # def infoUser(origClient, name):
    #     if name in handles:
    #         nameIndex = handles.index(name)
    #         clientInfo = clients[nameIndex]
    #         info = clients(clientInfo)
    #         origClient.send(f"Info for user {name} is {info}".encode(format))
    #         broadcast(f'{origClient} got info about {name}'.encode(format))
    #



    #Funciton t send messages to everyone
    def broadcast(message):
        print(message)

        #sending a msg to all the clinets in teh client list
        for client in clients:
            client.send(message)
            #print("sent to all clients ")
            #Printing messages to server console screen.
            #print({str(message.decode(format))})

    # #Funciton t send messages to single user
    # def direct(client, message):
    #     #sending a msg to all the clinets in teh client list
    #     client.send(message)
    #     #Printing messages to server console screen.
    #     print({str(message.decode(format))})

    #Fucntion to receive client messages
    def handleMsg(client):
        while True:
            try:
                handle = handles[clients.index(client)]
                msg = client.recv(1024)

               # msg = msg.decode(format)
               # msg = msg.decode(format)
                command = str(msg.decode(format))

               # Checking if user sent a command.
                if command[len(handle)+2:len(handle)+3] == '/' and handle in adminAccounts:
                    print(f"{handle} -- is running {command}")
                    command = command[len(handle) + 2:]

                    if kickMsg in command:
                        print("Command is kick")
                        whoKick = command[6:]
                        # client.send("Attempting to Kick User")
                        print("Sending to kickUser def " )
                        kickUser(str(whoKick),client)

                    elif banMsg in command:
                        print("Command is ban")
                        whoBan = command[5:]
                        with open('Banned.txt','a+') as file:
                            file.write(f'{whoBan}\n')
                            print(f"{whoBan}-wrote user to ban file")
                        print("Sending to kickUser def " )
                        kickUser(str(whoBan),client)

                    elif helpMsg in command:
                        client.send(str(adminCommands).encode(format))
                    elif onlineMsg in command:
                        client.send(f'This is who is Online: \n{str(handles)}\n'.encode(format))

                    elif "/exit" in command:
                        if client in clients:
                            # Iff error happens we weill disconnect client and remove them from our list.
                            index = clients.index(client)
                            clients.remove(client)
                            client.close()
                            handle = handles[index]
                            handles.remove(handle)
                            print(f'{str(handle)} : left the chat! ')
                            broadcast(f'{str(handle)} : left the chat! '.encode(format))
                            continue

                    else:
                        client.send(f"\nNot a valid command, try these:\n {str(adminCommands)}\n".encode(format))

                elif onlineMsg in command:
                    client.send(f'This is who is Online: \n{str(handles)}\n'.encode(format))

                elif helpMsg in command:
                    client.send(str(regularCommands).encode(format))

                elif "/exit" in command:
                    if client in clients:
                        # Iff error happens we weill disconnect client and remove them from our list.
                        index = clients.index(client)
                        clients.remove(client)
                        client.close()
                        handle = handles[index]
                        handles.remove(handle)
                        print(f'{str(handle)} : left the chat! ')
                        broadcast(f'{str(handle)} : left the chat! '.encode(format))
                        continue

                elif command[len(handle)+2:len(handle)+3 ] == '/':
                    client.send("Not an Admin - Ask for a promotion".encode(format))
                    print(f"This was done----{command}----")


                else:
                   # print("Sending to brodcast")
                    broadcast(msg)


            except Exception as error:
                if client in clients:
                    print(error)
                    time.sleep(5 )
                    #Iff error happens we weill disconnect client and remove them from our list.
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    handle = handles[index]
                    handles.remove(handle)
                    #print(f'{str(handle)} : left the chat! ')
                    broadcast(f'{str(handle)} : left the chat! '.encode(format))
                    continue

    #FUnction to resive clients
    def take():
        while True:
            # Seeing if user        bannded

            try:
                #Recivng connection from clinet

                client, address = server.accept()
            except Exception as error:
                if client in clients:
                    print("Error")
                    client.send(error)
                    client.close()
                    continue

            syn = client.recv(1024).decode(format)

            if syn != 'SYN':
                client.close()
                continue


            print(f'!!!!!!!{str(client)} wth {str(address)}: has connected')
            #SYN TO Client
          #  client.send('MOTD: Welcome to Hacked.FYI Chat Room'.encode(format))

            #ACK and Handle To client
            client.send('HANDLE'.encode(format))


            #Handle From client
            handle = client.recv(1024).decode(format)
            #Chekcing if handle is less than 15 chars
            if len(handle) >= 20:
                client.send('Please have a handle less than 15 char'.encode(format))
                print("Handle bigger than 20 chars")
                #print(error)
                client.close()
                continue
            else:
                #client.send("\nHandle Accepted \n ".encode(format))
                print("Handle Acepted")
            #print(f'-{handle}-')
            #
            with open('Banned.txt', 'r') as file:
                banned = file.readlines()

            print(banned)
            if handle+'\n' in banned:
                print(f'{handle} is in Banned list - ')
                client.send('BAN'.encode(format))
                time.sleep(5)
                client.close()
                continue
            else:
                print(print(f'-{handle}- not banned'))

            try:
                print("Trying if handle in adminAccounts")
                #Seeing if user has admin rights
                if handle in adminAccounts:
                    print("Handle in admin accounts")

                    client.send("PASS".encode(format))

                    password = client.recv(1024).decode(format)
                    print(f'-{password}-')
                    print(password[len(handle)+2:])
                    #Checking if password is right
                    if password[len(handle)+2:] != adminAccounts[handle]:

                        print("Wrong pass word")
                        client.send("REFUSE".encode(format))
                        client.close()
                        continue
                    else:
                        client.send('You are an Admin! Welcome'.encode(format))
                        print(f'Admin: {handle} has connected to server')
            except Exception as error:
                print("Error during auth of admin user")
                print(error)
                pass
            #Adding new user info to our list
            print("Adding to clients list")
            handles.append(handle)
            clients.append(client)

            #printing to console the handle of user and telling eveyrone who joined. and telling client they are on the serve.r
            #print(f'User with Handle: {str(handle)} connected')
            client.send(f'\nConnected to server with Handle: {str(handle)}'.encode(format))
            broadcast("\n--- {} joined!---\n".format(handle).encode(format))
            client.send(f'This is who is Online: {str(handles)}'.encode(format))
            #Starting the thread to handle Clients
            threadHandle = threading.Thread(target=handleMsg, args=(client,))
            threadHandle.start()


    print(f"Starting Server on {ip,port}")
    take()
except Exception as error:
    print(error)
    print("Main errror")

    take()
