import os
from pathlib import Path
from DSS.home import *
from DSS.settings import *
from DSS.graphs import *
from DSS.track_orders import *
from tkinter import *
import random
import threading

from algorithm.sim2 import *


writings = {
    'date': 'Tuesday 25-01-2022      17:52',     # upper right
    'current_page': 'Restaurants'
}




####################################################################
"""Home page"""
#home_stats = {0: 968, 1: 788, 2: 30, 3: 38.7, 4: 90432}
home_stats = {0:0, 1:0, 2:0, 3:0, 4:0,
              5: [0]*7, 6:[0]*7}


"""Settings page"""
# settings per sector!!!!!
settings_first_section = ['vehicle' for i in range(7)]
settings_fourth_section = ['cost' for i in range(7)]


n_vehicles = [[random.randint(0, 30) for i in range(2)] for i in range(7)]
n_vehicles.append([sum([n_vehicles[j][0] for j in range(7)]), sum([n_vehicles[j][1] for j in range(7)])])


"""Track orders page"""
track_stats = [
    {'id': 1529, 'status': 'Waiting in restaurant',
     'order_time': "19:23",
      'del_time': "20:12"},
    {'id': 1346, 'status': 'On it\'s way', 'order_time': "19:02", 'del_time': "19:48"}
]
###################################################################



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./pics")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def minus(vehicles, veh_num, i, j):
    if vehicles[j][i-2] > 2:
        # this changes the number of vehicles in the shift as defined by the dic fiven in the base module
        vehicles[j][i-2] -= 1
        # this modifies the GUI label accordingly
        veh_num[j][i-2].configure(text = str(vehicles[j][i-2]))

        change_vehicle_number(j+1, -1, i+1, orders[len(orders)-1].time)

        # change total as well
        vehicles[7][i-2] = sum([vehicles[k][i-2] for k in range(7)])
        veh_num[7][i-2].configure(text=str(vehicles[7][i-2]))
    else:
        pass




def upper_rect(canvas):
    canvas.create_rectangle(
        10.0,
        6.0,
        1244.0,
        66.0,
        fill="#FFFFFF",
        outline="")

    canvas.create_text(
        885.0,
        25.0,
        anchor="nw",
        text= writings['date'],
        fill="#000",
        font=("None", int(11.0))
    )





""" --------- Pages & frames and stuf ------------"""

# all pages should fit inside the following shape......
#canvas.create_rectangle(220, 85, 1235, 610, fill="#FFFFFF", outline="")
def make_images():
    settings_images = [
        PhotoImage(file=relative_to_assets("image_2.png")),    # sector titles
        PhotoImage(file=relative_to_assets("image_4.png")),      # total
        PhotoImage(file=relative_to_assets("button_13.png")),    # minus
        PhotoImage(file=relative_to_assets("button_14.png")),    # plus
        PhotoImage(file=relative_to_assets("button_vehicle_selected.png")),
        PhotoImage(file=relative_to_assets("button_vehicle_nonselect.png")),
        PhotoImage(file=relative_to_assets("button_clock_selected.png")),
        PhotoImage(file=relative_to_assets("button_clock_nonselect.png")),
        PhotoImage(file=relative_to_assets("button_cost_selected.png")),
        PhotoImage(file=relative_to_assets("button_cost_nonselect.png"))
    ]

    home_images = [
        PhotoImage(file=relative_to_assets("image_home1.png")),    # orders received
        PhotoImage(file=relative_to_assets("image_home2.png")),      # orders delivered
        PhotoImage(file=relative_to_assets("image_home3.png")),    # orders delayed
        PhotoImage(file=relative_to_assets("image_home4.png")),      # avg waiting time
        PhotoImage(file=relative_to_assets("image_home5.png")),    # costs
        PhotoImage(file=relative_to_assets("graph1.png")),
        PhotoImage(file=relative_to_assets("graph2.png")),
        PhotoImage(file=relative_to_assets("graph_empty.png"))
    ]

    track_images = [
        PhotoImage(file=relative_to_assets("map.png"))
    ]
    return settings_images, home_images, track_images




