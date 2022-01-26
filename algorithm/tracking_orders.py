#<<<<<<< Updated upstream
orders = {}
#=======

from algorithm.handle_vehiclefleet import *
from classes.vehicle import assign_order

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

number = 20

for i in range(number):
    create_orders(i)

print('Order 0 was placed from location ', orders[0].node,' which lies in region ', orders[0].region, ' at ', orders[0].time, ' and contains ', orders[0].amount, ' ', orders[0].food_type,
      '. It was assigned to restaurant nr. ', orders[0].restaurant, ' and is expected to be ready at ', orders[0].window[0])
#pprint(vars(orders[0]))

date = datetime.now().date()
initialize_vehicles(date)



for i in range(len(orders)):
    pick, drop = order_to_node(orders[i])
    pick_up_nodes.append(pick)
    drop_off_nodes.append(drop)
    #print(pick.order.time)
    #print('Order', i, 'was placed from location ', orders[i].node, ' which lies in region ', orders[i].region, ' at ',
    #      orders[i].time, ' and contains ', orders[i].amount, ' ', orders[i].food_type,
    #      '. It was assigned to restaurant nr. ', orders[i].restaurant, ' and is expected to be ready at ',
    #      orders[i].window[0])
    #assign_order(pick, drop, orders[i].time, mode='time')


#pprint(vars(regions[1].get_vehicles()[2]))
"""Mode can either be time or cost, depending on optimization focus"""
















#>>>>>>> Stashed changes
