import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback

import paramiko
from paramiko.py3compat import b, u, decodebytes


host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server (paramiko.ServerInterface):

    def check_channel_request(self, kind, channelid):
    	if kind == "session":
    		return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, u, p):
        if(u =='robit' and p=='human'):
            return paramiko.AUTH_SUCCESSFUL
        return paramike.AUTH_FAILED

host = sys.argv[1]
port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
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

