import threading
import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 9000))
server.listen()

clients = []
nicknames = []
database = []
filebase = []

def broadcast(client, message):
    for client_aux in clients:
        if client_aux == client:
            continue
        client_aux.send(message)

def unicast(message,client):
    client.send(message)

def check_offline_messages(nickname,client):

    client.send('\nOFFLINE MESSAGES:'.encode('utf-8'))
    time.sleep(0.1)

    if nickname in database:
        while nickname in database:
            index = database.index(nickname) + 1
            client.send(('[OFFLINE] ' + database[index] + '\n').encode('utf-8'))
            del database[index]
            del database[index-1]

    else:
        client.send('[NO MESSAGES]\n'.encode('utf-8'))

def check_offline_files(nickname,client):

    client.send('\nOFFLINE FILES:'.encode('utf-8'))
    time.sleep(0.1)

    if nickname in filebase:
        while nickname in filebase:
            index = filebase.index(nickname) + 1
            message = filebase[index]
            client.send(('fileoff ' + message).encode('utf-8'))
            del filebase[index]
            del filebase[index-1]

    else:
        client.send('[NO FILES]\n'.encode('utf-8'))

def client_sent(client):

    while True:
        message_raw = client.recv(1024).decode('utf-8')
        client_sent, msg = message_raw.split(' ', 1)

        try:
   
            if msg[0:3] == '/p ':
 
                command, nickname_and_message = msg.split(' ', 1)
                nickname, message = nickname_and_message.split(' ', 1)
                
                if nickname in nicknames:
                
                    index = nicknames.index(nickname)
                    message_enc = ("[PRIVATE] " + client_sent + " " + message).encode('utf-8')
                    unicast(message_enc, clients[index])

                elif not (nickname in nicknames):
                    database.append(nickname)
                    database.append(client_sent + " " + message)

            elif msg[0:3] == '/s ':

                command, nickname_filename = msg.split(' ', 1)
                nickname, filename = nickname_filename.split(' ', 1)

                client.send(('filename ' + filename).encode('utf-8'))

                file = open(filename, "w")
                #print("\nFilename received")

                data = client.recv(1024).decode('utf-8')
                #print("\nFile data received")
                    
                file.write(data)
                file.close()
                
                if nickname in nicknames:

                    message_enc =('file ' + client_sent + ' ' + filename + ' ' + data).encode('utf-8')
                    index = nicknames.index(nickname)
                    unicast(message_enc, clients[index])
                
                elif not (nickname in nicknames):
                    
                    filebase.append(nickname)
                    filebase.append(client_sent + ' ' + filename + ' ' + data)

            elif msg[0:6] == '/sall ':
            
                command, filename = msg.split(' ', 1)
                client.send(('filename ' + filename).encode('utf-8'))

                file = open(filename, "w")
                #print("\nFilename received")

                data = client.recv(1024).decode('utf-8')
                #print("\nFile data received")
                
                file.write(data)
                message_enc =('file ' + client_sent + ' ' + filename + ' ' + data).encode('utf-8')
                broadcast(client,message_enc)
                file.close()

            elif msg[0:2] == '/o':
        
                client.send(('\n[ONLINE CLIENTS]\n').encode('utf-8'))
                for nicknames_aux in nicknames:
                    client.send((nicknames_aux + "\n").encode('utf-8'))
            
            else:
                message_enc = message_raw.encode('utf-8')
                broadcast(client, message_enc)
            
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname_off = nicknames[index]
            nicknames.remove(nickname_off)
            client.close()
            break
            
def receive():
    while True:

        print('Server is running...')
        client, address = server.accept()
        print(f'{str(address)} is now connected')
        client.send('nickname'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f'{nickname} connected ...'.encode('utf-8'))
        broadcast(client, f'{nickname} entered the room\n'.encode('utf-8'))
        client.send('Connection established!'.encode('utf-8'))
        check_offline_messages(nickname,client)
        check_offline_files(nickname,client)
        thread = threading.Thread(target = client_sent, args=(client,))
        thread.start()
        print(nicknames)

if __name__ == "__main__":
    receive()
