import time
from pymongo import MongoClient
import requests
import time
import concurrent.futures
from threading import Thread
from change_route import *

class Counter(Thread):
    def __init__(self, key, client):
        Thread.__init__(self)
        self.key = key
        self.timeout = 60
        self.client = client

    def run(self):
        time.sleep(self.timeout)

        
        while True:
            if self.timeout > 5:
                timeout = self.timeout
                time.sleep(timeout)
            else:
                # key = self.key
                flow = self.client.sdn01.flow_routing.find()
                for obj in flow:
                    #if key[0] == obj['src_ip'] and key[1] == obj['src_port'] and key[2] == obj['dst_ip'] and key[3] == obj['dst_port']:
                    if all(self.key[i] == obj[i] for i in self.key):
                        payload = {'flow_id':str(obj['flow_id'])}
                        # requests.delete("http://localhost:5001/api/v1/flow/routing",  params=payload)
                        break
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
                    key = {i:obj[i] for i in ['src_ip', 'src_port', 'dst_ip', 'dst_port', 'src_wildcard']}
                    # key = (obj['src_ip'] + "-" + obj['src_port'] + "-" + obj['dst_ip'] + "-" + obj['dst_port'] + "-" + obj['src_wildcard']).split("-")
                    Counter(key, self.client).start()
                    
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            time.sleep(20)
