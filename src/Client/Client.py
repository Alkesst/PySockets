"""
    Client abstraction
"""
import ipaddress


class Client(object):

    def __init__(self, ip_address: ipaddress):
        self.__ip_address = ip_address