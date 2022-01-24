#import time
import copy
from datetime import datetime, timedelta
from stuff.map_dfs import dist
from classes.route_node import *

""" Needs Shift start and region as input argument when initialized. That is an object of datetime which states the starting time of this vehicle."""






class Vehicle:

    def __init__(self, region, shift_start, max_cap = 20):

        self.region = region  # polygon object of shapely package
        # dynamically get position
        self.last_update = shift_start  # timestamp when last route was decided
        # self.next_destination                         # next node and time when this node is reached
        self.route = [self.set_depot(region, shift_start)]
        self.wait = [0]
        self.arrival = [shift_start]
        self.maxshift = [180]


        # self.time_busy

        self.kms = 0
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

    def set_depot(self, region, shift_start):
        depot = Route_node(0, 0, 0)
        depot.set_location(region.depot)
        depot.set_time_window(shift_start, shift_start + timedelta(hours=4))
        return depot

    def drop_node(self, idx):
        if self.route[idx].type_ == 1:
            ord = self.route[idx].order
            ord.calc_waiting_time(self.arrival[idx])
        del self.route[idx]
        del self.wait[idx]
        del self.arrival[idx]
        del self.maxshift[idx]
        del self.cap[idx]

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
        if node.get_type() == 0 :
            self.cap.append(self.cap[n-1] - node.number_of_meals)
        else:
            self.cap.append(self.cap[n-1] + node.number_of_meals)

    def update_vehicle(self, time_now):
        if len(self.route) > 1:
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
            self.append_node(n_pick)
            self.append_node(n_drop)
            bestroute = copy.deepcopy(self)
            earliest_arrival = bestroute.arrival[2]
            position = 2
        else:
            # First best position for pick up node
            # Check all route possibilities
            node = n_pick
            bestrouteval_pick = -1000
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
                bestrouteval = -1000
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
            # insert node
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


def assign_order(n_pick, n_drop, region_fleet, order_time):
    for i in region_fleet:
        i.update_vehicle(order_time)
    assign = find_best_vehicle(n_pick, n_drop, region_fleet)
    # Information will be returned to GUI
    region_fleet[assign['Vehicle_id']] = assign['Vehicle_info']['Route']
    #print(assign['Vehicle_info']['cap'])
    print('Order was assigned to vehicle number', assign['Vehicle_id'], '. Estimated arrival time at Customer is',
          assign['Vehicle_info']['Arrival'], 'and there are', assign['Vehicle_info']['position in queue'],
          'stations before.')
    return region_fleet


def find_best_vehicle(n_pick, n_drop, region_fleet):
    # get region specific fleet #Missing
    bestrouteval = -1000
    for i in range(len(region_fleet)):
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
    solution = {'Vehicle_info': vehicle_info, 'Vehicle_id': vehicle_id}
    return solution
