from tkinter import *
from pathlib import Path
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./pics")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def create_home_page(canvas, images, stats):


    home_objects = [
        canvas.create_rectangle(215, 85, 1235, 189, fill="#FFFFFF", outline=""),
        canvas.create_rectangle(215, 200, 1235, 610, fill="#FFFFFF", outline="")
    ]



    """" Top five statistics -------------"""
    for i in range(5):
        image = canvas.create_image(312+206*i, 143, image = images[i])
        home_objects.append(image)


        if i<3:
            label = Label(canvas, text=str(stats[i]), bg='white', font=('Arial', 13))
            label.place(x=330+206*i, y= 145)
        else:
            label = Label(canvas, text=str(round(stats[i], 2)), bg='white', font=('Arial', 13))
            label.place(x=318+206*i, y=140)

        home_objects.append(label)



    """ Three graphs -------------------"""
    graph_titles = ['Cost per region', 'Customer waiting time per region']

    for i in range(2):
        label = Label(canvas, text=graph_titles[i], bg='white', font=('Arial', 12))
        label.place(x=360+440*i, y=210)
        home_objects.append(label)

        if sum(stats[5+i]) > 0:
            graph = canvas.create_image(460+500*i, 430, image=images[5+i])
        else:
            graph = canvas.create_image(460+500*i, 430, image=images[7])
        home_objects.append(graph)





    title = canvas.create_text(
        78.0,
        22.0,
        anchor="nw",
        text='Home',
        fill="#1D2129",
        font=("OpenSansRoman-Regular", int(17.0))
    )

    home_objects.append(title)
    return home_objects


def leave_home_page(canvas, objects):
    for object in objects:
        try:
            canvas.delete(object)
        except:
            object.place_forget()



