import time
from pymongo import MongoClient

class TimerPolicyWorker:
    def __init__(self, policy_number):
        self.policy_number = policy_number
        self.client = MongoClient('localhost', 27017)
        self.flow = self.client.sdn01.flow_routing.find()
        self.running_policy = []

    def update_currentflow(self):
        for obj in self.flow:
            self.running_policy.append(obj)
            print("############################")
            print(self.running_policy)
            print("############################")

    def run(self):
        while True:
            self.update_currentflow(self)
            time.sleep(1)
    
