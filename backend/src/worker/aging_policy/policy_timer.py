import time
import logging

class TimerPolicyWorker:
    def __init__(self, policy_number):
        self.policy_number = policy_number

    def run(self):
        while True:
            print("############################################")
            print("############################################")
            print("############################################")
            print("############################################")
            time.sleep(1)