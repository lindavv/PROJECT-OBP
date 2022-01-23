import numpy as np
import datetime


class Route_node:
    # Missing: assign region to node
    def __init__(self, location, number_of_meals, time):
        self.type_ = np.NaN
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
