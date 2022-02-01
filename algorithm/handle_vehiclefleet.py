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

def read_shifts(day, weekd):
    Shift1_str = [shifts_df[weekd]['1s'], shifts_df[weekd]['1e']]
    Shift2_str = [shifts_df[weekd]['2s'], shifts_df[weekd]['2e']]
    start1 = datetime.strptime(str(day) + ' ' + Shift1_str[0], '%Y-%m-%d %H:%M:%S')
    start2 = datetime.strptime(str(day) + ' ' + Shift2_str[0], '%Y-%m-%d %H:%M:%S')
    end1 = datetime.strptime(str(day) + ' ' + Shift1_str[1], '%Y-%m-%d %H:%M:%S')
    end2 = datetime.strptime(str(day) + ' ' + Shift2_str[1], '%Y-%m-%d %H:%M:%S')
    return [start1, end1], [start2, end2]




def read_vehicleamount(day, region, focus):
    ans = [0,0]
    if focus == 'mintime':
       ans[0] = mintime_S1_df[day][region]
       ans[1] = mintime_S2_df[day][region]
    elif focus == 'minvehicle':
        ans[0] = minveh_S1_df[day][region]
        ans[1] = minveh_S2_df[day][region]
    return ans

def initialize_vehicles(day, mode = 'minvehicle'):
    """Needs day as timestamp"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekd = day.weekday() #returns integer of weekday 0-6 Mon-Sun
    Shift1, Shift2 = read_shifts(day, days[weekd])
    for i in range(1, 8):
        fleet = []
        amount = read_vehicleamount(days[weekd], i, mode)
        for j in range(amount[0]):
            fleet.append(Vehicle(i, 1, Shift1[0], Shift1[1]))
        for j in range(int(amount[1])-int(amount[0])):
            fleet.append(Vehicle(i, 2, Shift2[0], Shift2[1]))
        regions[i].set_vehicles(fleet)


date = datetime.now().date()
initialize_vehicles(date)
#print(regions[1].get_vehicles())
#print(datetime.now().date())

def change_vehicle_number(region, amount, shift, time_now):
    """
    Amount should either be 1 or -1
    shift is either 1 or 2, depending on the shift we want to change the vehicles in
    time_now is a timestamp of now (incl. day)
    """
    #Read in shifts
    day = time_now.date()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekd = day.weekday() #returns integer of weekday 0-6 Mon-Sun
    Shift1, Shift2 = read_shifts(day, days[weekd])
    if shift == 1:
        #Shift start, either the real start of the shift, or 15 minutes from now (if decision is made during the shift), bc driver needs time to get to depot
        shift_start = max(time_now + timedelta(minutes = 15),Shift1[0])
        shift_end = Shift1[1]
        if amount == 1:
            regions[region].get_vehicles().append(Vehicle(region, shift, shift_start,shift_end))
        elif amount == -1:
            drop_vehicle(region,shift, time_now)
        else:
            print('Amount not valid')
    else:
        shift_start = max(time_now + timedelta(minutes = 15),Shift2[0])
        shift_end = Shift2[1]
        if amount == 1:
            regions[region].get_vehicles().append(Vehicle(region, shift, shift_start,shift_end))
        elif amount == -1:
            drop_vehicle(region, shift, time_now)
        else:
            print('Amount not valid')


def drop_vehicle(region, shift, time_now):
    empty = []              #tracks minutes until vehicles of given shift are empty
    idx = []
    for i in range(len(regions[region].get_vehicles())):
        regions[region].get_vehicles()[i].update_vehicle(time_now)
        if regions[region].get_vehicles()[i].get_shift() == shift:
            idx.append(i)
            empty.append(regions[region].get_vehicles()[i].get_empty())
    minval = min(empty)
    dropidx = empty.index(minval)
    shift_end = time_now + timedelta(minutes = minval)
    regions[region].get_vehicles()[idx[dropidx]].set_shift_end(shift_end)
#for i in range(1, 8):
#    fleet = []
#    for j in range(50):
#        fleet.append(Vehicle(i, t,1))
#    regions[i].set_vehicles(fleet)