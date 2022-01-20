from datetime import datetime, timedelta
import math
from collections import Counter
from collections import namedtuple
from stuff.map_dfs import *
from classes.region import regions
import networkx as nx
import numpy as np


Node = namedtuple("node", ["lat", "lon"])
Edge = namedtuple("edge", ["start", "end", "directions", "time", "distance"])


class Restaurant:

    def __init__(self, ID):
        # general info
        self.ID = ID
        self.data = rests_df.loc[self.ID].copy()  # copy dataframe row for ease
        self.finished = {'full': [], 'partial': []}  # list of finished orders (full or partial orders)
        self.node = self.data['node']

        # initialize food dictionaries
        self.get_food_type_data()

        # initialize opening and closing hours
        self.opening_hours()

    def check_availability(self, order, orders):
        """
        This function takes an order and determines when the order would be finished in this restaurant.
        Returned: finish time of order (or 'False' when restaurant is closed or when it cannot be finished on time)

        The order is not added to the queue, just the finish time is calculated

        The current queue of orders that the restaurant has already accepted is taken into account!
        Opening and closing hours of restaurants also taken into account!
        """

        self.update_queue(order.time, orders)

        foodtype = order.food_type


        duration = int(self.foods[foodtype]['time'])
        cap = int(self.foods[foodtype]['cap'])

        queue = self.queue[foodtype][-cap:]  # consider the final few items in the queue
        Q = len(queue)
        spots = cap - Q  # spots that can be filled in queue, in case there is more capacity

        # how many sequences of preparation blocks (e.g. when 7 items are ordered and capacity is 2, we need 4 blocks(=sequences) of preparation)
        blocks = math.ceil(order.amount / cap)
        rest = order.amount % cap

        preparation_time = int(60 * blocks * duration)

        day = order.time.weekday()
        opening_time = self.hours[day][0]

        # in case the restaurant is closed
        if opening_time == 0:
            return False

        # in case restaurant is open
        else:

            # order can start no earlier than both order time and restaurant opening time
            # start_time below is the minimal starting time of the order
            if order.time.hour <= opening_time:
                start_time = order.time.replace(hour=opening_time, minute=0, second=0)
            else:
                start_time = order.time

            # deal with queue and see if start_time is later because of it
            if rest == 0:
                try:
                    start_time = queue[-1][2]
                except:
                    pass
            elif rest > spots:
                start_time = queue[-cap - 1 + rest][2]

            # time the order would be finished
            finish_time = start_time + timedelta(0, preparation_time)

            # consider case where the order is done after midnight...
            if finish_time.hour < 4:
                hour_done = finish_time.hour + 24
            else:
                hour_done = finish_time.hour

            # return finish time in case it is done before closing hour
            if hour_done >= self.hours[day][1]:
                return False
            else:
                return finish_time

    def plan_order(self, order):
        """
        Add order to the queue

        TODO: change order.finish_time when done
        """
        foodtype = order.food_type
        duration = self.foods[foodtype]['time']
        cap = self.foods[foodtype]['cap']

        queue = self.queue[foodtype][-cap:]  # consider the final few items in the queue
        Q = len(queue)
        spots = cap - Q  # spots that can be filled in queue, in case there is more capacity
        n = order.amount

        day = order.time.weekday()
        opening_time = self.hours[day][0]

        # order can start no earlier than both order time and restaurant opening time
        # start_time below is the minimal starting time of the order
        if order.time.hour <= opening_time:
            start_time = order.time.replace(hour=opening_time, minute=0, second=0)
        else:
            start_time = order.time

        # for orders that can immediately be started (the queue has still some capacity left)
        for i in range(spots):
            finish_time = start_time + timedelta(0, int(60 * duration))

            item = (order.id, n, finish_time)
            self.queue[foodtype].append(item)

        # for when a queue is full (meaning it covers whole capacity)
        for i in range(n - spots):
            queue = self.queue[foodtype][-cap:]
            finish_time = queue[0][2] + timedelta(0, int(60 * duration))

            item = (order.id, n, finish_time)
            self.queue[foodtype].append(item)

        # TODO: edit the order object so that its finished time is included

    def update_queue(self, dt, orders):
        # look at queue, move food that is done preparing to finished['partial']
        # when full order is complete, move to finished['full']

        t = dt.time()

        # check which foods have been prepared
        for food in self.foods.keys():
            queue = self.queue[food].copy()

            for item in queue:
                if item[2].time() < t:
                    self.finished['partial'].append(item)
                    self.queue[food].remove(item)

        # check which orders are fully completed
        partial = []
        for order in self.finished['partial']:
            partial.append((order[0], order[1]))
        partial = Counter(partial)  # make counter to see if amount done matches amount ordered

        # add order object to finished['full'] list if all parts are completed
        for item in partial:
            if partial[item] == item[1]:  # if the number prepared of this order is the total amount ordered
                self.finished['full'].append(orders[item[0]])

        # if an order is fully completed, remove from partially completed list
        partial = self.finished['partial'].copy()
        for order in self.finished['full']:
            for item in partial:
                if order.id == item[0]:
                    self.finished['partial'].remove(item)

    def pick_up_order(self, order):
        # order is picked up by truck and removed from finished orders list
        pass

    def finish_day(self):
        # empty all order lists
        pass

    def opening_hours(self):
        """
        When creating restaurant objects, create dictionary with their opening and closing hours
        """
        self.hours = {}
        for i in range(7):
            self.hours[i] = (int(self.data[37 + (2 * i)][:2]), int(self.data[38 + (2 * i)][:2]))

            # adjust closing hours in case restaurant closes at 00:00 or later
            if self.hours[i][1] < 4:
                self.hours[i] = (self.hours[i][0], self.hours[i][1] + 24)

    def get_food_type_data(self):
        """
        When construction a restaurant object, get foods dictionary with food types as key,
        Each food item itself is dictionary with capacity and production time
        """
        self.foods = {}
        for col in self.data[3:37].to_frame().itertuples():
            if 'parallel' in col[0] and col[1] > 0:
                self.foods[col[0][:-9]] = {'cap': col[1]}
                self.foods[col[0][:-9]]['time'] = self.data[col[0][:-9] + '_production_minutes']

        self.queue = {}
        for key in self.foods.keys():
            self.queue[key] = []


