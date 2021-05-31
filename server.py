import threading
import socket

host = '127.0.0.1'
port = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []


def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections


def handle_client(client):
    while True:
        try:
            msg = message = client.recv(4096)
            if msg.decode('ascii').startswith('KICK'):
                if aliases[clients.index(client) == 'proadmin']:
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('command was refused!'.encode('ascii'))

            elif msg.decode('ascii').startswith('BAN'):
                if aliases[clients.index(client) == 'proadmin']:
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban}was banned!')
                else:
                    client.send('command was refused!'.encode('ascii'))
            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                broadcast(f'{alias} has left the chat room!'.encode('ascii'))
                aliases.remove(alias)
                break
# Main function to receive the clients connection


def receive():
    while True:
        print('Server is UP and  running...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('ascii'))
        # new line
        alias = client.recv(4096).decode('ascii')

        with open('bans.txt', 'r') as f:
            bans = f.readline()

        if alias+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if alias == "proadmin":
            client.send('PASS'.encode('ascii'))
            password = client.recv(4096).decode('ascii')
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}')
        broadcast(f'{alias} has connected to the chat room'.encode('ascii'))
        client.send('you are now connected!'.encode('ascii'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


def kick_user(name):
    if name in aliases:
        name_index = aliases.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin'.encode('ascii'))
        client_to_kick.close()
        aliases.remove(name)
        broadcast(f'{name} was kicked by an admin!'.encode('ascii'))

if __name__ == "__main__":
    receive()
