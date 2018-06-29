from __future__ import print_function
from src.Client.Client import Client
import sys


def main():
    """
    Main app for the client.
    :return: void
    """
    try:
        host_ip = input("Enter the host ip: ").encode()
        port = int(input("Enter the port: "))
        client = Client(host_ip, port)
        client.connect()
        print(client.receive())
        cesar_offset = None
        while cesar_offset != b'0':
            cesar_offset = input("Enter the offset of the codification!: ").encode()
            if cesar_offset != b'0':
                codify_text = input('Enter the string to codify!: ').encode()
                client.send(cesar_offset + b'\r')
                client.send(codify_text)
                print(client.receive(), end='')
        client.send(b'0')
        print(client.receive())
        client.close()
    except ConnectionResetError:
        print('Connection timeout with the server... Closing client.', file=sys.stderr)
        exit(-1)


if __name__ == '__main__':
    main()
