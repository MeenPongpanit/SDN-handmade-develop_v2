import time
from pymongo import MongoClient
import requests
from threading import Thread 
import time

class MyThread(Thread):
    def __init__(self, flow_id, timeout):
        Thread.__init__(self)
        self.flow_id = str(flow_id)
        self.timeout = timeout
        self.controller_ip = '10.50.34.37'

    def run(self):
        time.sleep(self.timeout)
        payload = {'flow_id': self.flow_id}
        response = requests.delete("http://"+self.controller_ip+":5001/api/v1/flow/routing",  params=payload)

class TimerPolicyWorker:
    def __init__(self, policy_number):
        self.policy_number = policy_number
        self.client = MongoClient('localhost', 27017)
        self.flow = self.client.sdn01.flow_routing.find()
        self.running_policy = []

    def run(self):
        while True:
            for obj in self.flow:
                if obj['flow_id'] not in self.running_policy:
                    self.running_policy.append(obj['flow_id'])
                    timeout = 10
                    tread_obj = MyThread(obj['flow_id'], timeout)
                    tread_obj.start()
            print("############################")
            print(self.running_policy)
            print("############################")
            time.sleep(1)
    
