import time
from pymongo import MongoClient
import requests
import time
import concurrent.futures
from threading import Thread 

class Counter(Thread):
    def __init__(self, key):
        Thread.__init__(self)
        self.key = key
        self.timeout = 10

    def run(self):
        time.sleep(self.timeout)
        key = self.key.split('-')
        flow = MongoClient('localhost', 27017).sdn01.flow_routing.find()

        for obj in flow:
            if key[0] == obj['src_ip'] and key[1] == obj['src_port'] and key[2] == obj['dst_ip'] and key[3] == obj['dst_port']:
                print("@@@@@@@@@@@@@")
                print("@@@@@@@@@@@@@")
                print("@@@@@@@@@@@@@")
                print(obj['flow_id'])
                print("@@@@@@@@@@@@@")
                print("@@@@@@@@@@@@@")
                print("@@@@@@@@@@@@@")
        # payload = {'flow_id':'1'}
        # requests.delete("http://localhost:5001/api/v1/flow/routing",  params=payload)
        # print("@@@@@@@@@@@@@@")
        # print("@@@@@@@@@@@@@@")
        # print("@@@@@@@@@@@@@@")


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
                        Counter(key).start()


            print(self.running_policy)
            print("############################")

            # print(self.running_policy)
            print("############################")
            time.sleep(2)
