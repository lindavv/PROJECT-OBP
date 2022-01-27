import threading
#from algorithm.tracking_orders import *
import time
from datetime import datetime, timedelta

testsecs = [3,5,2,8]
#del testsecs[0]
#print(testsecs)
def simulation():
    if len(testsecs)>0:
        threading.Timer(testsecs[0], simulation).start()
        del testsecs[0]
        return print(t.get_time())



#t = threading.Timer(5,simulation)
#t.start()

class sim_time:

    def __init__(self, time):
        self.sim_start = time
        self.timer = None

    def start(self):
        self.timer = time.perf_counter()

    def get_time(self):
        elapsed_time = time.perf_counter() - self.timer
        return self.sim_start + timedelta(minutes = elapsed_time/60)


date = datetime.now().date()
sim_start = datetime.strptime(str(date) + ' ' + '12:00:00', '%Y-%m-%d %H:%M:%S')
t = sim_time(sim_start)
t.start()
simulation()
