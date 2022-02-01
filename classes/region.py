from stuff.map_dfs import rests_df
from stuff.map_dfs import paris_nodes
from stuff.map_dfs import assign_loc
from shapely.geometry import Point, Polygon
import os



class Region:

    def __init__(self, region, color):
        """ Provide polygon that defines this region """

        self.poly = region                          # polygon object of shapely package
        self.area = region.area * 111.139**2        # area in km2
        self.n_res = self.get_restaurants()         # number of restaurants
        self.color = color
        self.vehicles = []                          # Vehicle fleet of this region
        self.depot = self.find_depot()
        self.evaluation = {'Orders delivered':0, 'Num_delayed_orders':0, 'Percentage delayed orders':0,
                           'Total delay time':0, 'Avg. delay': 0,
                           'Total waiting time':0, 'Avg. waiting time':0,
                           'kms driven':0,
                           'Vehicles busy':0, 'Avg. time until free':0}
    """"
    The Evaluation system of a region can be described with the following parameters at every point in time:
    - Kms driven: How many kms were driven so far in that region. Like this also the costs can be calculated. For now only one vehicle type.
    - Percentage delayed orders
    - Avg. delay: Average minutes delay of all delayed orders
    - Vehicles busy: Number of vehicles currently loaded with orders
    - Avg. time until free: The time that the vehicles need on average to be empty again    
    """

    def get_restaurants(self):
        count = 0
        index = []
        for i in range(len(rests_df)):
            p = Point(rests_df['lat'][i], rests_df['lon'][i])
            if self.poly.contains(p):
                count+=1
                index.append(i)
        rest = {'n_rest':count,'index_rest':index}
        return rest

    def set_vehicles(self,vehicles):
      self.vehicles = vehicles

    def get_vehicles(self):
      return self.vehicles

    def get_evaluation(self):
        return self.evaluation

    def find_depot(self):
      lat = list(self.poly.centroid.coords)[0][0]
      lon = list(self.poly.centroid.coords)[0][1]
      return assign_loc(lat,lon,paris_nodes)

    def update_vehicle_summary(self):
        busy_num = 0
        busy_time = 0
        for v in self.vehicles:
            n = len(v.get_route())
            busy_time+= v.get_empty()
            if n>1:
                busy_num+=1
        self.evaluation['Vehicles busy'] = busy_num
        if busy_num >0:
            self.evaluation['Avg. time until free'] = busy_time/busy_num
        else:
            self.evaluation['Avg. time until free'] = 0

    def clear_evaluation(self):
        self.evaluation = {'Orders delivered':0, 'Num_delayed_orders':0, 'Percentage delayed orders':0,
                           'Total delay time':0, 'Avg. delay': 0,
                           'Total waiting time':0, 'Avg. waiting time':0,
                           'kms driven':0,
                           'Vehicles busy':0, 'Avg. time until free':0}



def update_region(region, type,kms,wait,delay):
    regions[region].evaluation['kms driven'] += kms
    regions[region].update_vehicle_summary()
    if type == 1: #drop-off node, so order is finished
        regions[region].evaluation['Orders delivered']+=1
        regions[region].evaluation['Total waiting time'] += wait
        regions[region].evaluation['Avg. waiting time'] = regions[region].evaluation['Total waiting time']/ regions[region].evaluation['Orders delivered']
        if delay>0: #If order was delivered with delay
            regions[region].evaluation['Num_delayed_orders'] += 1
            regions[region].evaluation['Total delay time'] += delay
            regions[region].evaluation['Percentage delayed orders'] = regions[region].evaluation['Num_delayed_orders']/regions[region].evaluation['Orders delivered']
            regions[region].evaluation['Avg. delay'] = regions[region].evaluation['Total delay time']/regions[region].evaluation['Num_delayed_orders']





def read_region(color):
    """
    Returns region polygon from coordinates of region text file
    """
    path = os.getcwd() + "/data/regions/region_" + color + ".txt"
    coords = []
    with open(path) as file:
        n_nodes = int(file.readline())
        for i in range(n_nodes):
            line = file.readline().split()
            coords.append(tuple((float(line[0]), float(line[1]))))

    region = Polygon(coords)

    return region


regions = {1: Region(read_region('orange'), 'orange'),
           2: Region(read_region('green'), 'green'),
           3: Region(read_region('blue'), 'blue'),
           4: Region(read_region('yellow'), 'yellow'),
           5: Region(read_region('pink'), 'pink'),
           6: Region(read_region('purple'), 'purple'),
           7: Region(read_region('lightgreen'), 'lightgreen')}