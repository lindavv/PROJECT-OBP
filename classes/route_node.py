import numpy as np
import datetime

class Route_node:
#Missing: assign region to node
  def __init__(self):
    self.type_ = np.NaN
    self.location = {'node_index':np.NaN}
    self.time_window = {'closing':0,'opening':0}
    self.number_of_meals = 0                      #Either to be picked up or dropped off, depending on type

  def set_type(self,type_):
    self.type_ = type_
  def set_location(self,index):
    self.location['node_index']=index
  def set_number_of_meals(self,meals):
    self.number_of_meals = meals
  def set_time_window(self,opening,closing):
    self.time_window['opening'] = opening
    self.time_window['closing'] = closing

  def get_type(self):
    return self.type_
  def get_location(self):
    return self.location
  def get_number_of_meals(self):
    return self.number_of_meals
  def get_time_window(self):
    return self.time_window