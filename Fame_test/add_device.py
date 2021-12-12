"""Adding device by calling API"""

from pymongo import MongoClient
import requests


controller_ip = '10.50.34.15'

device_list = ['192.168.1.1', '192.168.1.2', '192.168.7.17', '192.168.7.18', '192.168.7.49', '192.168.3.1', '192.168.4.2']

def add_device():
    for device in device_list:
        print("adding device", device)
        payload = {
            'management_ip': device,
            'type': 'cisco_ios',
            'ssh_info':{
                'username':'cisco',
                'password':'cisco',
                'port':22,
                'secret':'cisco'
            },
            'snmp_info':{
                'version':'2c',
                'community':'public',
                'port':161
            }
        }
        requests.post("http://" + controller_ip +  ":5001/api/v1/device", json=payload)

def remove_all_device():
    device_list = requests.get("http://" + controller_ip + ":5001/api/v1/device").json()
    for device in device_list['devices']:
        remove_device(device['_id']['$oid'])

def remove_device(id):
    print("send command remove device id:", id)
    requests.delete("http://" + controller_ip + ":5001/api/v1/device",  params={'device_id': id})

def init():
    requests.post("http://" + controller_ip +  ":5001/api/v1/initialization", json={'service': 'snmp', 'management_ip':controller_ip})

def net_flow():
    requests.post("http://" + controller_ip +  ":5001/api/v1/initialization", json={'service': 'netflow', 'management_ip':controller_ip})

def main():
    print("1 : Add Device")
    print("2 : Remove All Device ")
    print("3 : Set Initialization")
    print("4 : Set NetFlow")
    action = input("Action : ")
    if action == '1':
        add_device()
    elif action == '2':
        remove_all_device()
    elif action == '3':
        init()
    elif action == '4':
        net_flow()

main()
