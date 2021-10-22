import time
import pyRserve

R_connection = None

def prepare_R():
    global R_connection
    R_connection = pyRserve.connect()

    return R_connection

def shutdown_R():
    if R_connection != None:
        R_connection.shutdown()

class Algorithm:
    estimates = []
    time_used = 0
    name = ""

    def __init__(self):
        global R_connection
        self.R_connection = R_connection

    def guess(self, changepoints, estimates):
        self.time_used = time.time_ns() - self.time_used
        if len(estimates) < len(changepoints):
            print(f"{self.name} didnt provide enough changepoints")
        self.estimates = estimates
    
    def start_timer(self):
        self.time_used = time.time_ns()

    def estimate(self, dist):
        raise NotImplementedError
