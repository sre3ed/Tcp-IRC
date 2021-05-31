from colored import fore, back, style
import socket
import threading

alias = input('Choose an alias >>> ')
if alias == "proadmin":
    password = input("enter the password :")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 4444))

stop_thread = False


def client_receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(4096).decode('ascii')
            if message == "alias?":
                client.send(alias.encode('ascii'))
                next_message = client.recv(4096).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(4096).decode('ascii') == 'REFUSE':
                        print("error in connection ")
                        stop_thread = True
                elif next_message == 'BAN':
                    print('connection refused because of BAN')
                    client.close()
                    stop_thread = True
            else:
                print(fore.LIGHT_BLUE + back.RED + style.BOLD +
                      "--#~" + message + style.RESET)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        if stop_thread:
            break
        message = f'{alias}: {input("")}'
        if message[len(alias)+2:].startswith('/'):
            if alias == 'proadmin':
                if message[len(alias)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(alias)+2+6:]}'.encode('ascii'))
                elif message[len(alias)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(alias)+2+5:]}'.encode('ascii'))
            else:
                print("commands can only be executed by admin")
        else:
            client.send(message.encode('ascii'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
