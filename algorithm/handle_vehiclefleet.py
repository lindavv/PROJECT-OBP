"""
This file should handle the vehicle fleet. This includes:
- Initializing new vehicles when the start shift (vehicle object). It is assumed that the vehicle is at the depot of the region at the time when the shift starts.
- Add new vehicle to fleet of corresponding region (every region has a list of its vehicles currently available)
- The attribute when a vehicle stops working still has to be added to the object and the algorithm
"""
from pprint import pprint
import datetime
from classes.region import *
from classes.vehicle import *
from classes.route_node import *


#Shift start
t = datetime.datetime.now()
t = t.replace(hour = 17)
t = t.replace(minute = 0)
t = t.replace(second = 0)
t = t.replace(microsecond = 0)

fleet_lightgreen = []
for i in range(50):
    fleet_lightgreen.append(Vehicle(regions[7],t))

regions[7].set_vehicles(fleet_lightgreen)
pprint(vars(regions[7]))