import sys
import threading
from pprint import pprint
from algorithm.tracking_orders import read_df_of_day, create_orders, orders, order_to_node
from classes.vehicle import assign_order
from classes.region import regions
import time
from datetime import datetime, timedelta
from six.moves import input

sim_secs = [3,5,2,8]
#del testsecs[0]
#print(testsecs)
glob = 'test2'

def simulation(timer, sim_secs, speed, orders_df, ord_num = 0):
    while len(sim_secs)>0:
        call_in = sim_secs[0]/speed
        print(timer.get_time(speed))
        #print(regions[3].get_vehicles())
        #print(glob)
        del sim_secs[0]
        ord = create_orders(ord_num,orders_df)
        picks, drops = [], []
        for i in range(len(ord)):
            pick, drop = order_to_node(ord[i])
            picks.append(pick)
            drops.append(drop)
            assign_order(pick, drop, ord[i].time, mode='time')
        time.sleep(call_in)
        #threading.Timer(call_in, simulation, [timer, sim_secs, speed, order_df, ord_num+1]).start()
        #thread.daemon = True
        #thread.start()
#    else:
#        pprint(vars(regions[6]))
#        pprint(vars(regions[6].get_vehicles()[0]))
#        print('Simulation ended')

start = time.perf_counter()
def simulation2():
    if len(sim_secs)>0:
        call_in = sim_secs[0]
        print(time.perf_counter()-start)
        print(glob)
        del sim_secs[0]
        threading.Timer(call_in, simulation2).start()
    else:
        print('Simulation ended')


def orders_diff_time(orders_df,sim_time_start):
    """
    :param orders_df: Data frame of orders to be used in simulation
    :param sim_time_start: time of simulation start (will be the same as time of first order
    :return: in seconds the time difference between every successive incoming order. This tells us when we have to check for an incoming order again
    """
    inc_sec = [0]
    for i in range(len(orders_df)-1):
        inc_sec.append((orders_df['order_time'][i+1]-orders_df['order_time'][i]).total_seconds())
    return inc_sec

#t = threading.Timer(5,simulation)
#t.start()

class sim_time:

    def __init__(self, time):
        self.sim_start = time
        self.timer = None

    def start(self):
        self.timer = time.perf_counter()

    def get_time(self, speed):
        elapsed_time = time.perf_counter() - self.timer
        return self.sim_start + timedelta(seconds = elapsed_time*speed)

def background():
    while True:
        time.sleep(5)
        print('nothing')


class incOrder:
    def __init__(self, time):
        self.pickup =[]
        self.dropoff=[]
        #To get time in simulation
        self.sim_time = time
        self.timer = time
        #self.regions = regions

    def order_pop_up(self,pick,drop):
        print('Order incoming...')
        self.pickup.append(pick)
        self.dropoff.append(drop)

    def assign(self):
        #for i in range(len(self.pickup)):
        print('order with id ', self.pickup[0].order.id, ' of time ', self.pickup[0].order.time, ' was assigned.')
        self.pickup.remove(self.pickup[0])
        self.dropoff.remove(self.dropoff[0])

    def get_time(self, speed):
        elapsed_time = time.perf_counter() - self.timer
        return self.sim_start + timedelta(seconds = elapsed_time*speed)

    def start(self):
        self.timer = time.perf_counter()

def order_pop_up(incOrd,cond, sleepscheduele, orders_df, speed):
    for i in range(len(sleepscheduele)):
        order = create_orders(i, orders_df)
        for j in range(len(order)):
            pick, drop = order_to_node(order[j])
            with cond:
                incOrd.order_pop_up(pick,drop)
                cond.notify()
        #print(incOrd.pickup)
        print('sleep for ', sleepscheduele[i]/speed, ' seconds')
        time.sleep(sleepscheduele[i]/speed)

def assign(incOrd,cond):
    cond.acquire()
    while True:
        try:
            incOrd.assign()
            print(incOrd.pickup)
        except:
            print('no order')
            val = cond.wait(20)
            if val:
                print('assigning order')
                #incOrd.assign()
                continue
            else:
                print('waiting timeout...')
                break

date = datetime.now().date()
orders_df = read_df_of_day(date)                                                        #Reads df of corresponding weekday, but saves the times with current date
first_ord_time = str(orders_df['order_time'][0].time())
sim_start = datetime.strptime(str(date) + ' ' + first_ord_time, '%Y-%m-%d %H:%M:%S')
sim_sec = orders_diff_time(orders_df,sim_start)
testsecs = sim_sec[0:5]

speed=100
incOrd = incOrder(sim_start)
incOrd.start() #Start timer of simulation
print(sim_start)
#Condition object
cond = threading.Condition()
#producer thread
p = threading.Thread(target=order_pop_up, args=(incOrd, cond, testsecs, orders_df,speed,))
p.start()
#Consumer thread
c=threading.Thread(target=assign, args=(incOrd, cond,))
c.start()

#p.join()
#c.join()


#print(sim_sec[0:5])
#testsecs = sim_sec[0:8]
#testsecs2 = sim_sec[8:12]

#t = sim_time(sim_start)
#t.start()
#print(sim_start)
#threading1 = threading.Thread(target=background)
#threading1.daemon = True
#threading1.start()
#simulation(t, testsecs,100, orders_df,0)
#while True:
#    if input() == '1':
#        #sys.exit()
#        time_now = t.get_time(100)
#        simulation(t,testsecs2,100,orders_df,0)
#    else:
#        print('Noooo')
#    dropcount = 0
#    for i in range(len(orders_df)):
#        if orders_df['order_time'][i] < time_now:
#            dropcount +=1
#    for i in range(dropcount):
#        orders_df = orders_df.drop(orders_df.index[0])
    #first_ord_time = str(orders_df['order_time'][0].time())
    #sim_start = datetime.strptime(str(date) + ' ' + first_ord_time, '%Y-%m-%d %H:%M:%S')
    #sim_sec = orders_diff_time(orders_df, sim_start)
    #t = sim_time(sim_start)
    #t.start()
    #simulation(t,sim_sec,100,orders_df,0)

#print('input')

#regions[3].set_vehicles([])
#print(regions[3].get_vehicles())
#time_now = t.get_time(100)+timedelta(hours = 1)
#print(time_now)
#print(orders_df['order_time'][0])
#print(orders_df['order_time'][0] < time_now)

#while orders_df['order_time'][0] < time_now:

#print(orders_df.iloc[0])
#orders_df = orders_df.drop(orders_df.index[0])
#print(orders_df.iloc[0])
#print(t.get_time(100))

#start = time.perf_counter()
#simulation2()

#simulation2()
#print(orders_df['order_time'][0].time())