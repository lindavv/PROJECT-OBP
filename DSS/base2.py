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


texts = {
    1: "Daily shift optimization focus",
    2: "Vehicles in shift 12:00 - 00:00",
    3: "Vehicles in shift 18:00 - 21:00",
    4: "Routing optimization focus"
}



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




def plus(vehicles, veh_num, i, j):
    # in case we have an upper limit or something
    if vehicles[j][i-2] < 80:
        # this changes the number of vehicles in the shift as defined by the dic fiven in the base module
        vehicles[j][i-2] += 1
        # this modifies the GUI label accordingly
        veh_num[j][i-2].configure(text = str(vehicles[j][i-2]))

        change_vehicle_number(j+1, 1, i+1, orders[len(orders)-1].time)

        # change total as well
        vehicles[7][i-2] = sum([vehicles[k][i-2] for k in range(7)])
        veh_num[7][i-2].configure(text=str(vehicles[7][i-2]))
    else:
        pass


def first_settings(j, clocks, cars, settings1):
    if settings1[j] == 'vehicle':
        clocks[j][1].place_forget()          # remove clock inactive button
        clocks[j][0].place(x=304 + 130 * j, y=180, width=28.0, height=28.0)

        cars[j][0].place_forget()
        cars[j][1].place(x=234 + 130 * j, y=180, width=50.0, height=25.0)

        settings1[j] = 'time'
        print('Chosen ' + settings1[j] + ' optimization priority for sector ' + str(j+1) )


    elif settings1[j] == 'time':
        cars[j][1].place_forget()  # remove cars inactive button
        cars[j][0].place(x=234 + 130 * j, y=180, width=50.0, height=25.0)

        clocks[j][0].place_forget()
        clocks[j][1].place(x=304 + 130 * j, y=180, width=28.0, height=28.0)

        settings1[j] = 'vehicle'
        print('Chosen ' + settings1[j] + ' optimization priority for sector ' + str(j + 1))


def fourth_settings(j, costs, clocks, setting, settings4):
    if setting == 'time':
        clocks[j][1].place_forget()          # remove clock inactive button
        clocks[j][0].place(x=304 + 130 * j, y=573, width=28.0, height=28.0)

        costs[j][0].place_forget()
        costs[j][1].place(x=237 + 130 * j, y=567, width=34.0, height=36.0)

        settings4[j] = 'time'
        print('Chosen ' + settings4[j] + ' optimization priority for sector ' + str(j+1) )


    elif setting == 'cost':
        costs[j][1].place_forget()  # remove cars inactive button
        costs[j][0].place(x=237 + 130 * j, y=567, width=34.0, height=36.0)

        clocks[j][0].place_forget()
        clocks[j][1].place(x=304 + 130 * j, y=573, width=28.0, height=28.0)

        settings4[j] = 'cost'
        print('Chosen ' + settings4[j] + ' optimization priority for sector ' + str(j + 1))





