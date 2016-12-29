import socket, sys, select
from thread import *
__port__ = 10015
max_buff_size = 8192
time_out_max = 100

# conn.send("HTTP/1.1 200 OK\nDate: Wed, 11 Apr 2012 21:29:04 GMT\nServer:
# Python/6.6.6 (custom)\nContent-Type: text/html\n\n<body>ERROR</body>")
# conn.close()

# Client Properties
# WebServer Properties
# conn.send("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n"
# +"\n" # Important! +"<html><body>Hello World</body></html>\n")


def receive_server_request(data):
    try:
        temp = data.split()
        proxy_server_socket = None
        print(temp)
        if temp[0] == 'CONNECT':
            print "CONNECT request"
            webaddress = (temp[1].split(':'))[0]
            webport = (temp[1].split(':'))[1]
            proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            proxy_server_socket.connect((webaddress, int(webport)))
            print "> Connection with web server established!"

        if temp[0] == 'GET':
            #conn.send("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n" +"\n" +"<html><body><h1>It works!</h1></body></html>\n")
            print "GET req"
        print(data)
        return proxy_server_socket
    except Exception,e:
        print "Error parsing client request."


def client_receiver(host, port):
    try:
        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_client_socket.bind((host, port))
        proxy_client_socket.listen(5)

    except Exception, e:
        print "> Error"
        sys.exit(1)
    while 1:
        try:
            conn, addr = proxy_client_socket.accept()
            print "New client has been created"
            data = conn.recv(1024)
            server = receive_server_request(data)
            if server is None:
                start_new_thread(http_bridge, (conn, server))
            else:
                start_new_thread(https_bridge, (conn,server ))
        except KeyboardInterrupt:
            proxy_client_socket.close()
            print "> Stopping"
            sys.exit(1)


def send_web_request(webaddress, webport, proxy_client_socket):
    print "> Web server address: "+webaddress + " : " + webport
    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server_socket.connect((webaddress, int(webport)))
    print "> Connection with web server established!"
    proxy_client_socket.send("HTTP/1.1 200 Connection established\nProxy-agent: Python Proxy/0.1.0 Draft 1\n\n")


    #while 1:
     #   print "> Client to server:"

      #  data_to_server = proxy_client_socket.recv(max_buff_size)
       # if len(data_to_server) > 0:
        #    print "> Data from client to server" + data_to_server + " END"
         #   proxy_server_socket.send(data_to_server)
        #else:
         #   print ">Empty data"
         #   break

      #  print "> Server to client"

       # data_to_client = proxy_server_socket.recv(max_buff_size)
        #if len(data_to_server) > 0:
         #   print "> Data from server to client" + data_to_server + " END"
          #  proxy_client_socket.send(data_to_client)
        #else:
          #  print ">Empty data"
         #   break
    #print "FINISHED"
    #proxy_client_socket.send(data_to_client)

# The method that every programmer should call.
def http_bridge(proxy_client_socket, proxy_server_socket):
    proxy_client_socket.send("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n" +"\n" +"<html><body><h1>It works!</h1></body></html>\n")


def https_bridge(proxy_client_socket, proxy_server_socket):
    proxy_client_socket.send("HTTP/1.1 200 Connection established\nProxy-agent: Python Proxy/0.1.0 Draft 1\n\n")
    sockets = [proxy_server_socket, proxy_client_socket]
    num_of_chats = 0
    while 1:
        num_of_chats += 1
        (recv, outready, err) = select.select(sockets, [], [3])

        if err:
            break
        if recv:
            for receiver in recv:
                data = receiver.recv(max_buff_size)
                if receiver is proxy_client_socket:
                    print "Client turn"
                    transmitter = proxy_server_socket
                else:
                    print "Server turn"
                    transmitter = proxy_client_socket
                if data:
                    transmitter.send(data)
                    print "> Data START: "+ data+ " :END"
                    num_of_chats = 0
        if num_of_chats == time_out_max:
            break


def main():
    client_receiver('',__port__)

if __name__ == "__main__":
    main()


