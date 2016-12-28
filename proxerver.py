import socket
class Proxerver:
    host = ''
    port = '0000'
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self,port,host):
        self.port = port
        self.host = host
    def __init__(self):
        print "default settings"

    def start():
        socket.bind((host,port))
        socket.listen(1)

        conn, addr = s.accept()

        while 1:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
        conn.close()
