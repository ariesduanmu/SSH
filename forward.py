import argparse
import os
import socket
import paramiko
import sys
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer
class ForwardServer(socketServer.ThreadingTCPServer):
	daemon_threads = True
	allow_reuse_address = True
class Handler (SocketServer.BaseRequestHandler):
	def handle(self):
		chan = self.ssh_transport.open_channel('direct-tcpip',
                                               (self.chain_host, self.chain_port),
                                               self.request.getpeername())
		while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)
        peername = self.request.getpeername()
        chan.close()
        self.request.close()



def forward_tunnel(local_port, remote_host, remote_port, transport):
	class SubHandler(Handler):
		chain_host = remote_host
		chain_port = remote_port
		ssh_transport = transport

	ForwardServer(('', local_port), SubHander).serve_forever()

def parse_options():
	pass
if __name__ == '__main__':
	server_host = sys.argv[1]
	server_port = int(sys.argv[2])
	remote_host = sys.argv[3]
	remote_port = int(sys.argv[4])
	username = sys.argv[5]
	keyfile = sys.argv[6]
	password = sys.argv[7]
	port = int(sys.argv[8])


	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.WarningPolicy())
	print('Connecting to ssh host %s:%d' % (server_host, server_port))
	client.connect(server_host, server_port, username = username, key_file = keyfile,
		           password = password)
	forward_tunnel(port, remote_host, remote_port, client.get_transport())



