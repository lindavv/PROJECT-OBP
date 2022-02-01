#<<<<<<< Updated upstream
orders = {}
#=======

from algorithm.handle_vehiclefleet import *
from classes.vehicle import assign_order
import pandas as pd

root = os.getcwd() + '/data/orders/orders_21-01-0'+ str(7) + '.csv'
orders_df = pd.read_csv(root, sep=' ', index_col = 0)
orders_df['order_time'] = pd.to_datetime(orders_df['order_time'])

#row = orders_df.loc[0]
def read_df_of_day(date):
    """We can read in the corresponding weekday of date in the first februar week 2021"""
    weekd = date.weekday()
    #2021-02-01 is a monday, and weekd = 0 if date is also a monday
    root = os.getcwd() + '/data/orders/orders_21-02-0' + str(1+weekd) + '.csv'
    orders_df = pd.read_csv(root, sep=' ', index_col=0)
    orders_df['order_time'] = pd.to_datetime(orders_df['order_time'])
    return orders_df




def create_orders(orders, df_index,orders_df):
    row = orders_df.loc[df_index]
    ord = []
    for food in row[3:].to_frame().itertuples():
        if food[1] > 0:
            id = len(orders)
            order = Order(id, food[1], food[0][:-7], row.copy())
            orders[id] = order
            ord.append(order)
    return orders


orders = {}

def create_orders_testing(df_index,orders_df):
    row = orders_df.loc[df_index]
    ord = []
    for food in row[3:].to_frame().itertuples():
        if food[1] > 0:
            id = len(orders)
            order = Order(id, food[1], food[0][:-7], row.copy())
            orders[id] = order
            ord.append(order)
    return ord

def order_to_node(order):
    # make nodes
    pick = Route_node(restaurants[order.restaurant].node, order.amount, order.time, order)
    drop = Route_node(order.node, order.amount, order.time, order)
    pick.set_time_window(order.window[0], order.window[0]+timedelta(0, 120*60))
    drop.set_time_window(order.window[0], order.window[1])
    pick.set_type(0)
    drop.set_type(1)
    return pick, drop

def dummy_simulation():
    orders = {}
    pick_up_nodes, drop_off_nodes = [], []

    number = 4
    #date = datetime.now().date()
    #orders_df = read_df_of_day(date)
    for i in range(number):
        orders = create_orders(orders, i,orders_df)

    for i in range(len(orders)):
        pick, drop = order_to_node(orders[i])
        pick_up_nodes.append(pick)
        drop_off_nodes.append(drop)
        # print(pick.order.time)
        # print('----------------------------------------------------------------------------------------------------------')
        print('Order', i, 'was placed from location ', orders[i].node, ' which lies in region ', orders[i].region,
              ' at ',
              orders[i].time, ' and contains ', orders[i].amount, ' meals of type ', orders[i].food_type,
              '. It was assigned to restaurant nr. ', orders[i].restaurant, ' and is expected to be ready at ',
              orders[i].window[0])
        assign_order(pick, drop, orders[i].time, mode='time')

def dummy2(j):
    orders = {}
    pick_up_nodes, drop_off_nodes = [], []


    # date = datetime.now().date()
    # orders_df = read_df_of_day(date)

    #orders = create_orders(orders, i, orders_df)

    for i in range(len(orders)):
        pick, drop = order_to_node(orders[i])
        pick_up_nodes.append(pick)
        drop_off_nodes.append(drop)
        # print(pick.order.time)
        # print('----------------------------------------------------------------------------------------------------------')
        print('Order', i, 'was placed from location ', orders[i].node, ' which lies in region ', orders[i].region,
              ' at ',
              orders[i].time, ' and contains ', orders[i].amount, ' meals of type ', orders[i].food_type,
              '. It was assigned to restaurant nr. ', orders[i].restaurant, ' and is expected to be ready at ',
              orders[i].window[0])
        assign_order(pick, drop, orders[i].time, mode='time')

#print('----------------------------------------------------------------------------------------------------------')
#print('Check out vehicle 2 of region 1, to see how the order is handled in the vehicle')
#pprint(vars(regions[1].get_vehicles()[2]))
#print('Finally see the performance measures of region 6')
#print(regions[6].get_evaluation())
"""Mode can either be time or cost, depending on optimization focus"""

















#>>>>>>> Stashed changes
