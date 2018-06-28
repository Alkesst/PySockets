import socket
import sys


class Server(object):
    def __init__(self, port_to_listen: int):
        """
        Creates the server socket, assigns the port to listen and begin to listen in the
        assigned port and the 0.0.0.0 network by default Java uses 0.0.0.0 network.
        :param port_to_listen: I think that the name is clearly descriptive
        """
        self.MAXLEN = 2048
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__port = port_to_listen
        self.__client_socket = None
        self.__client_address = None
        try:
            self.__server_socket.bind(('0.0.0.0', port_to_listen))              
            self.__server_socket.listen(port_to_listen)
        except OSError:
            print('Port already in use... exiting', file=sys.stderr)
            exit(-1)
        print('Listening on 0.0.0.0:{}'.format(port_to_listen))

    def accept_connection(self):
        """
        Accepts a connection from a client and stores the socket
        :return: tuple with a socket and an ipAddress
        """
        (self.__client_socket, self.__client_address) = self.__server_socket.accept()

    @property
    def client_address(self):
        return self.__client_address

    def send(self, msg: bytes):
        """
        Sends to the client a message
        :param msg: message to send in bytes
        :return: void
        """
        total_sent = 0
        while total_sent < msg.__len__():
            sent = self.__client_socket.send(msg[total_sent:] + b'\n')
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent += sent
            print("Sent {} bytes".format(total_sent))

    def receive(self) -> str:
        """
        Waits until receives a message from the client
        :return: received message from client in string format
        """
        chunks = []
        bytes_recd = 0
        print("Waiting client response...")
        chunk = self.__client_socket.recv(min(self.MAXLEN - bytes_recd, 2048))
        if chunk == '':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_recd += len(chunk)
        print("Received {} bytes".format(bytes_recd))
        return b''.join(chunks).decode('utf-8')

    def close(self):
        """
        Closes the socket connection with a client
        :return: void
        """
        self.__client_socket.close()
        print('Connection with a client closed...')
        self.__client_socket = None

    def close_server(self):
        self.__server_socket.close()
        print('Server closed...')

    @staticmethod
    def codify(message: bytes, offset: int) -> bytes:
        """
        TODO Check this please!!!!!
        :param message:
        :param offset:
        :return:
        """
        codified = ''
        letter_number = 26
        offset %= letter_number
        for chars in message:
            current_char = chr(chars)
            if current_char.isalpha():
                if (current_char.islower() and chars + offset > ord('z')) or \
                        (current_char.isupper() and chars + offset > ord('Z')):
                    chars -= letter_number
                chars += offset
            codified += chr(chars)
        return ''.join(codified).encode()
