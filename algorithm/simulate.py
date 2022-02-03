"""
This file is called when simulating a day while running the DSS
 - dummy_simulation2() simulates receiving orders and assigning them to rest and vehicles

"""
from algorithm.handle_vehiclefleet import *
from classes.vehicle import assign_order
import pandas as pd

root = os.getcwd() + '/data/orders/orders_21-01-0'+ str(7) + '.csv'
orders_df = pd.read_csv(root, sep=' ', index_col = 0)
orders_df['order_time'] = pd.to_datetime(orders_df['order_time'])



def create_orders(orders, df_index, orders_df):
    row = orders_df.loc[df_index]
    n= 0

    # separate orders by food type
    for food in row[3:].to_frame().itertuples():
        if food[1] > 0:
            n+=1
            id = len(orders)
            order = Order(id, food[1], food[0][:-7], row.copy())
            orders[id] = order
    orders_df.drop([df_index])

    return orders, n


def order_to_node(order):
    """
    Given an order, create pick up (restaurant) node and drop off (customer) node
    """
    # make nodes
    pick = Route_node(restaurants[order.restaurant].node, order.amount, order.time, order)
    drop = Route_node(order.node, order.amount, order.time, order)
    pick.set_time_window(order.window[0], order.window[0]+timedelta(0, 120*60))
    drop.set_time_window(order.window[0], order.window[1])
    pick.set_type(0)
    drop.set_type(1)

    return pick, drop




def dummy_simulation2(orders, number, rownr, modes):
    """
    orders: dictionary of all orders of today
    number: how many orders should be simulated in one go (batch size)
    rownr: index of first item in orders dataframe we need to read
    modes: list of 7 modes, each element either 'time', 'cost', or 'mix'
            the mode determines the routing optimization focus for that sector
    """

    pick_up_nodes, drop_off_nodes = [], []


    for j in range(number):
        orders, n = create_orders(orders, rownr+j, orders_df)

        for i in range(len(orders)-n, len(orders)):
            pick, drop = order_to_node(orders[i])
            pick_up_nodes.append(pick)
            drop_off_nodes.append(drop)

            print('Order', i,'at ', orders[i].time, 'was placed from location ', orders[i].node, ' which lies in region ', orders[i].region,
                  ' at ',
                  orders[i].time, ' and contains ', orders[i].amount, ' meals of type ', orders[i].food_type,
                  '. It was assigned to restaurant nr. ', orders[i].restaurant, ' and is expected to be ready at ',
                  orders[i].window[0])
            assign_order(pick, drop, orders, orders[i].time, mode=modes[orders[i].region - 1])

