import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback

import paramiko
from paramiko.py3compat import b, u, decodebytes


# setup logging
paramiko.util.log_to_file('demo_server.log')

if not os.path.isfile('test_rsa.key'):
    print 'Create or get from paramiko repo the test_rsa.key'
    sys.exit(1)
    
host_key = paramiko.RSAKey(filename='test_rsa.key')
print('Read key: ' + u(hexlify(host_key.get_fingerprint())))

class Server (paramiko.ServerInterface):
    print 'Serverstuff ;)'
