import pandas as pd
import numpy as np
import datetime
import os
import random
from pprint import pprint
from classes.region import *
from classes.route_node import *
from stuff.map_dfs import restaurants_df

path = os.getcwd() + "/data/orders/orders_21-01-05.csv"
df_orders = pd.read_csv(path, sep=' ', index_col = 0)

#Get different meal types
cols = df_orders.columns
meal_types = []
for i in range(3,20):
  meal_types.append(cols[i].split('_',1)[0])

#Create new data frame with all meals added up per order (regardless of meal type)
meal_order = np.zeros(len(df_orders))
for j in meal_types:
  meal_order += df_orders[j+'_amount']
df_orders['meals_amount'] = meal_order
df_orders['order_time'] = pd.to_datetime(df_orders['order_time'])
df_incoming_order = df_orders[['lat','lon','order_time','meals_amount']]

#Assgin random restaurant to order (no matter what food type, opening hours, or capacity)
temp_assign_rest = np.empty(len(df_incoming_order))
temp_assign_rest[:] = np.NaN
region = np.empty(len(df_incoming_order))
region[:] = np.NaN
prod_time = np.empty(len(df_incoming_order))
prod_time[:] = np.NaN

for i in range(len(df_incoming_order)):
  p = Point(df_incoming_order['lat'][i], df_incoming_order['lon'][i])
  if regions[7].poly.contains(p):
     temp_assign_rest[i]= random.choice(regions[7].n_res['index_rest'])
     region[i] = 7
  prod_time[i] = int(df_incoming_order['meals_amount'].iloc[i]*15)
df_incoming_order['restaurant'] = temp_assign_rest
df_incoming_order['region'] = region
#pick up time
pick_up_time = np.zeros(len(df_incoming_order),dtype='datetime64[s]')
for i in range(len(df_incoming_order)):
  pick_up_time[i] = df_incoming_order['order_time'].iloc[i]+datetime.timedelta(minutes = int(prod_time[i]))
df_incoming_order['pick_up_time'] = pick_up_time
#Select only orders that concern test region
df_inc_Test_orders = df_incoming_order[df_incoming_order['region'] == 7]

#Simulate order
order_pop_up1 = df_inc_Test_orders.iloc[0]
order_pop_up2 = df_inc_Test_orders.iloc[1]


pick1 = Route_node()
drop1 = Route_node()
#When new order pops up, generate nodes
pick1.set_type('C')
pick1.set_location(assign_loc(order_pop_up1['lat'],order_pop_up1['lon'],paris_nodes))
pick1.set_number_of_meals(order_pop_up1['meals_amount'])
pick1.set_time_window(order_pop_up1['pick_up_time'],order_pop_up1['pick_up_time']+datetime.timedelta(hours = 4))

drop1.set_type('R')
drop1.set_location(int(restaurants_df.iloc[int(order_pop_up1['restaurant'])]['index']))
drop1.set_number_of_meals(order_pop_up1['meals_amount'])
drop1.set_time_window(order_pop_up1['pick_up_time'],order_pop_up1['pick_up_time']+datetime.timedelta(hours = 1))

#pprint(vars(pick1))

#second order simulation
order_pop_up2 = df_inc_Test_orders.iloc[1]
pick2 = Route_node()
drop2 = Route_node()
#When new order pops up, generate nodes
pick2.set_type('C')
pick2.set_location(assign_loc(order_pop_up2['lat'],order_pop_up2['lon'],paris_nodes))
pick2.set_number_of_meals(order_pop_up2['meals_amount'])
pick2.set_time_window(order_pop_up2['pick_up_time'],order_pop_up2['pick_up_time']+datetime.timedelta(hours = 4))

drop2.set_type('R')
drop2.set_location(int(restaurants_df.iloc[int(order_pop_up2['restaurant'])]['index']))
drop2.set_number_of_meals(order_pop_up2['meals_amount'])
drop2.set_time_window(order_pop_up2['pick_up_time'],order_pop_up2['pick_up_time']+datetime.timedelta(hours = 1))

time_now1 = order_pop_up1['order_time']
time_now2 = order_pop_up2['order_time']