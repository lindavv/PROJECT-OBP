import time

from algorithm.handle_vehiclefleet import initialize_vehicles
from algorithm.tracking_orders import create_orders, orders, order_to_node
from classes.region import regions
from classes.vehicle import assign_order
from datetime import datetime, timedelta
import os
import pandas as pd
import numpy as np
from pprint import pprint


#pick_up_nodes, drop_off_nodes = [], []


def read_df_of_day2(date):
    """We can read in the corresponding weekday of date in the first februar week 2021"""
    weekd = date.weekday()
    #2021-02-01 is a monday, and weekd = 0 if date is also a monday
    root = os.getcwd() + '/data/orders/orders_21-02-0' + str(1+weekd) + '.csv'
    orders_df = pd.read_csv(root, sep=' ', index_col=0)
    orders_df['order_time'] = pd.to_datetime(orders_df['order_time'])
    return orders_df


start = time.perf_counter()
date = datetime.now().date()
orders_df = read_df_of_day2(date)
number = 20#len(orders_df)
for i in range(len(orders_df)-50,len(orders_df)):
    create_orders(i,orders_df)
print('Time for creation of orders: ', (time.perf_counter()-start)/60)


results = np.zeros((6,64))
modes = ['time','cost','mix']
initialize_vehicles(date, 'minvehicle')
for j in range(3):
    print('Analysis of minvehicles and routing optimizer '+modes[j])
    for i in range(len(orders)):
        pick, drop = order_to_node(orders[i])
        #print('----------------------------------------------------------------------------------------------------------')
        #print('Order', i, 'was placed from location ', orders[i].node, ' which lies in region ', orders[i].region, ' at ',
        #      orders[i].time, ' and contains ', orders[i].amount, ' meals of type ', orders[i].food_type,
        #      '. It was assigned to restaurant nr. ', orders[i].restaurant, ' and is expected to be ready at ',
        #      orders[i].window[0])
        assign_order(pick, drop, orders[i].time, mode=modes[j])
    for r in range(1,8):
        #update region info
        results[j, 0 + 8 * (r - 1)] = regions[r].get_evaluation()['Orders delivered']
        results[j, 1 + 8 * (r - 1)] = regions[r].get_evaluation()['Num_delayed_orders']
        results[j, 2 + 8 * (r - 1)] = regions[r].get_evaluation()['Percentage delayed orders']
        results[j, 3 + 8 * (r - 1)] = regions[r].get_evaluation()['Total delay time']
        results[j, 4 + 8 * (r - 1)] = regions[r].get_evaluation()['Avg. delay']
        results[j, 5 + 8 * (r - 1)] = regions[r].get_evaluation()['Total waiting time']
        results[j, 6 + 8 * (r - 1)] = regions[r].get_evaluation()['Avg. waiting time']
        results[j, 7 + 8 * (r - 1)] = regions[r].get_evaluation()['kms driven']
        #Add to whole Paris
        results[j, 56] += regions[r].get_evaluation()['Orders delivered']
        results[j, 57] += regions[r].get_evaluation()['Num_delayed_orders']
        results[j, 58] += regions[r].get_evaluation()['Percentage delayed orders']
        results[j, 59] += regions[r].get_evaluation()['Total delay time']
        results[j, 60] += regions[r].get_evaluation()['Avg. delay']
        results[j, 61] += regions[r].get_evaluation()['Total waiting time']
        results[j, 62] += regions[r].get_evaluation()['Avg. waiting time']
        results[j, 63] += regions[r].get_evaluation()['kms driven']