restaurants = {}
for i in range(42):
    restaurants[i] = Restaurant(i)

class Order:
    """ First draft for order class, just to test restaurant functions """

    def __init__(self, ID, amount, food_type, data):
        self.id = ID
        self.food_type = food_type
        self.amount = amount
        self.data = data
        self.node = assign_loc(self.data['lat'], self.data['lon'], paris_nodes)
        self.time = data['order_time']

        self.set_region()

        # these can be updated when the order is done
        self.time_prepared = False
        self.time_delivered = False

    def set_region(self):
        self.region = 0
        for region in regions.keys():
            if regions[region].poly.contains(Point(self.data['lat'], self.data['lon'])):
                self.region = region

    def choose_restaurant(self, orders):
        options_t, options_i = [], []

        for rest in restaurants:
            r = restaurants[rest]

            # only consider restaurants that offer this foodtype
            if self.food_type in r.foods.keys():

                # check opening hours and when the order would be done preparing
                if r.check_availability(self, orders):
                    # store restaurant ID
                    options_i.append(r.ID)

                    # order would be done preparing after...
                    preparation_time = pd.to_datetime(r.check_availability(self, orders))

                    # duration of shortest path to restaurant....
                    lower_bound_delivery = int(self.restaurant_path(r))

                    # add lower bound to restaurant options list
                    options_t.append(preparation_time + timedelta(0, lower_bound_delivery))

        # ID of restaurant with lowest lower bound for delivery
        best_option = options_i[np.argmin(np.array(options_t))]

        return best_option



    def restaurant_path(self, restaurant):
        duration = nx.algorithms.shortest_path_length(g, self.node, restaurant.node, weight="time")

        return duration

