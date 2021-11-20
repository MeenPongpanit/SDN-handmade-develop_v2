import time

class TimerPolicyWorker:
    def __init__(self, policy_number):
        self.policy_number = policy_number

    def run(self):
        while True:
            print("------------------------------------")
            print(self.policy_number)
            print("------------------------------------")
            time.sleep(1)