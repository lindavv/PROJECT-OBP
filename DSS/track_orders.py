from tkinter import *



def track():
    print('track')



def create_tracking_page(canvas, images, stats):

    tracking_objects = [canvas.create_rectangle(215, 85, 1235, 610, fill="#FFFFFF", outline="")]

    """Map"""
    map = canvas.create_image(570, 350, image=images[0])
    tracking_objects.append(map)

    """Orders"""
    # first
    id = 0
    write = 'Order #'+ str(stats[id]['id'])+ ' placed at ' + stats[id]['order_time'] + ' and\nis waiting at the restaurant.\nIt is expected to be delivered at ' + stats[id]['del_time']+'.'
    label = Label(canvas, text=write, anchor='nw',  bg='white', font=('Arial', 11))
    label.place(x=950, y=200, anchor='nw')
    tracking_objects.append(label)


    # input order
    input_order = Text(height=5, width=5)
    input_order.place(x=1000, y=380)
    tracking_objects.append(input_order)

    input_title = Label(canvas, bg='white', text="Track another order #", font=('Arial', 13))
    input_title.place(x=980, y=350)
    tracking_objects.append(input_title)

    order_chosen_label = Label(canvas, bg='white', text="Order available y/n?", font=('Arial', 12))
    order_chosen_label.place(x=980, y=480)
    tracking_objects.append(order_chosen_label)

    track_button = Button(text="Track", command= lambda: track())
    track_button.place(x=1100, y=400)
    tracking_objects.append(track_button)




    title = canvas.create_text(
        78.0,
        22.0,
        anchor="nw",
        text='Track orders',
        fill="#1D2129",
        #font=("OpenSansRoman-Regular", int(20.0))
        font = ("Tahoma", 17)
    )
    tracking_objects.append(title)

    return tracking_objects


def leave_tracking_page(canvas, objects):
    for object in objects:
        try:
            canvas.delete(object)
        except:
            object.place_forget()
