import time
from pymongo import MongoClient

class TimerPolicyWorker:
    def __init__(self, policy_number):
        self.policy_number = policy_number
        self.client = MongoClient('localhost', 27017)
        self.flow = self.client.sdn01.flow_routing.find()
        self.running_policy = []

    def run(self):
        
        while True:
            for obj in self.flow:
                if obj['_id'] not in self.running_policy:
                    self.running_policy.append(obj['_id'])
            print("############################")
            print(self.running_policy)
            print("############################")
            time.sleep(1)
    
