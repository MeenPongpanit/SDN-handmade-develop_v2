import time
from pymongo import MongoClient
import requests
import time
import concurrent.futures
from threading import Thread
from ipaddress import IPv4Network, IPv4Address

class Counter(Thread):
    def __init__(self, key, client):
        Thread.__init__(self)
        self.key = key
        self.timeout = 2
        self.client = client

    def run(self):
        time.sleep(self.timeout)
        while True:
            src_ip_list, dst_ip_list = [], []
            src_prefix, dst_prefix = IPv4Address._prefix_from_ip_int(int(IPv4Address(self.key['src_wildcard']))^(2**32-1)), IPv4Address._prefix_from_ip_int(int(IPv4Address(self.key['dst_wildcard']))^(2**32-1))
            src_network_obj = IPv4Network(self.key['src_ip'] + '/' + str(src_prefix))
            dst_network_obj = IPv4Network(self.key['dst_ip'] + '/' + str(dst_prefix))
            for i in src_network_obj:
                src_ip_list.append(str(i))
            for i in dst_network_obj:
                dst_ip_list.append(str(i))

            if str(self.key['src_port']).lower() == 'any' and str(self.key['dst_port']).lower() == 'any':
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list} } )
            elif str(self.key['src_port']).lower() == 'any':
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list}, 'l4_dst_port': {'$in': int(self.key['dst_port'])} } )
            elif str(self.key['dst_port']).lower() == 'any':
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list}, 'l4_src_port': {'$in': int(self.key['src_port'])} } )
            else:
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list}, 'l4_src_port': {'$in': int(self.key['src_port'])}, 'l4_dst_port': {'$in': int(self.key['dst_port'])} } )
            
            try:
                if flows[0]:
                    time.sleep(self.timeout)
            except:
                payload = {'flow_id': self.key['flow_id']}
                # requests.delete("http://localhost:5001/api/v1/flow/routing",  params=payload)

                break
        


class TimerPolicyWorker:
    def __init__(self, obj_id):
        self.obj_id = obj_id
        self.client = MongoClient('localhost', 27017)   
        self.timeout = 20

    def run(self):
        while True:
            self.flow = self.client.sdn01.flow_routing.find()
            for obj in self.flow:
                if len(obj) == 14:
                    key = {i:obj[i] for i in ['src_ip', 'src_port', 'dst_ip', 'dst_port', 'src_wildcard', 'dst_wildcard', 'flow_id']}
                    Counter(key, self.client).start()
                    
            time.sleep(20)
