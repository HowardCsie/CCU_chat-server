#!/usr/bin python3
""" A simple chat TCP server """
import socket
import select
import time

def broadcast_data(message):
    for sock in CONNECTION_LIST:
        if sock != SERVER_SOCKET:
            try:
                sock.sendall(message) # send all data at once
            except Exception as msg: # Connection was closed. Errors
                print(type(msg).__name__)
                sock.close()
                try:
                    CONNECTION_LIST.remove(sock)
                except ValueError as msg:
                    print("{}:{}".format(type(msg).__name__, msg))
def isOnline(person):
    for connection in CONNECTION_PORT_LIST:
        if connection.split(' ', 1 )[0] == person:
            return 1
    return 0
def isUser(person):
    for user in ACCOUNT_LIST:
        if user.split(' ', 1 )[0] == person:
            return 1
    return 0
def isFriend(myName, person):
    for friend in FRIEND_LIST:
        if friend.split(' ', 1 )[0] == myName:
            if friend.split(' ', 1 )[1] == person:
                return 1
    return 0
def isTalking(person):
    for talk in TALK_LIST:
        if talk.split(' ', 1 )[0] == person:
            return 1
    return 0
def isAskingFile(person):
    for element in FILE_REQUEST_LIST:
        if element.split(' ', 2 )[0] == person:
            return 1
        elif element.split(' ', 2 )[1] == person:
            return 2
    return 0
def bothTalking(person):
    for talk in TALK_LIST:
        if talk.split(' ', 1 )[0] == person:
            for talk2 in TALK_LIST:
                if talk2.split(' ', 1 )[0] == talk.split(' ', 1 )[1] and talk2.split(' ', 1 )[1] == person:
                    return 1
    return 0
def getTalkingTo(person):
    for talk in TALK_LIST:
        if talk.split(' ', 1 )[0] == person:
            return talk.split(' ', 1 )[1]
    return ""
def getSendingFileFrom(person):
    for element in FILE_REQUEST_LIST:
        if element.split(' ', 2 )[1] == person:
            return element.split(' ', 2 )[0]
    return ""
def getUserName(port):
    for connection in CONNECTION_PORT_LIST:
        if connection.split(' ', 1 )[1] == port:
            return connection.split(' ', 1 )[0]
    return ""
def getPort(user):
    for connection in CONNECTION_PORT_LIST:
        if connection.split(' ', 1 )[0] == user:
            return connection.split(' ', 1 )[1]
    return ""
def getIP(port):
    for connection in CONNECTION_LIST:
        if sock != SERVER_SOCKET:
            a = sock.getpeername()
            if "{}".format(a[1]) == "{}".format(port):
                return "{}".format(a[0])
    return ""
def getFileName(sender, reciever):
    for request in FILE_REQUEST_LIST:
        if request.split(' ',2)[0] == sender and request.split(' ',2)[1] == reciever:
            return "{}".format(request.split(' ',2)[2])
    return ""


CONNECTION_LIST = []
RECV_BUFFER = 4096 
PORT = 1340

ACCOUNT_LIST = []
CONNECTION_PORT_LIST = []
FRIEND_LIST = []
TALK_LIST = []
FILE_REQUEST_LIST = []
# FRIEND_LIST.append(('howard kila'))
FRIEND_LIST.append(('howard popo'))
FRIEND_LIST.append(('howard su'))
FRIEND_LIST.append(('kila su'))
FRIEND_LIST.append(('popo kila'))
FRIEND_LIST.append(('howard kila'))
FRIEND_LIST.append(('kila howard'))
ACCOUNT_LIST.append('howard kk')
ACCOUNT_LIST.append('kila qq')
ACCOUNT_LIST.append('popo pp')
ACCOUNT_LIST.append('su gg')

MESSAGE_LIST = []

SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM -> tcp
SERVER_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER_SOCKET.bind(("", PORT))

print("Listening...")
SERVER_SOCKET.listen(10) # 10 connections

CONNECTION_LIST.append(SERVER_SOCKET)
print("Server started!")

