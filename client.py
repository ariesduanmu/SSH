import paramiko
import sys

host = sys.argv[1]
port = int(sys.argv[2])

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
client.connect(host,port,'robit','human')
ssh_session = client.get_transport().open_session()
if ssh_session.active:
    ssh_session.send('ClientConnected')
    print ssh_session.recv(1024)