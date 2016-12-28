import socket

class Proxerver:
    host = ''
    port = 0
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,port,host):
        self.port = port
        self.host = host

    @classmethod
    def start(self):
        self.soc.bind((self.host,self.port))
        self.soc.listen(5)

        conn, addr = self.soc.accept()
        print("works")

        while 1:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
        conn.close()