class App(threading.Thread):
    def __init__(self, window):
        self.window = window

        self.window.geometry("1256x636")
        self.window.configure(bg="#F7F8FA")
        self.window.resizable(False, False)

        threading.Thread.__init__(self)
        self.current = 'home'
        self.canvas = Canvas(
            self.window,
            bg = "#F7F8FA",
            height =636,   #636
            width = 1256,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)



        upper_rect(self.canvas)
        self.settings_images, self.home_images, self.track_images = make_images()
        self.current_objects = create_home_page(self.canvas, self.home_images, home_stats)




    def click_sidebar_button(self, next):
        # remove previous page
        if self.current == 'settings':
            print('Leave settings page')
            leave_settings_page(self.canvas, self.current_objects)
        elif self.current == 'home':
            print('Leave home page')
            leave_home_page(self.canvas, self.current_objects)
        elif self.current == 'track':
            print('Leave track orders page')
            leave_tracking_page(self.canvas, self.current_objects)

        self.settings_images, self.home_images, self.track_images = make_images()
        # go to new page
        if next == 'home':
            print('Go to home page')
            new_objects = create_home_page(self.canvas, self.home_images, home_stats)
        elif next == 'settings':
            print('Go to settings')
            new_objects = create_settings_page(self.canvas, self.settings_images, n_vehicles, settings_first_section, settings_fourth_section)
        elif next == 'track':
            print('Go to track orders page')
            new_objects = create_tracking_page(self.canvas, self.track_images, track_stats)

        self.current = next
        self.current_objects = new_objects

window = Tk()
app = App(window)

app.canvas.create_rectangle(
    16.0,
    86.0,
    195.0,
    616.0,
    fill="#FFFFFF",
    outline="")


""" -------- Sectors Button ------------- """
button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
)

button_1.place(
    x=26.0,
    y=187.0,
    width=135.0,
    height=44.0
)


"""------------ Logo --------------- """
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = app.canvas.create_image(
    42.0,
    32.62371826171875,
    image=image_image_1
)


"""--------------Settings button -----------------"""
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    #command=lambda: print("button_3 clicked"),
    #command = lambda: click_sidebar_button(canvas, current_page, 'settings', current_page_objects),
    command = lambda: app.click_sidebar_button('settings'),
    relief="flat"
)
button_3.place(
    x=26.0,
    y=198.0,
    width=139.0,
    height=40.0
)


""" ------ Track orders button ------------"""
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: app.click_sidebar_button('track'),
    relief="flat"
)
button_4.place(
    x=26.0,
    y=148.0,
    width=161.0,
    height=40.0
)



"""------------- Home button ----------- """
button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    #command = lambda: click_sidebar_button(canvas, current_page, 'home', current_page_objects),
    command = lambda: app.click_sidebar_button('home'),
    relief="flat"
)
button_6.place(
    x=26.0,
    y=99.0,
    width=139.0,
    height=40.0
)

orders = {}
count = 0

def make_graphs():
    pass


def update_home_stats():
    # total orders
    home_stats[0] = len(orders)

    delivered = 0
    delayed = 0
    waitt  = 0
    kms = 0

    costs_persector = [regions[region].evaluation['kms driven']/2 for region in regions.keys()]
    wait_persector = [regions[region].evaluation['Avg. waiting time'] for region in regions.keys()]

    home_stats[5] = costs_persector
    home_stats[6] = wait_persector

    make_plot(costs_persector, 1)
    make_plot(wait_persector, 2)

    for region in regions.keys():
        delivered += regions[region].evaluation['Orders delivered']
        delayed += regions[region].evaluation['Num_delayed_orders']
        waitt += regions[region].evaluation['Avg. waiting time'] /7
        kms += regions[region].evaluation['kms driven']

    home_stats[1] = delivered
    home_stats[2] = delayed
    home_stats[3] = waitt
    home_stats[4] = kms / 2










def task_start():
    dummy_simulation2(orders=orders, number=10)
    update_home_stats()
    make_images()



def task_repeat():
    dummy_simulation2(orders =orders, number=3)
    update_home_stats()
    make_images()
    app.window.after(10000, task_repeat)            # 20 seconds


#app.window.resizable(True, True)


app.window.after(2000, task_start)

app.window.after(10000, task_repeat)




app.window.mainloop()

