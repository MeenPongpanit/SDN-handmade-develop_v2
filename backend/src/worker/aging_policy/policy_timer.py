import time
from pymongo import MongoClient
import requests
import time
import concurrent.futures

class TimerPolicyWorker:
    def __init__(self, obj_id):
        self.obj_id = obj_id
        self.client = MongoClient('localhost', 27017)
        self.flow = self.client.sdn01.flow_routing.find() 
        self.timeout = 20
        self.running_policy = []

    def run(self):
        while True:
            for obj in self.flow:
                self.running_policy.append(obj)
            print("############################")
            print(self.running_policy)
            print("############################")
            time.sleep(2)
