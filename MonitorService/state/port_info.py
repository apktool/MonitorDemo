import socket


class socket_info(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def get_port_info(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.ip, self.port))

        return result


if __name__ == '__main__':
    socket_info = socket_info('192.168.100.66', 8080)
    result = socket_info.get_port_info()
    if result == 0:
        print("Port is open")
    else:
        print("Port is not open")
