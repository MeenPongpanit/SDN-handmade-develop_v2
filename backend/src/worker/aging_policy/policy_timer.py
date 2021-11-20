import time
from pymongo import MongoClient
import requests
import time
import concurrent.futures


    

class TimerPolicyWorker:
    def __init__(self, policy_number):
        self.policy_number = policy_number
        self.client = MongoClient('localhost', 27017)
        
        self.timeout = 3
        self.running_policy = []

    def run(self):

        def delete(flow_id, timeout):
            time.sleep(timeout)
            #if condition last switch too long
            payload = {'flow_id': flow_id}
            print("@@@@@@@@@@@@@@")
            print("Policy %d NOW REMOVE" %(flow_id))
            print("@@@@@@@@@@@@@@")
            response = requests.delete("http://localhost:5001/api/v1/flow/routing",  params=payload)
            return flow_id
        
        while True:
            self.flow = self.client.sdn01.flow_routing.find()
            for obj in self.flow:
                print(obj)
                try:
                    if obj['flow_id'] not in self.running_policy:
                        self.running_policy.append(obj['flow_id'])
        
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(delete, obj['flow_id'], self.timeout)
                            return_value = future.result()
                            print("########################")
                            print(return_value)
                            self.running_policy.remove(return_value)
                except:
                    print("updating flow in process")
            print(self.running_policy)
            time.sleep(1)
    
