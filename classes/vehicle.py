#import time
import copy
from datetime import datetime, timedelta
from stuff.map_dfs import dist
from classes.route_node import *
from classes.region import update_region

""" Needs Shift start and region as input argument when initialized. That is an object of datetime which states the starting time of this vehicle."""






class Vehicle:

    def __init__(self, region, shift, shift_start, shift_end, max_cap = 20, highspeed=1):

        self.region = region  # Index key in dictionary of regions (1 to 7)
        self.highspeed = highspeed     # highspeed roads
        # dynamically get position
        self.last_update = shift_start  # timestamp when last route was decided
        # self.next_destination                         # next node and time when this node is reached
        self.route = [self.set_depot(region, shift_start)]
        self.wait = [0]
        self.arrival = [shift_start]
        self.maxshift = [180]
        self.shift = shift                  #Either shift 1 or 2
        self.shift_start = shift_start
        self.shift_end = shift_end
        self.empty = 0                          #time in minutes until vehicle is empty

        # self.time_busy

        self.kms_total = 0
        self.kms = []       #saves the km between each consecutive node of the route
        self.cap = [max_cap]



    def set_route(self, route):
        self.route = route

    def set_wait(self, wait):
        self.wait = wait

    def set_arrival(self, arrival):
        self.arrival = arrival

    def set_maxshift(self, maxshift):
        self.maxshift = maxshift

    def get_route(self):
        return self.route

    def get_arrival(self):
        return self.arrival

    def get_empty(self):
        return self.empty

    def get_shift(self):
        return self.shift

    def get_shift_start(self):
        return self.shift_start

    def get_shift_end(self):
        return self.shift_end

    def set_shift_end(self, end):
        self.shift_end = end
    def set_depot(self, region, shift_start):
        depot = Route_node(0, 0, 0)
        depot.set_location(regions[region].depot)
        depot.set_time_window(shift_start, shift_start + timedelta(hours=4))
        return depot

    def drop_node(self, idx):
        """ Drop nodes when vehicle has passed these (based on time) """

        # update time the customer has been waiting!!
        waiting_time = 0
        delay = 0
        ord = self.route[idx].order
        type = self.route[idx].type_
        #update_order_status(type, ord)
        if self.route[idx].type_ == 1:

            # only do cases where we haven't calculated waiting time before (to avoid bug)
            #if ord.wait == 0:
            update_order_waiting_time(ord, self.arrival[idx])
            waiting_time = (self.arrival[idx]-ord.window[0]).total_seconds()/60
            delay = max(0, (self.arrival[idx]-ord.window[1]).total_seconds()/60)
        #Update kms driven for vehicle
        self.kms_total = self.kms_total+self.kms[0]
        #Update region
        update_region(self.region, self.route[idx].type_, self.kms[0], waiting_time, delay)
        # dropping nodes from vehicle
        del self.route[idx]
        del self.wait[idx]
        del self.arrival[idx]
        del self.maxshift[idx]
        del self.cap[idx]
        del self.kms[idx]

    def append_node(self, node):
        n = len(self.route)
        arr_node = max(self.arrival[n - 1] + timedelta(minutes=self.wait[n - 1]),
                       self.last_update) + timedelta(minutes=dist(self.route[n - 1], node))
        wait_node = max(0, (node.window[0] - arr_node).total_seconds() / 60)
        maxshift_node = (node.window[1] - arr_node).total_seconds() / 60
        self.route.append(node)
        self.wait.append(wait_node)
        self.arrival.append(arr_node)
        self.maxshift.append(maxshift_node)
        self.kms.append(dist_km(self.route[n-1].location, node.location))
        if node.get_type() == 0 :
            self.cap.append(self.cap[n-1] - node.number_of_meals)
        else:
            self.cap.append(self.cap[n-1] + node.number_of_meals)

    def update_vehicle(self, time_now):
        n = len(self.route)
        if n > 1:
            # find out which nodes have already been passed
            #temp = [idx for idx, element in enumerate(self.arrival) if element <= time_now]
            temp = []
            for i in range(len(self.route)):
                if self.arrival[i] <= time_now:
                    temp.append(i)
            drop = 0
            for i in temp:
                if self.route[i].get_time_window()[0] < time_now:
                    drop += 1
            for i in range(drop - 1):
                self.drop_node(0)
            if len(self.route) > 1:
                self.wait[1] = max((self.route[1].get_time_window()[0] - time_now).total_seconds() / 60,
                               self.wait[1])
            else:
                self.wait[0] = 0
            #Check how much time until empty
            m = len(self.route)
            if m>1:
                self.empty = (self.arrival[m-1]-time_now).total_seconds()/60
            else:
                self.empty = 0
        else:
            self.empty = 0
        self.last_update = time_now
        # self.wait[1] = (time_now-self.last_update).total_seconds()/60
        # self.wait[0] = max(0,self.wait[0]-round(temp.total_seconds()/60))


    def check_insertion(self, node, behind):
        """ Only call this function for pick up nodes!! """
        if self.cap[behind] >= node.number_of_meals:
            return True
        else:
            return False


    def find_best_position(self, n_pick, n_drop):
        # This function is given a vehicle and two nodes and calculates where to put them best
        if len(self.route) <= 1:
            bestroute = copy.deepcopy(self)
            bestroute.append_node(n_pick)
            bestroute.append_node(n_drop)

            earliest_arrival = bestroute.arrival[2]
            position = 2
        else:
            # First best position for pick up node
            # Check all route possibilities
            node = n_pick
            bestrouteval_pick = -10000
            for i in range(1, len(self.route)):
                tempv = copy.deepcopy(self)
                if self.check_insertion(node, i):
                    tempv.insert(node, i)
                    p = tempv.route_value()
                    if p > bestrouteval_pick:
                        bestrouteval_pick = p
                        earliest_arrival = tempv.arrival[i + 1]
                        bestroute_pick = tempv
                        behind = i
                    elif p == bestrouteval_pick:
                        if tempv.arrival[i + 1] < earliest_arrival:
                            earliest_arrival = tempv.arrival[i + 1]
                            bestroute_pick = tempv
                            behind = i
            # Now find drop position after pick_node
            if behind == len(bestroute_pick.route) - 1:
                bestroute_pick.append_node(n_drop)
            else:
                bestrouteval = -10000
                for j in range(behind + 1, len(bestroute_pick.route)):
                    tempv = copy.deepcopy(bestroute_pick)
                    tempv.insert(n_drop, j)
                    p = tempv.route_value()
                    if p > bestrouteval:
                        bestrouteval = p
                        earliest_arrival = tempv.arrival[j + 1]
                        bestroute = tempv
                        position = j
                    elif p == bestrouteval:
                        if tempv.arrival[j + 1] < earliest_arrival:
                            earliest_arrival = tempv.arrival[j + 1]
                            bestroute = tempv
                            position = j
        solution = {'Route': bestroute, 'Arrival': earliest_arrival, 'position in queue': position, 'cap':self.cap}
        return solution

    def insert(self, node, behind):
        # insert node behind index "behind"
        #n_pick = node
        i = behind
        #Update distance
        arr_node = max(self.arrival[i] + timedelta(minutes=self.wait[i]),
                       self.last_update) + timedelta(minutes=dist(self.route[i], node))
        wait_node = max(0, (node.get_time_window()[0] - arr_node).total_seconds() / 60)
        if node.get_type() == 0:
            cap_node = self.cap[behind] - node.number_of_meals
        else:
            cap_node = self.cap[behind] + node.number_of_meals

        if i < len(self.route) - 1:
            # update nodes after insertion
            shift = dist(self.route[i], node) + wait_node + dist(self.route[i + 1], node) - dist(self.route[i],
                                                                                                 self.route[i + 1])
            for j in range(i + 1, len(self.route)):
                self.wait[j] = max(0, self.wait[j] - shift)
                self.arrival[j] = self.arrival[j] + timedelta(minutes=shift)
                shift = max(0, shift - self.wait[j])
                self.maxshift[j] = self.maxshift[j] - shift
                if node.get_type() == 0:
                    self.cap[j] -= node.number_of_meals
                else:
                    self.cap[j] += node.number_of_meals

            # update insertion node
            maxshift_node = (node.get_time_window()[1] - arr_node).total_seconds() / 60
            self.kms[i] = dist_km(self.route[i].location, node.location)
            # insert node
            self.kms.insert(i + 1, dist_km(node.location, self.route[i+1].location))
            self.arrival.insert(i + 1, arr_node)
            self.wait.insert(i + 1, wait_node)
            self.maxshift.insert(i + 1, maxshift_node)
            self.route.insert(i + 1, node)
            self.cap.insert(i+1, cap_node)

            # and nodes before insertion
            for l in range(i, -1, -1):
                self.maxshift[l] = (self.route[l].get_time_window()[1] - self.arrival[l]).total_seconds() / 60
        else:
            self.append_node(node)


    def route_value(self):
        delay = [x for x in self.maxshift if x < 0]
        p = sum(delay) / 10
        return p

    def route_value_km(self):
        return sum(self.kms)


