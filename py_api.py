#<<<<<<< HEAD
import requests

#device
def device(device_name):
    url = "http://192.168.217.132:5001/api/v1/device/"+device_name
    response = requests.get(url)
    data = response.json()
    for device in data['devices']:
        print("device ip : "+device['device_ip'])
        print("device type : "+device['type'])
        print("description : "+device['description'])
        print()

#link
def link(device_name):
    url = "http://192.168.217.132:5001/api/v1/link/"+device_name
    response = requests.get(url)
    data = response.json()
    for link in data['links']:
        print("device 1 : "+link['src_node_hostname']+"("+link['src_ip']+")")
        print("device 2 : "+link['dst_node_hostname']+"("+link['dst_ip']+")")
        print("%  utilization")
        print()
#flow
def flow():
    url = "http://192.168.217.132:5001/api/v1/flow"
    response = requests.get(url)
    data = response.json()
    for flow in data['flows']:
        print("src_ip : "+flow['ipv4_src_addr']+" src_port : "+str(flow['l4_src_port']))
        print("dst_ip : "+flow['ipv4_dst_addr']+" dst_port : "+str(flow['l4_dst_port']))
        print()

#flow_routing
def flow_routing():
    url = "http://192.168.217.132:5001/api/v1/flow/routing"
    response = requests.get(url)
    data = response.json()
    print(data)

def get_device_name_by_ip(ip):
    url = "http://192.168.217.132:5001/api/v1/device/"+ip
    response = requests.get(url)
    data = response.json()
    return data['devices']['name']

#path
def path(src_node_ip, dst_node_ip):
    url = "http://192.168.217.132:5001/api/v1/path/"+src_node_ip+","+dst_node_ip
    response = requests.get(url)
    data = response.json()
    for path in data['paths']:
        print("rotue id "+path['route_id']+" : ", end="")
        print('start node '+path['start_node'], end=", ")
        print('nexthop node '+path['nexthop_node'], end=", ")
        print('end node '+path['end_node'])
        print()

#device(input("device_name or interface_ip or None"))
#link(input("device_name or None"))
#flow()
#flow_routing()
path(input("src_node_ip : "), input("dst_node_ip : "))
#=======
import requests

#device
def device(device_name):
    url = "http://192.168.217.132:5001/api/v1/device/"+device_name
    response = requests.get(url)
    data = response.json()
    for device in data['devices']:
        print("device ip : "+device['device_ip'])
        print("device type : "+device['type'])
        print("description : "+device['description'])
        print()

#link
def link(device_name):
    url = "http://192.168.217.132:5001/api/v1/link/"+device_name
    response = requests.get(url)
    data = response.json()
    for link in data['links']:
        print("device 1 : "+link['src_node_hostname']+"("+link['src_ip']+")")
        print("device 2 : "+link['dst_node_hostname']+"("+link['dst_ip']+")")
        print("%  utilization")
        print()
#flow
def flow():
    url = "http://192.168.217.132:5001/api/v1/flow"
    response = requests.get(url)
    data = response.json()
    for flow in data['flows']:
        print("src_ip : "+flow['ipv4_src_addr']+" src_port : "+str(flow['l4_src_port']))
        print("dst_ip : "+flow['ipv4_dst_addr']+" dst_port : "+str(flow['l4_dst_port']))
        print()

#flow_routing
def flow_routing():
    url = "http://192.168.217.132:5001/api/v1/flow/routing"
    response = requests.get(url)
    data = response.json()
    print(data)

def get_device_name_by_ip(ip):
    url = "http://192.168.217.132:5001/api/v1/device/"+ip
    response = requests.get(url)
    data = response.json()
    return data['devices']['name']

#path
def path(src_node_ip, dst_node_ip):
    url = "http://192.168.217.132:5001/api/v1/path/"+src_node_ip+","+dst_node_ip
    response = requests.get(url)
    data = response.json()
    for path in data['paths']:
        print("rotue id "+path['route_id']+" : ", end="")
        print('start node '+path['start_node'], end=", ")
        print('nexthop node '+path['nexthop_node'], end=", ")
        print('end node '+path['end_node'])
        print()

#device(input("device_name or interface_ip or None"))
#link(input("device_name or None"))
#flow()
#flow_routing()
path(input("src_node_ip : "), input("dst_node_ip : "))
#>>>>>>> 5d0d22bde1fe001196028b13b3b50c82f89a330e
