"""
This file should handle the vehicle fleet. This includes:
- Initializing new vehicles when the start shift (vehicle object). It is assumed that the vehicle is at the depot of the region at the time when the shift starts.
- Add new vehicle to fleet of corresponding region (every region has a list of its vehicles currently available)
- The attribute when a vehicle stops working still has to be added to the object and the algorithm
"""
from pprint import pprint
from datetime import datetime, timedelta
from classes.region import *
from classes.vehicle import Vehicle
from classes.route_node import *


#Shift start
#t = datetime.datetime.now()
t = datetime.now()
t = t.replace(hour = 14)
t = t.replace(minute = 0)
t = t.replace(second = 0)
t = t.replace(microsecond = 0)




for i in range(1, 8):
    fleet = []
    for j in range(50):
        fleet.append(Vehicle(i, t,1))
    regions[i].set_vehicles(fleet)