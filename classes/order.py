from stuff.map_dfs import *
from classes.region import regions
from classes.restaurant import *

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


