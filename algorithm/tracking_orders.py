#<<<<<<< Updated upstream
orders = {}
#=======
import pandas as pd
from classes.restaurant_order import Order, Restaurant, restaurants
import os
from stuff.map_dfs import g
import networkx as nx
from classes.route_node import *
from classes.region import *
from algorithm.handle_vehiclefleet import *
from datetime import datetime, timedelta


root = os.getcwd() + '/data/orders/orders_21-01-0'+ str(7) + '.csv'
orders_df = pd.read_csv(root, sep=' ', index_col = 0)
orders_df['order_time'] = pd.to_datetime(orders_df['order_time'])

row = orders_df.loc[0]


def create_orders(df_index):
    row = orders_df.loc[df_index]
    for food in row[3:].to_frame().itertuples():
        if food[1] > 0:
            id = len(orders)
            order = Order(id, food[1], food[0][:-7], row.copy())
            orders[id] = order



orders = {}


def order_to_node2(order):
    # make nodes
    pick = Route_node2(order, 0)
    drop = Route_node2(order, 1)

    return pick, drop

def order_to_node(order):
    # make nodes
    pick = Route_node(restaurants[order.restaurant].node, order.amount, order.time, order)
    drop = Route_node(order.node, order.amount, order.time, order)
    pick.set_time_window(order.window[0], order.window[0]+timedelta(0, 120*60))
    drop.set_time_window(order.window[0], order.window[1])
    pick.set_type(0)
    drop.set_type(1)

    return pick, drop





pick_up_nodes, drop_off_nodes = [], []

number = 100

for i in range(number):
    create_orders(i)

for i in range(len(orders)):
    pick, drop = order_to_node(orders[i])
    pick_up_nodes.append(pick)
    drop_off_nodes.append(drop)

    assign_order(pick, drop, regions[orders[i].region].get_vehicles(), orders[i].time)


veh = regions[4].get_vehicles()[0]
pprint(vars(veh))



#print(dist(veh.route[1], veh.route[2]))















#>>>>>>> Stashed changes
