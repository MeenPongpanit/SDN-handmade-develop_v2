import requests
import ipaddress
ip = "10.50.34.37"

def get_wildcard(mask):
    mask = mask.split(".")
    for num in range(len(mask)):
        mask[num] = str(255 - int(mask[num]))
    return ".".join(mask)

def get_mask(mgmtip):
    device = requests.get("http://"+ip+":5001/api/v1/device/mgmtip/"+mgmtip).json()['device']
    for interface in device['interfaces']:
        if 'ipv4_address' in interface:
            if interface['ipv4_address'] == mgmtip:
                return interface['subnet']

def get_nexthop_from_management_ip(device_id1, device_id2):
    links = requests.get("http://"+ip+":5001/api/v1/link/").json()
    for link in links['links']:
        if device_id1 == link['src_node_ip'] and device_id2 == link['dst_node_ip']:
            return link['dst_ip']
        elif device_id1 == link['dst_node_ip'] and device_id2 == link['src_node_ip']:
            return link['src_ip']

def get_device_ip_from_device_id(device_id):
    if requests.get("http://"+ip+":5001/api/v1/device/"+device_id).json()['device'] != []:
        return requests.get("http://"+ip+":5001/api/v1/device/"+device_id).json()['device'][0]['device_ip']
    return None

def get_device_id_from_network(network):
    routes = requests.get("http://"+ip+":5001/api/v1/routes/").json()['routes']
    for route in routes:
        if route['dst'] == network and route['next_hop'] == "0.0.0.0":
            if get_device_ip_from_device_id(route['device_id']['$oid']) != None:
                print(route['device_id']['$oid'])
                return route['device_id']['$oid']


def get_network(mgmtip):
    net = ipaddress.ip_network(mgmtip+"/"+get_mask(mgmtip), strict=False)
    net = str(net).split("/")[0]
    return net

def get_device_id(mgmtip):
    device = requests.get("http://"+ip+":5001/api/v1/device/mgmtip/"+mgmtip).json()['device']
    return device['_id']['$oid']

def get_all_inteface(device):
    interface = []
    for i in device['device']['interfaces']:
        if i['description'] != 'Null0':
            interface.append(i['description'])
    return interface

def find_nexthop_node(src_mgmtip, dst_mgmtip):
    routes = requests.get("http://"+ip+":5001/api/v1/routes/"+get_device_id(src_mgmtip)).json()
    for route in routes['routes']:
        if get_network(dst_mgmtip) == route['dst']:
            return requests.get("http://"+ip+":5001/api/v1/device/"+route['next_hop']).json()['device']['management_ip']

# def get_interface(ip):
#     interface = ip
#     print(interface)
#     return str(interface)

def change_route(path, src_net, src_mgmtip, dst_mgmtip):
    src_mask = get_wildcard(get_mask(src_mgmtip))
    dst_mask = get_wildcard(get_mask(dst_mgmtip))
    new_flow = {'name':'new_route', 'src_ip':src_net, 'src_port':'any', 'src_subnet':src_mask, 'dst_ip':dst_mgmtip, 'dst_port':'any', 'dst_subnet':dst_mask, 'actions':[]}
    for i in range(len(path)-1):
        device = requests.get("http://{}:5001/api/v1/device/mgmtip/{}".format(
            ip,
            path[i]
        )).json()
        device_id = device['device']['_id']['$oid']
        next_hop_ip = get_nexthop_from_management_ip(path[i], path[i+1])
        interface = get_all_inteface(device)
        print(interface)
        action = {'device_id':device_id, 'action':2, 'interface':interface, 'data':next_hop_ip}
        new_flow['actions'].append(action)
    response = requests.post("http://"+ip+":5001/api/v1/flow/routing", json=new_flow)
    print("change route success")

def my_path(paths):
    check = paths[0].split(".")[1]
    for path in paths:
        if path.split(".")[1] != check:
            return False
    return True

def get_path(src_net, dst_mgmtip, nexthop_node=None):
    src_mgmtip = get_device_ip_from_device_id(get_device_id_from_network(src_net))
    paths = requests.get("http://"+ip+":5001/api/v1/path/"+src_mgmtip+","+dst_mgmtip).json()
    if nexthop_node is None:
        nexthop_node = find_nexthop_node(src_mgmtip, dst_mgmtip)
    for path in paths['paths']:
        change_route(path['path'], src_net, src_mgmtip, dst_mgmtip)
        break


#print(get_device_id_from_network("100.1.2.0"))
#print(get_device_ip_from_device_id(get_device_id_from_network("100.1.1.0")))

#get_path("192.168.8.0", "192.168.1.2", "192.168.7.49") # A1->B
# get_path("100.1.2.0", "100.1.3.1", "100.1.7.1") # A2->B

graph = requests.get("http://10.50.34.37:5001/api/v1/graph").json()

#get_mask("100.3.11.1")
#find_nexthop_node("100.3.11.1", "100.3.12.1")
#get_path("100.1.3.1", "100.1.5.1") # A'->A''
#get_path("100.1.5.1", "100.1.1.1") # A''->A
#get_path("100.1.2.1", "100.1.4.1") # B->B'
#get_path("100.1.4.1", "100.1.6.1") # B'->B''
#get_path("100.1.6.1", "100.1.1.1") # B''->B

#========================================================