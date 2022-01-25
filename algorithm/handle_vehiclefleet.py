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

#read in shifts
path = os.getcwd()
pd.read_csv(path + '/data/restaurants.csv', delimiter = " ")
mintime_S1_df = pd.read_csv(path + '/data/Shifts/Mintime_Shift1.csv', sep=';', index_col = 0)
mintime_S2_df = pd.read_csv(path + '/data/Shifts/Mintime_Shift2.csv', sep=';', index_col = 0)
minveh_S1_df = pd.read_csv(path + '/data/Shifts/Minvehicle_Shift1.csv', sep=';', index_col = 0)
minveh_S2_df = pd.read_csv(path + '/data/Shifts/Minvehicle_Shift2.csv', sep=';', index_col = 0)
shifts_df = pd.read_csv(path + '/data/Shifts/Shifts.csv', sep=';', index_col = 0)

def read_shifts(day):
    Shift1 = [shifts_df[day]['1s'], shifts_df[day]['1e']]
    Shift2 = [shifts_df[day]['2s'], shifts_df[day]['2e']]
    return Shift1, Shift2




def read_vehicleamount(day, region, focus):
    ans = [0,0]
    if focus == 'mintime':
       ans[0] = mintime_S1_df[day][region]
       ans[1] = mintime_S2_df[day][region]
    elif focus == 'minvehicle':
        ans[0] = minveh_S1_df[day][region]
        ans[1] = minveh_S2_df[day][region]
    return ans

def initialize_vehicles(day):
    """Needs day as timestamp"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekd = day.weekday() #returns integer of weekday 0-6 Mon-Sun
    Shift1, Shift2 = read_shifts(days[weekd])
    start1 = datetime.strptime(str(day) + ' ' + Shift1[0], '%Y-%m-%d %H:%M:%S')
    start2 = datetime.strptime(str(day) + ' ' + Shift2[0], '%Y-%m-%d %H:%M:%S')
    end1 = datetime.strptime(str(day) + ' ' + Shift1[1], '%Y-%m-%d %H:%M:%S')
    end2 = datetime.strptime(str(day) + ' ' + Shift2[1], '%Y-%m-%d %H:%M:%S')
    for i in range(1, 8):
        fleet = []
        amount = read_vehicleamount(days[weekd], i, 'minvehicle')
        for j in range(amount[0]):
            fleet.append(Vehicle(i, start1, end1))
        for j in range(amount[1]):
            fleet.append(Vehicle(i,start2,end2))
        regions[i].set_vehicles(fleet)



#for i in range(1, 8):
#    fleet = []
#    for j in range(50):
#        fleet.append(Vehicle(i, t,1))
#    regions[i].set_vehicles(fleet)