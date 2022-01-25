import pandas as pd
import os
from pprint import pprint
from stuff.test_data_vrp import *
from classes.vehicle import *
from classes.region import *
from algorithm.handle_vehiclefleet import *


#pprint(vars(regions[7].get_vehicles()[0]))
sol = assign_order(pick1,drop1,regions[7].get_vehicles(),time_now1)
print(sol)