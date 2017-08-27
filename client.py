import paramiko
import sys
import getopt
import os
import socket
import argparse

paramiko.util.log_to_file('client.log')


def ssh_client(username, host, port, keyfile, password):
	
	'''
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host,port))
	except Exception as e:
		print('[-] Connect failed: ' + str(e))
		sys.exit(1)
	try:
		t = paramiko.Transport(sock)
		try:
			t.start_client()
		except paramiko.SSHException:
			print "[-] SSH negotiation failed"
			sys.exit(1)

		try:
			keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
		except IOError:
			try:
				keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
			except IOError:
				print '[-] Unable to open host keys file'
				keys = {}

		key = t.get_remote_server_key()
		if host not in keys:
			print '[*] WARNING: Unknown host key!'
		elif key.get_name() not in keys[host]:
			print '[*] WARNING: Unknown host key!'
		elif keys[host][key.get_name()] != key:
			print '[*] WARNING: Host key has changed!!!'
			sys.exit(1)
		else:
			print('[+] Host key OK.')

		if len(password) > 0:
			t.auth_password(username,password)
		elif len(key_filename) > 0:
			try:
				key = paramiko.RSAKey.from_private_key_file(key_filename)
			except paramiko.PasswordRequiredException:
				magic = getpass.getpass('RSA key password: ')
				key = paramiko.RSAKey.from_private_key_file(path, magic)
			t.auth_publickey(username, key)
		if not t.is_authenticated():
			print('[-] Authentication failed. :(')
			t.close()
			sys.exit(1)

		chan = t.open_session()
		chan.get_pty()
		chan.invoke_shell()
		print '[+] Here we go!\n'
		interactive.interactive_shell(chan)
		chan.close()
		t.close()

	except Exception as e:
	    print '[+] Caught exception: ' + str(e.__class__) + ': ' + str(e)
	    
	    try:
	        t.close()
	    except:
	        pass
	    sys.exit(1)
	'''

	
	try:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		if keyfile == None or len(keyfile) == 0:
			client.connect(host,port,username,password)
		else:
			key = paramiko.RSAKey.from_private_key_file(keyfile)
			client.connect(host,port,username,pkey = keyfile)
		ssh_session = client.get_transport().open_session()
		if ssh_session.active:
		    ssh_session.send('ClientConnected')
		    print ssh_session.recv(1024)

	except Exception as e:
		print str(e)
		sys.exit(1)

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s <username>[@<host>] [-p port] [-i pubkey_path]',
                                     description='SSH is Paramiko based SSH tool @Ludisposed & @Qin',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=
'''
Examples:
python2.7 client.py username@host
python2.7 client.py username@host -p port
python2.7 client.py username@host -p port -i filename

'''
                                     )
    parser.add_argument('-i', dest='keyfile', type=str, help="server pub key's filename")
    parser.add_argument('-p','--port', type=int, default=22, help='port use to connect, default is 22')
    parser.add_argument('username_host',type=str,help='server username and host')
    args = parser.parse_args()

    return args	

if __name__ == "__main__":
	args = parse_options()
	username, host = args.username_host.split('@')
	password = ''
	if args.keyfile == None:
		password = raw_input('Password: ')
	ssh_client(username, host, args.port, args.keyfile, password)

    