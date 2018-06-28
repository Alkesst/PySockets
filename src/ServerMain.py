from src.Server.Server import Server


def main():
    """
    Main app for the server.
    :return: void
    """
    server = Server(12345)
    try:
        while True:
            server.accept_connection()
            print('{}:{} connected to the server...'.format(server.client_address[0], server.client_address[1]))
            server.send(b'Bienvenido al servidor de cifrado')
            offset = None
            while offset != 0:
                offset = int(server.receive())
                if offset != 0:
                    received_message = server.receive()
                    message_to_send = Server.codify(received_message.encode(), offset)
                    server.send(message_to_send)
                    print('Client ' + server.client_address[0] + ' sends offset: ' + str(offset), end='')
                    print('Client ' + server.client_address[0] + ' sends message: ' + received_message, end='')
                    print('Message sent to the client: ' + message_to_send.decode(), end='')
            server.send(b'OK\n')
            server.close()
            print('Connection with {} closed...'.format(server.client_address[0]))
    except KeyboardInterrupt:
        server.close_server()
        exit(1)


if __name__ == '__main__':
    main()
