import paramiko
import time
from pymongo import MongoClient
from threading import Thread

client = MongoClient('localhost', 27017)
# devices = client.sdn01.device.find() #client.(database).(collection).find()

class set_snmp_worker(Thread):
    def run(self, device):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device['management_ip'], port=22, username=device['ssh_info']['username'], password=device['ssh_info']['password'])
        remote_connect = ssh.invoke_shell()
        output = remote_connect.recv(65535)
        print("connect to "+device['management_ip'], end=" ")
        if output.decode("utf-8")[-1] == "#":
            print("Privileged mode")
        elif output.decode("utf-8")[-1] == ">":
            print("User mode")
            remote_connect.send("enable\n")
            time.sleep(0.5)
            remote_connect.send(device['ssh_info']['secret']+"\n")
            time.sleep(0.5)
        else:
            pass
        # set snmp
        snmp_commands = ['conf t\n', 'snmp-server enable traps\n', 'snmp-server community public RO\n', 'snmp-server community private RW\n']
        for command in snmp_commands:
            remote_connect.send(command)
            time.sleep(0.5)
        
        ssh.close()


def sleep(device_connection):
    while(device_connection.recv(65535).decode("utf-8")[-1] not in "#>"):
        time.sleep(0.1)


def init_snmp_setting(devices):
    for device in devices:
        set_snmp_worker().run(device)