def assign_order(n_pick, n_drop, order_time, mode = 'time'):
    region = n_pick.order.get_region()
    region_fleet = regions[region].get_vehicles()
    for i in region_fleet:
        i.update_vehicle(order_time)
    assign = find_best_vehicle(n_pick, n_drop, region_fleet, mode)
    # Information will be returned to GUI
    region_fleet[assign['Vehicle_id']] = assign['Vehicle_info']['Route']
    region_fleet[assign['Vehicle_id']].update_vehicle(order_time)
    #print(assign['Vehicle_info']['cap'])
    print('Order ', n_drop.order.id, 'in Region ', region ,' was assigned to vehicle number', assign['Vehicle_id'], '. Estimated arrival time at Customer is',
          assign['Vehicle_info']['Arrival'], 'and there are', assign['Vehicle_info']['position in queue'],
          'stations before.')
    return region_fleet


def find_best_vehicle(n_pick, n_drop, region_fleet, mode):
    if mode == 'time':
        bestrouteval = -10000
        for i in range(len(region_fleet)):
            time_available = (region_fleet[i].get_shift_end() - n_pick.order.time + timedelta(minutes = region_fleet[i].get_empty())).total_seconds()/60
            if time_available > 15: #Only consider vehicle if it would otherwise be empty for the last 15 minutes of shift
                current = region_fleet[i].find_best_position(n_pick, n_drop)
                rv = current['Route'].route_value()
                if rv > bestrouteval:
                    vehicle_info = current
                    bestrouteval = rv
                    vehicle_id = i
                elif rv == bestrouteval:
                    if current['Arrival'] < vehicle_info['Arrival']:
                        vehicle_info = current
                        bestrouteval = rv
                        vehicle_id = i
    else:
        bestrouteval = 10000
        for i in range(len(region_fleet)):
            current = region_fleet[i].find_best_position(n_pick, n_drop)
            rv = current['Route'].route_value()
            if rv < bestrouteval:
                vehicle_info = current
                bestrouteval = rv
                vehicle_id = i
            elif rv == bestrouteval:
                if current['Arrival'] < vehicle_info['Arrival']:
                    vehicle_info = current
                    bestrouteval = rv
                    vehicle_id = i
    solution = {'Vehicle_info': vehicle_info, 'Vehicle_id': vehicle_id}
    return solution
