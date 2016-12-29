import socket,sys
from thread import *
__port__ = 10005

    #conn.send("HTTP/1.1 200 OK\nDate: Wed, 11 Apr 2012 21:29:04 GMT\nServer: Python/6.6.6 (custom)\nContent-Type: text/html\n\n<body>ERROR</body>")
    #conn.close()



  #Client Properties
    #WebServer Properties
#conn.send("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n" +"\n" # Important! +"<html><body>Hello World</body></html>\n")
def prepper_web_request(conn,data,addr):
    temp = data.split()
    print(temp)
    if temp[0] == 'CONNECT':
        print "CONNECT request"
        webaddress = (temp[1].split(':'))[0]
        webport = (temp[1].split(':'))[1]
        send_web_request(webaddress,webport)
        conn.send("HTTP/1.1 200 Connection established\nProxy-agent: Python Proxy/0.1.0 Draft 1\n\n")

    if temp[0] == 'GET':
        conn.send("HTTP/1.1 200 OK\n"+"Content-Type: text/html\n" +"\n" +"<html><body><h1>It works!</h1></body></html>\n")

    print(data)
    conn.close()

def receive_client_request(host,port):
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind((host,port))
        soc.listen(5)
    except Exception,e:
        print "> Error "
        sys.exit(1)
    while 1:
        try:
            conn,addr = soc.accept()
            print("> Works")
            data = conn.recv(1024)
            start_new_thread(prepper_web_request,(conn,data,addr))
        except KeyboardInterrupt:
            soc.close()
            print "> Stopping"
            sys.exit(1)


def send_web_request():
    print "todo"


def main():
    receive_client_request('',__port__)


if __name__ == "__main__":
    main()


