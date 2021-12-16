"""This file is for calling change route api"""
import requests
import time
from ipaddress import IPv4Network, IPv4Address, ip_network



start = time.perf_counter()
controller_ip = "10.50.34.15"




def call_change_route_api():
    """prepare all agrs need for change route and call it's API"""
    src_net, dst_net = '192.168.8.0', '192.168.10.0'
    src_port, dst_port = '5555', '5555'
    path = get_path(src_net, dst_net)
    print("A")
    change_route(path, src_net, dst_net, src_port, dst_port)

def get_path(src_net, dst_net):
    """get all possible path from src_network to dst_network"""
    print(src_net)
    src_mgmtip = get_device_ip_from_device_id(get_device_id_from_network(src_net))
    print("SRC_MNIP = ", src_mgmtip)
    dst_mgmtip = get_device_ip_from_device_id(get_device_id_from_network(dst_net))
    path_s = requests.get("http://"+controller_ip+":5001/api/v1/path/"+src_mgmtip+","+dst_mgmtip).json()['paths']
    """
    path_s format 
    [{'route_id': '192.168.8.1,192.168.7.34,192.168.1.2', 'start_node': '192.168.8.1', 'nexthop_node': '192.168.7.34',
     'end_node': '192.168.1.2', 'path': ['192.168.8.1', '192.168.7.34', '192.168.7.17', '192.168.1.1', '192.168.1.2']}]
    """
    path = select_path(path_s)
    return path

def get_device_id_from_network(network):
    print("Network = ", network)
    routes = requests.get("http://"+controller_ip+":5001/api/v1/routes/").json()['routes']
    for route in routes:
        if route['dst'] == network and route['next_hop'] == "0.0.0.0":
            if get_device_ip_from_device_id(route['device_id']['$oid']) != None:
                return route['device_id']['$oid']

def get_device_ip_from_device_id(device_id):
    print(device_id)
    print()
    if requests.get("http://"+controller_ip+":5001/api/v1/device/"+device_id).json()['device'] != []:
        print("dsfsdfdsfsdf")
        return requests.get("http://"+controller_ip+":5001/api/v1/device/"+device_id).json()['device'][0]['device_ip']
    return None

def select_path(paths):
    """paths is all possible path from src to dst this function will return path you select from your algorithm"""
    path = paths[0]['path']
    return path

def change_route(path, src_net, dst_net, src_port=None, dst_port=None):
    """call API send agrs to database wait for config is pulling see more flow_routing.py"""
    src_wildcard = get_wild_card(get_mask(src_net))
    dst_wildcard = get_wild_card(get_mask(dst_net))
    if src_port == None:
        src_port = 'any'
    if dst_port == None:
        dst_port = 'any'
    new_flow = {'name':'new_route', 'src_ip':src_net, 'src_port':src_port, 'src_subnet':src_wildcard, 'dst_ip':dst_net, 'dst_port':dst_port, 'dst_subnet':dst_wildcard, 'actions':[]}
    for i in range(len(path)-1):
        device = requests.get("http://{}:5001/api/v1/device/mgmtip/{}".format(
            controller_ip,
            path[i]
        )).json()
        device_id = device['device']['_id']['$oid']
        next_hop_ip = get_nexthop_from_management_ip(path[i], path[i+1])
        action = {'device_id':device_id, 'action':2, 'data':next_hop_ip}
        new_flow['actions'].append(action)
        new_flow['aging_time'] = 20

    response = requests.post("http://"+controller_ip+":5001/api/v1/flow/routing", json=new_flow)
    print("change route success")

def get_mask(ip):
    """return subnetmask from ip"""
    mgmtip = get_device_ip_from_device_id(get_device_id_from_network(ip))
    device = requests.get("http://"+controller_ip+":5001/api/v1/device/mgmtip/"+mgmtip).json()['device']
    for interface in device['interfaces']:
        if 'ipv4_address' in interface:
            if interface['ipv4_address'] == mgmtip:
                return interface['subnet']
    return None

def get_wild_card(subnet_mask):
    """return wild card mask from subnet mask"""
    mask = subnet_mask.split(".")
    for num in range(len(mask)):
        mask[num] = str(255 - int(mask[num]))
    wildcard = ".".join(mask)
    return wildcard

def get_nexthop_from_management_ip(device_id1, device_id2):
    links = requests.get("http://"+controller_ip+":5001/api/v1/link/").json()
    for link in links['links']:
        if device_id1 == link['src_node_ip'] and device_id2 == link['dst_node_ip']:
            return link['dst_ip']
        elif device_id1 == link['dst_node_ip'] and device_id2 == link['src_node_ip']:
            return link['src_ip']

def get_all_inteface(device):
    interface = []
    for i in device['device']['interfaces']:
        if i['description'] != 'Null0':
            interface.append(i['description'])
    return interface

def call_delete():
    """test delete"""
    payload = {'flow_id':'1'}
    response = requests.delete("http://"+controller_ip+":5001/api/v1/flow/routing",  params=payload)
    print(response)



def convert_ip_to_network(ip, mask):
    bi_mask = '1'*mask + '0'*(32-mask)
    bi_ip = ''.join([bin(int(i)+256)[3:] for i in str(ip).split('.')])
    bi_network = ''.join([(x, '0')[y == '0'] for x, y in zip(bi_ip, bi_mask)])
    network_address = str(IPv4Address(int(bi_network, 2)))
    return network_address

print('555555' + get_device_id_from_network('192.168.8.0'))
call_change_route_api()

