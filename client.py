try:
    #importing socket and threading to work
    import socket, threading, sys, time, logging, os, platform
    from os import system

    logging.basicConfig(filename='ClientLog.log',encoding='utf-8',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info(f'\n\n ----- NEW Client INSTANCE -----\n OS Info: {platform.system()} : {platform.platform()} : {platform.version()} : {platform.architecture()} : {platform.machine()}: {platform.node()} : {platform.processor()}')
    
    #Local Vars
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

    #Port and IP config options. Either static or ask on launch
    #port = 12000
    #ip = '127.0.0.1'
    ip = input("Enter an IP/Hose address of Server (192.168.1.2/chatserver.com): ")
    port = int(input("Input the Port Number (444): "))
    #ip = input("Enter an IP/URL of Server (192.168.1.2): ")

    #Vars from client
    print({ip},{port})
    logging.info(f'Connection to: {ip} and on port: {port}')

    firstConn = True
    start = True
    #starting socket
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        print("Connection Sucesfull")
        logging.info("Connection was Succesfull")
    except Exception as error:
        logging.critical(f'Unable to connect due to this error: \n {error} \n\n Will Exit in 10 Seconds')
        print(f'Unable to connect due to this error: \n {error} \n\n Will Exit in 10 Seconds')
        time.sleep(10)
        exit()

    handle = input("Enter Your Handle: ")
    system("title "+(f'Connected to: {ip} with Port: {port} and Handle: {handle}'))
    logging.info(f'Handle Is: {handle}')

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
                        msg = client.recv(1024).decode(format)
                       # client.send(password.encode(format))
                        if msg == "REFUSE":
                            logging.info("Wrong Password - Disconnecting")
                            print("Wrong Password - Disconnecting")
                            stopThread = True
                        else:
                            print(msg)

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
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.critical(f'Line: {exc_tb.tb_lineno} : Type: {exc_type} : Take Function: {error}')
                print("Some Error Occured\nPress (Enter) to exit. ")
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
                logging.info(message)
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
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.critical(f'Line: {exc_tb.tb_lineno} : Type: {exc_type} : Error in Write Function: {error}')
                break

     

    #Threads for taking and writing
    threadTake = threading.Thread(target=take)
    threadTake.start()

    threadWrite = threading.Thread(target=write)
    threadWrite.start()

except Exception as error:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    logging.critical(f'Line: {exc_tb.tb_lineno} : Type: {exc_type} : Main TRY Error: {error}')
    print("Some Major Error Happened - Please send ClientLog.log to Developer!")
    input("Press (Enter) to close")
    exit()