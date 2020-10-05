#importing socket and threading to work
import socket, threading, sys

#Server Variables
#port = int(sys.argv[2])
#ip = str(sys.argv[1])
port = 443
ip = '192.168.176.15'
format = 'utf8'
clients = []
handles = []
stopThread = False

#Custom Messages Varaibles
disconnectMsg = "/close"
kickMsg = "/kick"
banMsg = "/ban"
promoteToAdmin = "/promote"
userConnInfo = "/info"
msgToSingleClient = "/msg"

#if len(sys.argv) != 3:
 #   print("Correct usage: script, IP address, port number")
  #  exit()

#Vars from client
handle = input("What is your Handle: ")
password = input("Enter Password: ") if handle == 'admin' or  handle == 'jane' else print(" ")

#starting socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

#Reciving fucntion
def take():
    while True:
        global stopThread
        if stopThread:
            break
        try:
            message = client.recv(1024).decode(format)
            if message == "HANDLE":
                client.send(handle.encode(format))

                #If server asks for a keyword do this
                nextMessage = client.recv(1024).decode(format)
                if nextMessage == 'PASS':
                    client.send(password.encode(format))
                    if client.recv(1024).decode(format) == "REFUSE":
                        print("Wrong Password - Disconnecting")
                        stopThread = True

                elif nextMessage == "BAN":
                    print("You are Banned! Hint:Try another username")
                    print("Logging Off!")
                    stopThread = True
            else:
                print(message)
        except:
            print("Some Error Occured")
            client.close()
            break

#Write fucntions
def write():
    while True:
        #Makisng sure user logged in
        if stopThread:
            break
        message = '{}: {}'.format(handle, input(''))
       # if message[len(handle)+2:].startswith('/'):
            #Maksing sure its admin
           # if handle == 'admin':
                #If Kick in message
           #     if message[len(handle)+2:].startswith('/ban'):
            #        client.send(f'BAN {message[len(handle)+2+5:]}'.encode(format))
                # If /ban in message
               # elif message[len(handle) + 2:].startswith('/ban'):
                #    client.send(f'BAN {message[len(handle)+2+5:]}'.encode(format))
                # If /info in message
                # elif message[len(handle) + 2:].startswith('/info'):
                #     client.send(f'INFO {message[len(handle)+2+6:]}'.encode(format))
          #  else:
           #     print("Command only allowed for Admin")
       # else:
        client.send(message.encode(format))


#Threads for taking and writing
threadTake = threading.Thread(target=take)
threadTake.start()

threadWrite = threading.Thread(target=write)
threadWrite.start()
