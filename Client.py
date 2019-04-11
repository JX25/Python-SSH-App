import getpass
import os
import paramiko
from paramiko import SSHClient


class Client:
    client = ""
    stdin = ""
    stdout = ""
    stderr = ""

    def __init__(self):
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # passw = getpass.getpass()
    def connection(self, config):
        try:
            passw = "ubuntu"
            self.client.connect(config.address, port=config.port, username=config.username, password=passw)
        except Exception as error:
            print('ERROR', error)
            exit(1)

    def close(self):
        self.client.close()
