import paramiko
import sys
import getopt
import os
import socket

paramiko.util.log_to_file('client.log')

key_filename = ''
username = password = ""
host = ""
port = 22



def ssh_client():
	
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
		if len(key_filename) == 0:
			client.connect(host,port,username,password)
		else:
			key = paramiko.RSAKey.from_private_key_file(key_filename)
			client.connect(host,port,username,pkey = key_filename)
		ssh_session = client.get_transport().open_session()
		if ssh_session.active:
		    ssh_session.send('ClientConnected')
		    print ssh_session.recv(1024)

	except Exception as e:
		print str(e)
		sys.exit(1)
	'''
	
def usage():
    print "SSH Paramiko based SSH tool @Ludisposed & @Qin"
    print ""
    print "Usage: client.py username@host"
    print ""
    print "Optionals"
    print "-p --port                 - port use to connect, default is 22"
    print "-i                        - server pub key's filename"
    print ""
    print "Examples: "
    print "python2.7 client.py username@host"
    print "python2.7 client.py username@host -p port"
    print "python2.7 client.py username@host -p port -i filename"

if __name__ == "__main__":
    if not len(sys.argv[1]):
        usage()
    else:
        try:
            username, host = sys.argv[1].split('@')
        except Exception as e:
            print str(e)
            usage()
    if len(sys.argv[2:]) > 0:
        try:
            ops, args = getopt.getopt(sys.argv[2:], "p:i:", ["port="])
        except getopt.GetoptError as err:
            print str(err)
            usage()

        for o,a in ops:
            if o in ('-p','--port'):
                port = int(a)
            elif o in ('-i'):
            	filename = a
    
    if len(filename) == 0:
    	password = raw_input('Password: ')
    
    ssh_client() 
    