def create_settings_page(canvas, images, vehicles, settings1, settings4):


    settings_objects = []

    for i in range(1, 5):

        # sector titles
        image = canvas.create_image(740, 162 + 131*(i-1), image = images[0])
        settings_objects.append(image)


    """----- First section -----------"""

    cars = []
    clocks = []

    for j in range(7):
        # when car setting active
        car_but1 = Button(image=images[4], borderwidth=0, highlightthickness=0,
                          command=lambda: None, relief="flat")

        # when car setting inactive
        car_but2 = Button(image=images[5], borderwidth=0, highlightthickness=0,
                          command=lambda j=j: first_settings(j, clocks, cars, settings1), relief="flat")

        if settings1[j] == 'vehicle':
            car_but1.place(x=234 + 130 * j, y=180, width=50.0, height=25.0)
        elif settings1[j] == 'time':
            car_but2.place(x=234+130*j, y=180, width=50, height=25)

        settings_objects.append(car_but1)
        settings_objects.append(car_but2)
        cars.append((car_but1, car_but2))



        clock_but1 = Button(image=images[6], borderwidth=0, highlightthickness=0,
                          command=lambda: None, relief="flat")   # button is already active

        clock_but2 = Button(image=images[7], borderwidth=0, highlightthickness=0,
                          command=lambda j=j: first_settings(j, clocks, cars, settings1), relief="flat")

        if settings1[j] == 'vehicle':
            clock_but2.place(x=304 + 130 * j, y=180, width=28.0, height=28.0)
        elif settings1[j] == 'time':
            clock_but1.place(x=304 + 130 * j, y=180, width=28.0, height=28.0)
        settings_objects.append(clock_but1)
        settings_objects.append(clock_but2)
        clocks.append((clock_but1, clock_but2))





    """----- Second and Third section ---------"""

    # create label objects for number of vehicles per shift
    veh_label = {}
    for j in range(0,8):
        nums = []
        for i in range(2):
            lab = Label(canvas, text=str(vehicles[j][i]), bg='white', font=('Arial', 12))
            if j < 7:
                lab.place(x = 145 + 130*(j+1), y= 310+131*i)
            else:
                lab.place(x=1170, y=310+131*i)
            nums.append(lab)
            settings_objects.append(lab)
        # dictionary of these numbers so they can be modified when buttons are clicked
        veh_label[j] = nums


    """ Total images """
    image = canvas.create_image(1187, 46 + 131 * 2, image=images[1])
    settings_objects.append(image)

    image = canvas.create_image(1187, 46 + 131 * 3, image=images[1])
    settings_objects.append(image)




    for i in range(1,5):

        if i ==2 or i ==3:

            for j in range(7):
                # plus and minus buttons
                button_minus = Button(image=images[2], borderwidth=0, highlightthickness=0,
                    command=lambda i=i, j=j: minus(vehicles, veh_label, i, j), relief="flat")
                button_minus.place(x= 235 + 130*j, y=51+131*i, width=21.0, height=21.0)
                settings_objects.append(button_minus)

                button_plus = Button(image=images[3], borderwidth=0, highlightthickness=0,
                    command=lambda i=i, j=j: plus(vehicles, veh_label, i, j), relief="flat")
                button_plus.place(x=314 + 130*j, y=51 + 131 * i, width=21.0, height=21.0)
                settings_objects.append(button_plus)


    """--------- Fourth Section--------------"""
    clocks4 = []
    cost4 = []

    for j in range(7):
        cost_but1 = Button(image=images[8], borderwidth=0, highlightthickness=0,
                           command=lambda: None, relief='flat')

        cost_but2 = Button(image = images[9], borderwidth=0, highlightthickness=0,
                           command=lambda j=j: fourth_settings(j, cost4, clocks4, 'cost', settings4), relief='flat')

        if settings4[j] == 'cost':
            cost_but1.place(x=237+130*j, y =567, width = 34, height=36)
        elif settings4[j] == 'time':
            cost_but2.place(x=237 + 130 * j, y=567, width=34, height=36)

        settings_objects.append(cost_but1)
        settings_objects.append(cost_but2)
        cost4.append((cost_but1, cost_but2))

        clock_but1 = Button(image=images[6], borderwidth=0, highlightthickness=0,
                            command=lambda: None, relief="flat")  # button is already active

        clock_but2 = Button(image=images[7], borderwidth=0, highlightthickness=0,
                            command=lambda j=j: fourth_settings(j, cost4, clocks4, 'time', settings4), relief="flat")

        if settings4[j] == 'cost':
            clock_but2.place(x=304 + 130 * j, y=573, width=28.0, height=28.0)
        elif settings4[j] == 'time':
            clock_but1.place(x=304 + 130 * j, y=573, width=28.0, height=28.0)
        settings_objects.append(clock_but1)
        settings_objects.append(clock_but2)
        clocks4.append((clock_but1, clock_but2))




    for i in range(1,5):
        tex = canvas.create_text(
            244.0,
            106+131*(i-1),
            anchor="nw",
            text=texts[i],
            fill="#4E5969",
            font=("DoppioOne-Regular", int(14.0))
        )

        settings_objects.append(tex)



    # Page Title
    settings_objects.append(canvas.create_text(
        78.0,
        22.0,
        anchor="nw",
        text='Settings',
        fill="#1D2129",
        font=("OpenSansRoman-Regular", int(20.0))
    ))

    return settings_objects



def leave_settings_page(canvas, objects):
    for object in objects:
        try:
            canvas.delete(object)
        except:
            object.place_forget()



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
    dummy_simulation2(orders=orders, number=5)
    update_home_stats()
    make_images()



def task_repeat():
    dummy_simulation2(orders =orders, number=3)
    update_home_stats()
    print(len(regions[4].get_vehicles()))
    make_images()
    app.window.after(10000, task_repeat)            # 20 seconds


#app.window.resizable(True, True)


app.window.after(2000, task_start)

app.window.after(10000, task_repeat)




app.window.mainloop()

