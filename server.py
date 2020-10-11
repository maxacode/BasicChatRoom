    #Features:
        #*Connect as a user to a chat and msg other people

    #Feature to do
        #Colors for each user
        #Customizations
        #Logg all chat messages
        #Logg connection info
try:
    #importing socket and threading to work
    import socket, threading,time,random, uuid, hashlib
    from os import system
    #from socket import *
    from threading import Thread
    #Port and IP config options. Either static or ask on launch
    port = 12000
    ip = '127.0.0.1'
    #ip = input("Enter an IP address of Server (192.168.1.2): ")
    #port = int(input("Input the Port Number (444): "))

    #local Vars
    format = 'utf8'
    clients = []
    handles = []
    adminAccounts = []
    stopThread = False

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
    try:
        print(f'Trying: {ip} and {port}')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen()
        server.status
    except Exception as error:
        print(f'THis error occured when starting server socket: {error}')
        #INcreasing socket port number by random 1 to 999 if first bind fails.
        a = random.randint(1,999)
        port += a
        print(f'Trying: {ip} and {port}')

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen()
        system("title "+(f'Connected to: {ip} with Port: {port}.'))

    #Creating adminaccounts from user input
    while True:
        with open('.adminAccounts.encrypted','r') as file:
            adminAccounts = dict(map(str.split, file))
            print(f'These are the existing admin accounts: {adminAccounts}\n')
            cont = input("Would you like to add more admin Accounts? (y/n): ") 
            if cont == 'n': 
                break
        adminUsers = input("\nEnter a username for a admin account (Type in 'done' when finished): ")
        if adminUsers == 'done':
            break
        #Making sure passwords match
        while True:
            adminPass = input("Enter Password: ")
            adminPass2 = input("Re-Enter Password: ") 
            if adminPass2 != adminPass:
                print("Passwords dont match - lets try again")
                continue
            else:
                print(f'Account: {adminUsers} with password: {adminPass} was added to server admins! \n')
                break
        #hashing password
        salt = uuid.uuid4().hex
        print(salt)
        hashedPass = hashlib.sha256(salt.encode() + adminPass.encode()).hexdigest() + ':' + salt

        #writing account info to file and adding it to varible that will be used to check later. 
        with open('.adminAccounts.encrypted','a+') as file:
            account = (adminUsers + ' ' + hashedPass) 
            file.write(f'{account}\n')
            print(f"{account}-wrote user to adminAccounts file")

    print("-----Done with Admin account creation!-----\n")
    #Getting accounts from file 
    with open('.adminAccounts.encrypted','r') as file:
        adminAccounts = dict(map(str.split, file))

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

    #Funciton t send messages to everyone
    def broadcast(message):
        print(message)

        #sending a msg to all the clinets in teh client list
        for client in clients:
            client.send(message)
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
                     #Iff error happens we weill disconnect client and remove them from our list.
                    index = clients.index(client)
                    clients.remove(client)
                    #client.close()
                    handle = handles[index]
                    handles.remove(handle)
                    #print(f'{str(handle)} : left the chat! ')
                    broadcast(f'{str(handle)} : left the chat! '.encode(format))
                    continue

    #FUnction to resive clients
    def take():
        while True:

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

        # Seeing if user        bannded
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
                with open('.adminAccounts.encrypted','r') as file:
                    adminAccounts = dict(map(str.split, file))
                           # print(adminAccounts)
                    #adminAccounts = {'admin':'adminpass','jane':'janepass'}
                print(adminAccounts)

                print("Trying if handle in adminAccounts {}".format(handle))
                #Seeing if user has admin rights

                if handle in adminAccounts:
                    print("Handle in admin accounts")

                    client.send("PASS".encode(format))

                    password = client.recv(1024).decode(format)
                    password = password[len(handle)+2:]
                    print(f'-{password}-')
                    print(password[len(handle)+2:])
                    #Checking if password is right
                    hashPass, salt = adminAccounts[handle].split(':')
                    enteredHashedPass = hashlib.sha256(salt.encode()+password.encode()).hexdigest()

                    if enteredHashedPass != hashPass:
                        print("WRong password")
                        client.send("REFUSE".encode(format))
                        client.close()  
                        continue

                    else:
                        client.send('You are an Admin! Welcome'.encode(format))
                        print(f'Admin: {handle} has connected to server')
                else:
                    print("User not in adminAccounts")
            except Exception as error:
                print("Error during auth of admin user")
                print(error)
                pass

            #Adding new user info to our list
            print("Adding to clients list")
            handles.append(handle)
            clients.append(client)

            #printing to console the handle of user and telling eveyrone who joined. and telling client they are on the serve.r
            client.send(f'\nConnected to server with Handle: {str(handle)}'.encode(format))
            broadcast("\n--- {} joined!---\n".format(handle).encode(format))
            client.send(f'This is who is Online: {str(handles)}'.encode(format))
            #Starting the thread to handle Clients
            threadHandle = threading.Thread(target=handleMsg, args=(client,))
            threadHandle.start()

    #Function for teh server to write commands and reboot
    def write():
        while True:
            global stopThread
            if stopThread:
                for x in clients:
                    x.close()
                    break
            #input from server
            serverName = '-----Server: '
            message =input('')
            #checking if special command. 
            if message.startswith('/'):
                closeIn = int(input("When to shut down server: "))
                howLongDown = int(input("How long will it be down: "))

                if message.startswith('/close'):
                    reason = ('{} \n Will shut down in: {} Seconds! \n and will come back in {} Min!\n'.format(serverName, message[7:],closeIn, howLongDown))
                   # reason = serverName + message[7:] + ' Will shut down in: ' + {closeIn} + 'Min! \n ' 
                    broadcast(reason.encode(format))
                    time.sleep(closeIn)
                    stopThread = True
            else:
                broadcast(f'\n {serverName} {message} \n'.encode(format))


    print(f"Starting Server on {ip,port}")
    #take()
    threadTake = threading.Thread(target=take)
    threadTake.start()

    threadWrite = threading.Thread(target=write)
    threadWrite.start()

except Exception as error:
    print(error)
    print("Main errror")
    input('Press Enter to exit')