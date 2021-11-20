import time
from pymongo import MongoClient
from threading import Thread 
import time

class MyThread(Thread):

    def __init__(self, timeout):
        Thread.__init__(self)
        self.timeout = timeout

    def run(self):
        time.sleep(self.policy_number)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("NOW DELETE THIS")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

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
                    timeout = 10
                    tread_obj = MyThread(timeout)
            print("############################")
            print(self.running_policy)
            print("############################")
            time.sleep(1)
    
