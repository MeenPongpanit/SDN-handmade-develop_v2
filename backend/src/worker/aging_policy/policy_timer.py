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
        self.timeout = 10
        self.client = client

    def run(self):
        def convert_ip_to_network(ip, mask):
            bi_mask = '1'*mask + '0'*(32-mask)
            bi_ip = ''.join([bin(int(i)+256)[3:] for i in str(ip).split('.')])
            bi_network = ''.join([(x, '0')[y == '0'] for x, y in zip(bi_ip, bi_mask)])
            network_address = str(IPv4Address(int(bi_network, 2)))
            return network_address

        time.sleep(self.timeout)
        while True:
            src_ip_list, dst_ip_list = [], []
            src_prefix, dst_prefix = IPv4Address._prefix_from_ip_int(int(IPv4Address(self.key['src_wildcard']))^(2**32-1)), IPv4Address._prefix_from_ip_int(int(IPv4Address(self.key['dst_wildcard']))^(2**32-1))
            src_network_obj = IPv4Network(convert_ip_to_network(self.key['src_ip'], int(src_prefix)) + '/' + str(src_prefix))
            dst_network_obj = IPv4Network(convert_ip_to_network(self.key['dst_ip'], int(dst_prefix)) + '/' + str(dst_prefix))
            for i in src_network_obj:
                src_ip_list.append(str(i))
            for i in dst_network_obj:
                dst_ip_list.append(str(i))

            if str(self.key['src_port']).lower() == 'any' and str(self.key['dst_port']).lower() == 'any':
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list} } )
                print("11111111111111111111111111111111111111111")
                print("11111111111111111111111111111111111111111")
                print("11111111111111111111111111111111111111111")
                print("11111111111111111111111111111111111111111")
                for i in flows:
                    print(str(i))
            elif str(self.key['src_port']).lower() == 'any':
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list}, 'l4_dst_port': {'$in': [int(self.key['dst_port'])]} } )
                print("2222222222222222222222222222222222222")
                print("2222222222222222222222222222222222222")
                print("2222222222222222222222222222222222222")
                print("2222222222222222222222222222222222222")
                for i in flows:
                    print(str(i))
            elif str(self.key['dst_port']).lower() == 'any':
                # flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list}, 'l4_src_port': {'$in': [int(self.key['src_port'])]} } )
                print("3333333333333333333333333333333333333")
                print("3333333333333333333333333333333333333")
                print("3333333333333333333333333333333333333")
                print("3333333333333333333333333333333333333")
                print(src_ip_list)
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list}, 'l4_src_port': {'$in': [int(self.key['src_port'])]} } )
                for i in flows:
                    print(str(i))
            else:
                flows = self.client.sdn01.flow_stat.find({ 'ipv4_src_addr': {'$in': src_ip_list} ,  'ipv4_dst_addr': {'$in': dst_ip_list}, 'l4_src_port': {'$in': [int(self.key['src_port'])] }, 'l4_dst_port': {'$in': [int(self.key['dst_port'])]} } )
                print("444444444444444444444444444444444444444444")
                print("444444444444444444444444444444444444444444")
                print("444444444444444444444444444444444444444444")
                print("444444444444444444444444444444444444444444")
                for i in flows:
                    print(str(i))
            check = []
            for i in flows:
                check.append(i)
                break
            if len(check):
                print("=====================")
                print("=====================")
                time.sleep(self.timeout)
            else:
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                payload = {'flow_id': self.key['flow_id']}
                print(payload)
                # requests.delete("http://localhost:5001/api/v1/flow/routing",  params=payload)
                break


class TimerPolicyWorker:
    def __init__(self, obj_id):
        self.obj_id = obj_id
        self.client = MongoClient('localhost', 27017)

    def run(self):
        while True:
            self.flow = self.client.sdn01.flow_routing.find()
            for obj in self.flow:
                if len(obj) == 14:
                    key = {i:obj[i] for i in ['src_ip', 'src_port', 'dst_ip', 'dst_port', 'src_wildcard', 'dst_wildcard', 'flow_id']}
                    Counter(key, self.client).start()
            time.sleep(10)
