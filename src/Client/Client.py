"""
    Client abstraction
"""
import ipaddress
import socket
import time


class Client(object):

    def __init__(self, ip_address: bytes, port: int, sock: socket=None):
        """
        If sockets is none, creates a new socket object and stores the
        values of the server ip and port in class variables
        :param ip_address: Server ip to connect
        :param port: server port to connect
        :param sock: other socket already created. its default value is None
        """
        if sock is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.__socket = sock
        self.__ip_address = ip_address
        self.__port = port

    def connect(self):
        """
        Connects to the socket
        :return: void
        """
        self.__socket.connect((self.__ip_address, self.__port))
        print("Connected to {}:{}".format(self.__ip_address.decode('utf-8'), self.__port))

    def send(self, msg: bytes):
        """
        Sends to the server a message
        :param msg: message to send in bytes
        :return: void
        """
        total_sent = 0
        while total_sent < msg.__len__():
            sent = self.__socket.send(msg[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent += sent
        print("Sent {} bytes to {}:{}".format(total_sent, self.__ip_address.decode('utf-8'), self.__port))

    def receive(self) -> str:
        """
        Waits until receives a message from the server
        :return: received message from server in string format
        """
        chunks = []
        bytes_recd = 0
        print("Waiting server response...")
        chunk = self.__socket.recv(min(self.MAXLEN - bytes_recd, 2048))
        if chunk == '':
            raise RuntimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_recd += len(chunk)
        print("Received {} bytes".format(bytes_recd))
        return b''.join(chunks).decode('utf-8')
