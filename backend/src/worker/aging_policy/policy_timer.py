import time
from pymongo import MongoClient

class TimerPolicyWorker:
    def __init__(self, policy_number):
        self.policy_number = policy_number
        self.client = MongoClient('localhost', 27017)
        self.flow = self.client.sdn01.flow_routing.find() 

    def run(self):
        running_policy = []
        while True:
            for obj in self.flow:
                running_policy.append(obj)
            print("############################")
            print(running_policy)
            print("############################")
            time.sleep(1)