while True:
    READ_SOCKETS, WRITE_SOCKETS, ERROR_SOCKETS = select.select(CONNECTION_LIST, [], [])
    for SOCK in READ_SOCKETS:
        if SOCK == SERVER_SOCKET:
            SOCKFD, ADDR = SERVER_SOCKET.accept()
            CONNECTION_LIST.append(SOCKFD)
            print("\rClient ({0}, {1}) connected".format(ADDR[0], ADDR[1]))
        else:
            try:
                DATA = SOCK.recv(RECV_BUFFER)
                if DATA:
                    ADDR = SOCK.getpeername()
                    user = getUserName("{}".format(ADDR[1]))
                    if isTalking(user) == 0 and isAskingFile(user) == 0:
                        if DATA.decode().split(' ', 1 )[0] == 'login':
                            i = 0
                            for account in ACCOUNT_LIST:
                                if account == DATA.decode().split(' ', 1 )[1]:
                                    CONNECTION_PORT_LIST.append("{} {}".format(DATA.decode().split(' ', 2 )[1], ADDR[1]))
                                    i = 1
                                    print "{} login".format(DATA.decode().split(' ', 2 )[1])
                                    break
                            if i == 0:
                                SOCK.sendall("login fail")
                            elif i == 1:
                                result = "success "
                                for message in MESSAGE_LIST:
                                    if message.split(' ', 2 )[1] == "{}".format(DATA.decode().split(' ', 2 )[1]):
                                        result += "Message from {}:{}\n".format(message.split(' ', 2 )[0],message.split(' ', 2 )[2])
                                        
                                NEW_MESSAGE_LIST = []
                                for message in MESSAGE_LIST:
                                    if message.split(' ', 2 )[1] != "{}".format(DATA.decode().split(' ', 2 )[1]):
                                        NEW_MESSAGE_LIST.append(message)
                                MESSAGE_LIST = NEW_MESSAGE_LIST
                                SOCK.sendall(result)   
                        elif DATA.decode().split(' ', 3 )[0] == 'friend':
                            if DATA.decode().split(' ', 3 )[1] == 'list' and len(DATA.decode().split(' ', 3 )) == 2:
                                result = ""
                                for friendRelation in FRIEND_LIST:
                                    if friendRelation.split(' ', 1)[0] == user:
                                        if (isOnline(friendRelation.split(' ', 1)[1]) == 1):
                                            result += "{} online\n".format(friendRelation.split(' ', 1)[1])
                                        else:
                                            result += "{} offline\n".format(friendRelation.split(' ', 1)[1])
                                SOCK.sendall(result)
                            elif DATA.decode().split(' ', 3 )[1] == 'add' and len(DATA.decode().split(' ', 3 )) == 3:
                                if isUser(DATA.decode().split(' ', 3)[2]) == 1:
                                    FRIEND_LIST.append("{} {}".format(user, DATA.decode().split(' ', 3)[2]))
                                    SOCK.sendall("{} added into friend list\n".format(DATA.decode().split(' ', 3)[2]))
                                else:
                                    SOCK.sendall("user {} not exists\n".format(DATA.decode().split(' ', 3)[2]))
                            elif DATA.decode().split(' ', 3 )[1] == 'rm' and len(DATA.decode().split(' ', 3 )) == 3:
                                if isUser(DATA.decode().split(' ', 3)[2]) == 0:
                                    SOCK.sendall("user {} not exists\n".format(DATA.decode().split(' ', 3)[2]))
                                elif isFriend(user ,DATA.decode().split(' ', 3)[2]) == 0:
                                    SOCK.sendall("user {} is not your friend\n".format(DATA.decode().split(' ', 3)[2]))
                                else:
                                    FRIEND_LIST.remove("{} {}".format(user, DATA.decode().split(' ', 3)[2]))
                                    SOCK.sendall("{} removed from the friend list\n".format(DATA.decode().split(' ', 3)[2]))
                            else:
                                SOCK.sendall("unknown friend command")
                        elif DATA.decode().split(' ', 2 )[0] == 'send':
                            if len(DATA.decode().split(' ', 2 )) == 3:
                                if isUser(DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} not exists\n".format(DATA.decode().split(' ', 2)[1]))
                                elif isFriend(user ,DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} is not your friend\n".format(DATA.decode().split(' ', 2)[1]))
                                else:
                                    MESSAGE_LIST.append("{} {} {}".format(user,DATA.decode().split(' ', 2)[1],DATA.decode().split(' ', 2)[2]))
                                    SOCK.sendall("Message has been sent to your friend {}\n".format(DATA.decode().split(' ', 2)[1]))

                            else:
                                SOCK.sendall("unknown send command")
                        elif DATA.decode().split(' ', 1 )[0] == 'talk':
                            if len(DATA.decode().split(' ', 2 )) == 2:
                                if isUser(DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} not exists\n".format(DATA.decode().split(' ', 2)[1]))
                                elif isFriend(user ,DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} is not your friend\n".format(DATA.decode().split(' ', 2)[1]))
                                elif isOnline(DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} is not online\n".format(DATA.decode().split(' ', 2)[1]))
                                else:
                                    TALK_LIST.append("{} {}".format(user, DATA.decode().split(' ', 2)[1]))
                                    port = getPort(DATA.decode().split(' ', 2)[1])
                                    for sock in CONNECTION_LIST:
                                        if sock != SERVER_SOCKET:
                                            a = sock.getpeername()
                                            if "{}".format(a[1]) == "{}".format(port):
                                                sock.sendall("{} wants to talk to you".format(user))

                            else:
                                SOCK.sendall("unknown talk command")
                        elif DATA.decode().split(' ', 1 )[0] == 'sendfile':
                            if len(DATA.decode().split(' ', 3 )) == 3:
                                if isUser(DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} not exists\n".format(DATA.decode().split(' ', 2)[1]))
                                elif isFriend(user ,DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} is not your friend\n".format(DATA.decode().split(' ', 2)[1]))
                                elif isOnline(DATA.decode().split(' ', 2)[1]) == 0:
                                    SOCK.sendall("user {} is not online\n".format(DATA.decode().split(' ', 2)[1]))
                                else:
                                    FILE_REQUEST_LIST.append("{} {} {}".format(user, DATA.decode().split(' ', 2)[1], DATA.decode().split(' ', 2)[2]))
                                    port = getPort(DATA.decode().split(' ', 2)[1])
                                    for sock in CONNECTION_LIST:
                                        if sock != SERVER_SOCKET:
                                            a = sock.getpeername()
                                            if "{}".format(a[1]) == "{}".format(port):
                                                sock.sendall("{} wants to send file to you,agree?(y/n)".format(user))
                            else:
                                SOCK.sendall("unknown sendfile command")
                        elif DATA.decode().split(' ', 1 )[0] == 'broadcast':
                            broadcast_data("{}:{}".format(user,DATA.decode().split(' ', 1 )[1]))
                        elif DATA.decode().split(' ', 1 )[0] == 'exit':
                            for connection in CONNECTION_PORT_LIST:
                                if connection.split(' ', 1 )[1] == "{}".format(ADDR[1]):
                                    print "{} logout".format(connection.split(' ', 1 )[0])
                                    SOCK.sendall("exit")
                                    CONNECTION_PORT_LIST.remove(connection)
                                    CONNECTION_LIST.remove(SOCK)
                        else:
                            SOCK.sendall("unknown command")
                            print DATA.decode().split(' ', 1 )[0]
                    elif isAskingFile(user) == 1:
                        SOCK.sendall("wait for reply")
                    elif isAskingFile(user) == 2:
                        if DATA.decode().split(' ', 1 )[0] == 'yes' or DATA.decode().split(' ', 1 )[0] == 'y':
                            SOCK.sendall("sendfile {}".format(getFileName(getSendingFileFrom(user), user)))
                            port = getPort(getSendingFileFrom(user))
                            for sock in CONNECTION_LIST:
                                if sock != SERVER_SOCKET:
                                    a = sock.getpeername()
                                    if "{}".format(a[1]) == "{}".format(port):
                                        time.sleep(1)
                                        sock.sendall("accepted from {} {} {}".format(user, ADDR[0],getFileName(getSendingFileFrom(user), user)))
                            for request in FILE_REQUEST_LIST:
                                if request.split(' ',2)[0] == getSendingFileFrom(user) and request.split(' ',2)[1] == user:
                                    FILE_REQUEST_LIST.remove(request)
                        elif DATA.decode().split(' ', 1 )[0] == 'no' or DATA.decode().split(' ', 1 )[0] == 'n':
                            port = getPort(getSendingFileFrom(user))
                            for sock in CONNECTION_LIST:
                                if sock != SERVER_SOCKET:
                                    a = sock.getpeername()
                                    if "{}".format(a[1]) == "{}".format(port):
                                        sock.sendall("denied from {}".format(user))
                            for request in FILE_REQUEST_LIST:
                                if request.split(' ',2)[0] == getSendingFileFrom(user) and request.split(' ',2)[1] == user:
                                    FILE_REQUEST_LIST.remove(request)
                        else:
                            SOCK.sendall("reply yes or no (y/n)")

                    else:
                        if DATA.decode().split(' ', 1 )[0] == 'end' and DATA.decode().split(' ', 1 )[1] == 'talk' and len(DATA.decode().split(' ', 2)) == 2:
                            if bothTalking(user):
                                port = getPort(getTalkingTo(user))
                                for sock in CONNECTION_LIST:
                                    if sock != SERVER_SOCKET:
                                        a = sock.getpeername()
                                        if "{}".format(a[1]) == "{}".format(port):
                                            sock.sendall("end talk")
                            talker = getTalkingTo(user)
                            TALK_LIST.remove("{} {}".format(user, talker))
                            TALK_LIST.remove("{} {}".format(talker, user))
                        else:
                            if bothTalking(user):
                                port = getPort(getTalkingTo(user))
                                for sock in CONNECTION_LIST:
                                    if sock != SERVER_SOCKET:
                                        a = sock.getpeername()
                                        if "{}".format(a[1]) == "{}".format(port):
                                            sock.sendall("{}:{}".format(user,DATA))
            except Exception as msg:
                print(type(msg).__name__, msg)
                print("\rClient ({0}, {1}) disconnected.".format(ADDR[0], ADDR[1]))
                SOCK.close()
                try:
                    CONNECTION_LIST.remove(SOCK)
                except ValueError as msg:
                    print("{}:{}.".format(type(msg).__name__, msg))
                continue

SERVER_SOCKET.close()
