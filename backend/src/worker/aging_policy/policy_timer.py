import time
from pymongo import MongoClient
import requests
import time
import concurrent.futures

class TimerPolicyWorker:
    def __init__(self, obj_id):
        self.obj_id = obj_id
        self.client = MongoClient('localhost', 27017)   
        self.timeout = 20
        self.running_policy = []

    def run(self):
        while True:
            self.flow = self.client.sdn01.flow_routing.find()
            for obj in self.flow:
                if len(obj) == 14:
                    key = obj['src_ip'] + "-" + obj['src_port'] + "-" + obj['dst_ip'] + "-" + obj['dst_port']
                    if key not in self.running_policy:
                        self.running_policy.append(key)
            print(key)
            print("############################")

            # print(self.running_policy)
            print("############################")
            time.sleep(2)
