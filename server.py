import base64
from binascii import hexlify
import os
import socket
import sys
import getopt
import threading
import traceback

import paramiko
from paramiko.py3compat import b, u, decodebytes

paramiko.util.log_to_file('server.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')
public_key_data = (b'AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp'
                   b'fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC'
                   b'KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT'
                   b'UWT10hcuO4Ks8=')
public_key = paramiko.RSAKey(data = decodebytes(public_key_data))
username = password = ""
port = 22


class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, channelid):
    	if kind == "session":
    		return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, u, p):
        if(u == username and p == password):
            return paramiko.AUTH_SUCCESSFUL
        return paramike.AUTH_FAILED
    def check_auth_publickey(self, username, key):
        if(username == username) and (key == public_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


def ssh_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("localhost", port))
        sock.listen(5)
        print "[+] Listening for connection..."
        client, addr = sock.accept()
    except Exception,e:
        print "[-] Listen failed: " + str(e)
        sys.exit(1)
    print "[+] Got a connection"

    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()
        try:
            bhSession.start_server(server = server)
        except paramiko.SSHException, x:
            print "[-] SSH negotiation failed"
        chan = bhSession.accept(20)
        print "[+] Authenticated"
        print chan.recv(1024)
        chan.send('Welcome to the SSH')
    except Exception, e:
        print "[-] Caught exception: " + str(e)
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)

def usage():
    print "SSH Paramiko based SSH tool @Ludisposed & @Qin"
    print ""
    print "Usage: server.py -u username -m password"
    print "-u --username                 - username use to auth"
    print "-m --magic                    - password use to auth"
    print ""
    print "Optionals"
    print "-p --port                     - port use for ssh server, default is 22"
    print ""
    print "Examples: "
    print "python2.7 server.py -u username -m password"
    print "python2.7 server.py -p port -u username -m password"

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        usage()
    else:
        try:
            ops, args = getopt.getopt(sys.argv[1:], "p:u:m:", ["port=","username=","magic="])
        except getopt.GetoptError as err:
            print str(err)
            usage()

        for o,a in ops:
            if o in ('-p','--port'):
                port = int(a)
            elif o in ('-u','--username'):
                username = a
            elif o in ('-m','--magic'):
                password = a

        if len(username) > 0 and len(password) > 0:
           ssh_server() 
        else:
            usage()
    


