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

    def find_depot(self):
      lat = list(self.poly.centroid.coords)[0][0]
      lon = list(self.poly.centroid.coords)[0][1]
      return assign_loc(lat,lon,paris_nodes)

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