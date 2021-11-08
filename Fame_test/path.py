import requests
import ipaddress

from requests.models import Response

# response = requests.get("http://10.50.34.37:5001/api/v1/path/192.168.7.18,192.168.4.2")
# print(response.json())
# links = requests.get("http://10.50.34.37:5001/api/v1/link/").json()

def get_wildcard(mask):
    mask = mask.split(".")
    for num in range(len(mask)):
        mask[num] = str(255 - int(mask[num]))
    return ".".join(mask)

def get_mask(manage_ip):
    device = requests.get("http://10.50.34.37:5001/api/v1/device/mgmtip/"+manage_ip).json()['device']
    for interface in device['interfaces']:
        if 'ipv4_address' in interface:
            if interface['ipv4_address'] == manage_ip:
                return interface['subnet']

# def get_network(manage_ip):
#     net = ipaddress.ip_network(manage_ip+"/"+get_mask(manage_ip), strict=False)
#     net = str(net).splt("/")[0]
#     return net

def get_nexthop_from_management_ip(device_id1, device_id2):
    links = requests.get("http://10.50.34.37:5001/api/v1/link/").json()
    for link in links['links']:
        if device_id1 == link['src_node_ip'] and device_id2 == link['dst_node_ip']:
            return link['dst_ip']
        elif device_id1 == link['dst_node_ip'] and device_id2 == link['src_node_ip']:
            return link['src_ip']

    

# def find_nexthope_node(src, dest):
#     routes = requests.get("http://10.50.34.37:5001/api/v1/routes"+get_device_id(src)).json()
#     for route in routes['routes']:
#         if get_network(dest) == route['dst']:
#             return requests.get("http://10.50.34.37:5001/api/v1/device/"+route['next_hop']).json()['device']['management_ip']

def get_path(src_net, dst_manageip, nexthop_node=None):
    print("test")
    src_mangeip = "192.168.7.18"
    paths = requests.get("http://10.50.34.37:5001/api/v1/path/192.168.7.18,192.168.4.2").json()
    if nexthop_node is None:
        nexthop_node = find_nexthope_node("192.168.7.18", "192.168.4.2")
    short_paths = short_paths(paths['paths'], nexthop_node)
    print(type(short_paths))
    change_route(short_paths, src_net, src_mangeip, dst_manageip)

def change_route(path, src_net, src_mangeip, dst_manageip):
    ip = '10.50.34.37'
    src_mask = get_wildcard(get_mask(src_mangeip))
    dst_mask = get_wildcard(get_mask(dst_manageip))
    new_flow = {'name':'new_route', 'src_ip':src_net, 'src_port':'any', 'src_subnet':src_mask, 'dst_ip':dst_manageip, 'dst_port':'any', 'dst_subnet':dst_mask, 'actions':[]}
    print(new_flow)
    for i in range(len(path) - 1):
        url = "http://10.50.34.37:5001/api/v1/device/mgmtip/" + str(path[i])
        device = requests.get(url).json()
        device_id = device['device']['_id']['$oid']
        action = {'device_id':device_id, 'action':2, 'data':get_nexthop_from_management_ip(path[i], path[i+1])}
        new_flow['actions'].append(action)
        # print(new_flow)
    response = requests.post("http://10.50.34.37:5001/api/v1/flow/routing", json=new_flow)
    print(response)
    # print(path)
    # print("change route success")


path = ["192.168.7.18","192.168.7.34","192.168.7.17","192.168.1.1","192.168.1.2","192.168.4.2"]

change_route(path, '192.168.7.18', '192.168.7.18', '192.168.4.2')