import numpy as np
import datetime
from classes.restaurant_order import *


class Route_node2:
    # Missing: assign region to node
    def __init__(self, order, type_):
        self.type_ = type_
        self.order_id = order.id

        # pick up node
        if type_ == 0:
            self.location = restaurants[order.restaurant].node
            self.window = (order.window[0], order.window[0] + timedelta(0, 120*60))

        # drop off node
        elif type_ == 1:
            self.location = order.node
            self.window = order.window

        self.number_of_meals = order.amount  # Either to be picked up or dropped off, depending on type
        self.time = order.time

    def set_type(self, type_):
        self.type_ = type_

    def set_location(self, index):
        self.location = index

    def set_number_of_meals(self, meals):
        self.number_of_meals = meals

    def set_time_window(self, opening, closing):
        self.window = [opening, closing]

    def get_type(self):
        return self.type_

    def get_location(self):
        return self.location

    def get_number_of_meals(self):
        return self.number_of_meals

    def get_time_window(self):
        return self.window



class Route_node:
    # Missing: assign region to node
    def __init__(self, location, number_of_meals, time, order_id = None):
        self.type_ = np.NaN
        self.order_id  = order_id
        self.location = location
        self.window = [0, 0]
        self.number_of_meals = number_of_meals  # Either to be picked up or dropped off, depending on type
        self.time = time

    def set_type(self, type_):
        self.type_ = type_

    def set_location(self, index):
        self.location = index

    def set_number_of_meals(self, meals):
        self.number_of_meals = meals

    def set_time_window(self, opening, closing):
        self.window = [opening, closing]

    def get_type(self):
        return self.type_

    def get_location(self):
        return self.location

    def get_number_of_meals(self):
        return self.number_of_meals

    def get_time_window(self):
        return self.window
