import paramiko
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
devices = client.sdn01.device.find() #client.(database).(collection).find()

def sleep():
    while(remote_connect.recv(65535).decode("utf-8")[-1] not in "#> "):
        print(remote_connect.recv(65535).decode("utf-8"))
        print(remote_connect.recv(65535).decode("utf-8")[-1] not in "#> ")
        time.sleep(0.5)

for device in devices:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device['management_ip'], port=22, username=device['ssh_info']['username'], password=device['ssh_info']['password'])
    remote_connect = ssh.invoke_shell()
    output = remote_connect.recv(65535)
    print(output.decode("utf-8"))
    print("connect to "+device['management_ip'], end=" ")
    if output.decode("utf-8")[-1] == "#":
        print("Privileged mode")
    elif output.decode("utf-8")[-1] == ">":
        print("User mode")
        remote_connect.send("enable\n")
        time.sleep(0.5)
        remote_connect.send(input()+"\n")
        time.sleep(0.5)
    else:
        pass
    # set netflow
    interfaces = client.sdn01.device.find({'management_ip': device['management_ip']}, {'_id':0, 'interfaces': 1})
    remote_connect.send('conf t\n')
    time.sleep(0.5)
    for interface in interfaces:
        for iface in interface['interfaces']:
            if "ipv4_address" in iface:
                for command in ['interface '+iface["description"]+'\n', 'ip policy route-map SDN-handmade\n', 'ip route-cache flow\n', 'exit\n']:
                    print(command)
                    remote_connect.send(command)
                    time.sleep(0.5)
                    #print(remote_connect.recv(10000))
    ip = '10.30.7.40' #ip management device
    port = '23456'
    for command in ['ip flow-export destination '+ip+' '+port+'\n', 'ip flow-export version 9\n', 'ip flow-cache timeout active 1\n', 'ip flow-cache timeout inactive 15\n', 'ip flow-export template refresh-rate 1\n']:
        remote_connect.send(command)
        time.sleep(0.5)
    ssh.close()
