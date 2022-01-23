#<<<<<<< Updated upstream
orders = {}
#=======
import pandas as pd
from classes.restaurant_order import Order, Restaurant, restaurants
import os
from stuff.map_dfs import g
import networkx as nx



root = os.getcwd() + '/data/orders/orders_21-01-0'+ str(5) + '.csv'
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
    return order


orders = {}


for i in range(100):
    orders[i] = create_orders(i)
    orders[i].assign_restaurant()

print(orders[0].amount)
print(orders[0].time)
res = restaurants[orders[0].restaurant]
print(res.queue)


#>>>>>>> Stashed changes
