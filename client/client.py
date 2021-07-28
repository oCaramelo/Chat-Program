import threading
import socket

nickname = input('Choose nickame: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9000))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == "nickname":
                client.send(nickname.encode('utf-8'))

            elif message[0:9] == 'filename ':

                flag, filename = message.split(' ', 1)
                file = open(filename, "r")
                data = file.read()
                client.send(data.encode('utf-8'))
                file.close()

            elif message[0:5] == 'file ':
                
                flag, client_sent_filename_data = message.split(' ', 1)
                client_sent, filename_data = client_sent_filename_data.split(' ', 1)
                filename, data = filename_data.split(' ', 1)

                file = open(filename, "w")
                file.write(data)
                client_sent = client_sent.replace(':', ' ')
                print("\n" + client_sent + "sent you a file ( " + filename + " )")
                file.close()

            elif message[0:8] == 'fileoff ':
                
                flag, client_sent_filename_data = message.split(' ', 1)
                client_sent, filename_data = client_sent_filename_data.split(' ', 1)
                filename, data = filename_data.split(' ', 1)
                file = open(filename, "w")
                file.write(data)
                client_sent = client_sent.replace(':', ' ')
                print("\n[OFFLINE FILES] " + client_sent + "sent you a file ( " + filename + " )")
                file.close()

            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

def client_send():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()