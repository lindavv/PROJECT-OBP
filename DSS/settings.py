from tkinter import *
from pathlib import Path
from algorithm.handle_vehiclefleet import change_vehicle_number
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./pics")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

"""
python build\base.py
"""

"""-----------Settings ----------------"""

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


