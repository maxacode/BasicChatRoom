#importing socket and threading to work
import socket, threading, sys, time

#Server Variables
#port = int(sys.argv[2])
#ip = str(sys.argv[1])
#port = 444
#ip = 'hacked.fyi'
#ip = '192.168.176.15'
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

ip = input("Enter an IP/URL of Server (192.168.1.2): ")
port = int(input("Input the Port Number (444): "))
#Vars from client
print({ip},{port})
#handle = input("What is your Handle: ")
#password = input("Enter Password: ") if handle == 'admin' or  handle == 'jane' else print(" ")
firstConn = True
start = True

#starting socket
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print("Connection Succesfful")
except Exception as error:
    print(f'Unable to connect due to this error: \n {error} \n\n Will Exit in 10 Seconds')
    time.sleep(10)
    exit()

handle = input("Enter Your Handle: ")

#Reciving fucntion
def take():
    while True:
        global stopThread, firstConn
        if stopThread:
            break
        try:
            if firstConn == True:
                client.send('SYN'.encode(format))
                firstConn = False

            message = client.recv(1024).decode(format)
           # Chekcing if server sent special instructions.
            if "HANDLE" in message:
               # print("Handle in Message")
                client.send(handle.encode(format))

                #If server asks for a keyword do this
                nextMessage = client.recv(1024).decode(format)
              # print(nextMessage)

                if 'PASS' in nextMessage:
                    print("Enter Password:")

                   # client.send(password.encode(format))
                    if client.recv(1024).decode(format) == "REFUSE":
                        print("Wrong Password - Disconnecting")
                        stopThread = True

                elif nextMessage == "BAN":
                    print("You are Banned! Hint:Try another username")
                    print("Logging Off!")
                    stopThread = True

            elif "were kicked by an admin!" in message:
                print(message)
                stopThread = True

            else:
                print(message)

        except Exception as error:
            print(error)
            print("Some Error Occured\nPress (Enter) to exit. ")
            #time.sleep(2)
            break

#Write fucntions
def write():
    while True:
        global stopThread
         #Makisng sure user logged in
        if stopThread:
            client.close()
            break
        try:
         #   print(handle)
            message = '{}: {}'.format(handle, input(''))
         ##   print('before if message')
            if message[len(handle)+2:].startswith('/'):
                if message[len(handle)+2:].startswith('/exit'):
                    client.send(message.encode(format))
                    stopThread = True
                else:
                    client.send(message.encode(format))
            else:
                client.send(message.encode(format))
        except Exception as error:
            print("Error in write functions")
            print(error)
            break


#Threads for taking and writing
threadTake = threading.Thread(target=take)
threadTake.start()

threadWrite = threading.Thread(target=write)
threadWrite.start()
