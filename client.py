#importing socket and threading to work
import socket, threading, sys, time

#Server Variables
#port = int(sys.argv[2])
#ip = str(sys.argv[1])
#port = 444
#ip = '18.223.49.228'
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

#if len(sys.argv) != 3:
 #   print("Correct usage: script, IP address, port number")
  #  exit()

ip = input("Enter an IP address of Server (192.168.1.2): ")
port = int(input("Input the Port Number (444): "))
#Vars from client
print({ip},{port})
#handle = input("What is your Handle: ")
#password = input("Enter Password: ") if handle == 'admin' or  handle == 'jane' else print(" ")

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
        global stopThread
        if stopThread:
            break
        try:

            message = client.recv(1024).decode(format)
           # print(message)
            #print("input: ")

            if "HANDLE" in message:
               # print("Handle in Message")
                client.send(handle.encode(format))

                #If server asks for a keyword do this
                nextMessage = client.recv(1024).decode(format)
              # print(nextMessage)

                if 'PASS' in nextMessage:
                    print("Enter Password:")
                    #print('cleint Enter Pass Here:')
                   # password = input("")
                    #nextMessage = client.recv(1024).decode(format)
                   # print(nextMessage)d

                  #  print("Sending Password.")
                   # client.send(password.encode(format))
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
            time.sleep()
            exit()
            break

#Write fucntions
def write():
    while True:
        #Makisng sure user logged in
        if stopThread:
            break
        try:
         #   print(handle)
            message = '{}: {}'.format(handle, input(''))
         ##   print('before if message')
            if message[len(handle)+2:].startswith('/'):
                if message[len(handle)+2:].startswith('/exit'):
                    print("Exiting now!")
                    time.sleep(3)
                    client.close()
                    exit()
                else:
                    client.send(message.encode(format))

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
            else:
            #    print('sending to cly. ')
                client.send(message.encode(format))

        except Exception as error:
            print("Error in write functions")
            print(error)
            pass


#Threads for taking and writing
threadTake = threading.Thread(target=take)
threadTake.start()

threadWrite = threading.Thread(target=write)
threadWrite.start()
