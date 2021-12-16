import time
from pymongo import MongoClient
import requests
import time
import concurrent.futures
from threading import Thread
from ipaddress import IPv4Network, IPv4Address, ip_network


class Counter(Thread):
    def __init__(self, key, info, client, aging_time):
        Thread.__init__(self)
        self.key = key
        self.info = info
        self.timeout = aging_time
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
            query_filter = {}
            for i in self.key:
                if self.key[i].lower() != 'any':
                    if 'addr' in i:
                        ip_prefix = IPv4Address._prefix_from_ip_int(int(IPv4Address(self.info[i + '_wildcard']))^(2**32-1))
                        ip_network = IPv4Network(convert_ip_to_network(self.key[i], int(ip_prefix)) + '/' + str(ip_prefix))
                        query_filter[i] = {'$in':[str(i) for i in ip_network]}
                    else:
                        query_filter[i] = int(self.key[i])

            check = 0
            flows = self.client.sdn01.flow_stat.find(query_filter)
            for i in flows:
                check = 1
            
            if check:
                time.sleep(self.timeout)
            else:
                payload = {'flow_id': self.info['flow_id']}
                print(payload)
                requests.delete("http://localhost:5001/api/v1/flow/routing",  params=payload)
                break


class TimerPolicyWorker:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def run(self):
        while True:
            self.flow = self.client.sdn01.flow_routing.find()
            for obj in self.flow:
                if len(obj) == 15:
                    key = {
                        'ipv4_src_addr' : obj['src_ip'],
                        'l4_src_port' : obj['src_port'],
                        'ipv4_dst_addr' : obj['dst_ip'],
                        'l4_dst_port' : obj['dst_port'],
                        }
                    info = {
                        'ipv4_src_addr_wildcard' : obj['src_wildcard'],
                        'ipv4_dst_addr_wildcard' : obj['dst_wildcard'],
                        'flow_id' : obj['flow_id']
                    }
                    # key = {i:obj[i] for i in ['src_ip', 'src_port', 'dst_ip', 'dst_port', 'src_wildcard', 'dst_wildcard', 'flow_id']}
                    if obj['aging_time']:
                        Counter(key, info, self.client, obj['aging_time']).start()
            time.sleep(60)
