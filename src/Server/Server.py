import socket
import sys
import re


class Server(object):
    """
    Server abstraction class to handle connections from clients, and send them messages, receive messages from them and
    codify strings with the Caesar cypher method.
    """
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
            self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Fixes a bug in unix platforms
            self.__server_socket.bind(('0.0.0.0', port_to_listen))              
            self.__server_socket.listen(port_to_listen)
        except OSError:
            print('Port already in use... exiting', file=sys.stderr)
            exit(-1)
        print('Listening on 0.0.0.0:{}'.format(port_to_listen))

    def accept_connection(self):
        """
        Accepts a connection from a client and stores the socket and client address. Sets timeout to 40 secs.
        :return: void
        """
        (self.__client_socket, self.__client_address) = self.__server_socket.accept()
        self.__client_socket.settimeout(40)
        self.__client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    @property
    def client_address(self):
        return self.__client_address

    def send(self, msg: bytes):
        """
        Sends to the client a message in bytes
        :param msg: message to send in bytes
        :return: void
        """
        total_sent = 0
        while total_sent < msg.__len__():
            sent = self.__client_socket.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent += sent
            print("Sent {} bytes".format(total_sent))

    def receive(self) -> str:
        """
        Waits until receives a message from the client in bytes
        :return: received message from client in string format
        """
        chunks = []
        bytes_recd = 0
        print("Waiting client response...")
        chunk = None
        while chunk != b'\n':
            chunk = self.__client_socket.recv(1)
            if chunk == '':
                raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        if chunks[-1] == b'\r':
            chunks = chunks[:-1]
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
        """
        Closes server socket
        :return: void
        """
        self.__server_socket.close()
        print('Server closed...')

    @staticmethod
    def codify(message: bytes, offset: int) -> bytes:
        """
        Codifies a string with Caesar cypher method
        :param message: message to codify
        :param offset: offset from the Cesar codification
        :return: the codified text in bytes
        """
        codified = ''
        letter_number = 26
        offset %= letter_number
        for chars in message.decode():
            if re.match(r'[a-zA-Z]', chars) is not None:
                current_byte = ord(chars)
                if(chars.islower() and current_byte + offset > ord('z')) or \
                        (chars.isupper() and current_byte + offset > ord('Z')):
                    current_byte -= letter_number
                current_byte += offset
                codified += chr(current_byte)
            else:
                codified += chars
        if codified[-1] == '\n':
            codified = codified[:-1]
        return ''.join(codified).encode()
