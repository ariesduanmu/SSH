# -*- coding: utf-8 -*-
import threading
import paramiko
import subprocess

'''
What I need:
in windows, each time need type `powershell` and `ssh user@host` to connect to server
and more lots duplicated cmd all the time
but I don't wanna use alias in server

also I wish I can communicate with ssh using this script
'''
def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print("ssh_session.recv(1024)")
        client.close()

if __name__ == "__main__":
    ssh_command("localhost", "mody", "rick", "id")