initialize_vehicles(date, 'mintime')
for j in range(3):
    print('Analysis of minvehicles and routing optimizer ' + modes[j])
    for i in range(len(orders)):
        pick, drop = order_to_node(orders[i])
        #print('----------------------------------------------------------------------------------------------------------')
        #print('Order', i, 'was placed from location ', orders[i].node, ' which lies in region ', orders[i].region, ' at ',
        #      orders[i].time, ' and contains ', orders[i].amount, ' meals of type ', orders[i].food_type,
        #      '. It was assigned to restaurant nr. ', orders[i].restaurant, ' and is expected to be ready at ',
        #      orders[i].window[0])
        assign_order(pick, drop, orders[i].time, mode=modes[j])
    for r in range(1,8):
        #update region info
        results[j+3, 0 + 8 * (r - 1)] = regions[r].get_evaluation()['Orders delivered']
        results[j+3, 1 + 8 * (r - 1)] = regions[r].get_evaluation()['Num_delayed_orders']
        results[j+3, 2 + 8 * (r - 1)] = regions[r].get_evaluation()['Percentage delayed orders']
        results[j+3, 3 + 8 * (r - 1)] = regions[r].get_evaluation()['Total delay time']
        results[j+3, 4 + 8 * (r - 1)] = regions[r].get_evaluation()['Avg. delay']
        results[j+3, 5 + 8 * (r - 1)] = regions[r].get_evaluation()['Total waiting time']
        results[j+3, 6 + 8 * (r - 1)] = regions[r].get_evaluation()['Avg. waiting time']
        results[j+3, 7 + 8 * (r - 1)] = regions[r].get_evaluation()['kms driven']
        #Add to whole Paris
        results[j+3, 56] += regions[r].get_evaluation()['Orders delivered']
        results[j+3, 57] += regions[r].get_evaluation()['Num_delayed_orders']
        results[j+3, 58] += regions[r].get_evaluation()['Percentage delayed orders']
        results[j+3, 59] += regions[r].get_evaluation()['Total delay time']
        results[j+3, 60] += regions[r].get_evaluation()['Avg. delay']
        results[j+3, 61] += regions[r].get_evaluation()['Total waiting time']
        results[j+3, 62] += regions[r].get_evaluation()['Avg. waiting time']
        results[j+3, 63] += regions[r].get_evaluation()['kms driven']
df = pd.DataFrame(data = results, index = ["minveh_time", "minveh_cost", "minveh_mix","mintime_time", "mintime_cost", "mintime_mix"], columns=['Orders delivered_R1', 'Num_delayed_orders_R1', 'Percentage delayed orders_R1',
                           'Total delay time_R1', 'Avg. delay_R1','Total waiting time_R1', 'Avg. waiting time_R1', 'kms driven_R1','Orders delivered_R2', 'Num_delayed_orders_R2', 'Percentage delayed orders_R2',
                           'Total delay time_R2', 'Avg. delay_R2','Total waiting time_R2', 'Avg. waiting time_R2', 'kms driven_R2','Orders delivered_R3', 'Num_delayed_orders_R3', 'Percentage delayed orders_R3',
                           'Total delay time_R3', 'Avg. delay_R3','Total waiting time_R3', 'Avg. waiting time_R3', 'kms driven_R3','Orders delivered_R4', 'Num_delayed_orders_R4', 'Percentage delayed orders_R4',
                           'Total delay time_R4', 'Avg. delay_R4','Total waiting time_R4', 'Avg. waiting time_R4', 'kms driven_R4','Orders delivered_R5', 'Num_delayed_orders_R5', 'Percentage delayed orders_R5',
                           'Total delay time_R5', 'Avg. delay_R5','Total waiting time_R5', 'Avg. waiting time_R5', 'kms driven_R5','Orders delivered_R6', 'Num_delayed_orders_R6', 'Percentage delayed orders_R6',
                           'Total delay time_R6', 'Avg. delay_R6','Total waiting time_R6', 'Avg. waiting time_R6', 'kms driven_R6','Orders delivered_R7', 'Num_delayed_orders_R7', 'Percentage delayed orders_R7',
                           'Total delay time_R7', 'Avg. delay_R7','Total waiting time_R7', 'Avg. waiting time_R7', 'kms driven_R7','Orders delivered_Paris', 'Num_delayed_orders_Paris', 'Percentage delayed orders_Paris',
                           'Total delay time_Paris', 'Avg. delay_Paris','Total waiting time_Paris', 'Avg. waiting time_Paris', 'kms driven_Paris'])

path = os.getcwd() + '/data/Output/result.csv'
df.to_csv(path)
