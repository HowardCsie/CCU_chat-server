#!/usr/bin python3
""" TCP Client """

import socket
import select
import sys
import getpass

def server(filename):
    s = socket.socket()       
    host = socket.gethostname()
    port = 1234             
    s.bind((host, port))
    print "waiting for file..." 
    f = open(filename,'wb')
    s.listen(5)               
    while True:
        c, addr = s.accept()    
        print 'Got connection from', addr
        print "Receiving..."
        l = c.recv(4096)
        while (l):
            print "Receiving..."
            f.write(l)
            l = c.recv(4096)
        f.close()
        print "Done Receiving"
        c.close()
        s.close()
        break              
def client(filename, ip):
    print ip
    s = socket.socket()       
    host = socket.gethostname()        
    port = 1234            

    s.connect((host, port))
    f = open(filename,'rb')
    print 'Sending...'
    l = f.read(4096)
    while (l):
        print 'Sending...'
        s.send(l)
        l = f.read(4096)
    f.close()
    print "Done Sending"
    s.close                     # Close the socket when done

if len(sys.argv) < 3:
    print("Usage : python {0} hostname port".format(sys.argv[0]))
    sys.exit()

HOST = sys.argv[1]
PORT = 1340
User = sys.argv[2]

MASTER_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MASTER_SOCK.settimeout(200)


print "Login: %s" % User
passwd = getpass.getpass("Password: ")
# connect to remote host
try:
    MASTER_SOCK.connect((HOST, PORT))
    msg = "login " + User + " " + passwd.replace("\n", "")
    MASTER_SOCK.sendall(msg.encode())
except Exception as msg:
    print(type(msg).__name__)
    print("Unable to connect")
    sys.exit()


loginFlag = 0
while True:
    SOCKET_LIST = [sys.stdin, MASTER_SOCK]

    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])

    for sock in READ_SOCKETS: 
        if sock == MASTER_SOCK:
            data = sock.recv(4096)
            if not data:
                print('Disconnected from chat server')
                sys.exit()
            elif data.decode().split(' ', 1)[0] == "success": 
                print "---------------login success---------------"
                print data.decode().split(' ', 1)[1]
                loginFlag = 1
            else:
                print "login fail"
                sys.exit()
    if loginFlag == 1:
        break;


while True:
    SOCKET_LIST = [sys.stdin, MASTER_SOCK]
 
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(SOCKET_LIST, [], [])

    for sock in READ_SOCKETS: 
        if sock == MASTER_SOCK:
            data = sock.recv(4096)
            if not data:
                print('Disconnected from chat server')
                sys.exit()
            elif data.decode() == "exit":
                print('logout from chat server')
                sys.exit()
            else: 
                if data.decode().split(' ',1)[0] == 'sendfile':
                    print data.decode()
                    server(data.decode().split(' ',1)[1])
                elif data.decode().split(' ',2)[0] == 'accepted' and data.decode().split(' ',2)[1] == 'from':
                    print data.decode()
                    client(data.decode().split(' ',4)[4],data.decode().split(' ',4)[3])
                else:
                    print data.decode()
        else:
            msg = sys.stdin.readline().replace("\n", "")
            MASTER_SOCK.sendall(msg.encode())
