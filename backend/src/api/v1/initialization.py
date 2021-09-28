import paramiko
import time
from set_snmp import init_snmp_setting
from bson.json_util import dumps
from sanic.response import json
from sanic.views import HTTPMethodView

from repository import DeviceRepository

class InitializationView(HTTPMethodView):
    def get(self, request):
        device_repo = request.app.db['device']
        devices = device_repo.get_all()
        init_snmp_setting(devices)
        print('get device init')

        return json({"success": True, "message": "Initialization SNMP Success"})
    def post(self, request):
        device_repo = request.app.db['device']
        devices = device_repo.get_all()
        # init_snmp_setting(devices)
        # print('post device init')
        for device in devices:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(device['management_ip'], port=22, username=device['ssh_info']['username'], password=device['ssh_info']['password'])
            remote_connect = ssh.invoke_shell()
            output = remote_connect.recv(65535)
            if output.decode("utf-8")[-1] == ">":
                remote_connect.send("enable\n")
                time.sleep(0.5)
                remote_connect.send(device['ssh_info']['secret']+"\n")
                time.sleep(0.5)
            else:
                pass
            # set netflow
            interfaces = device_repo.get_interface(device['management_ip'])
            remote_connect.send('conf t\n')
            time.sleep(0.5)
            for interface in interfaces:
                for iface in interface['interfaces']:
                    if "ipv4_address" in iface:
                        for command in ['interface '+iface["description"]+'\n', 'ip policy route-map SDN-handmade\n', 'ip route-cache flow\n', 'exit\n']:
                            remote_connect.send(command)
                            time.sleep(0.5)
            ip = request.json['management_ip'] #ip management device
            port = '23456'
            for command in ['ip flow-export destination '+ip+' '+port+'\n', 'ip flow-export version 9\n', 'ip flow-cache timeout active 1\n', 'ip flow-cache timeout inactive 15\n', 'ip flow-export template refresh-rate 1\n']:
                remote_connect.send(command)
                time.sleep(0.5)

            ssh.close()

        return json({"success": True, "message": "Initialization Net_Flow Success"})    
