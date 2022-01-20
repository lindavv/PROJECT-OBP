import kivy

kivy.require('1.0.7')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class Order(GridLayout):

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.cols = 2
        A = Label(text='Order')
        food.txt = TextInput(multiline=False)
        self.add_widget(food)
        B = Label(text='Changes on Vehicle Amount')
        extra.txt = TextInput
        self.add_widget(extra)
        # This is the label that will hold a modified version of the user's
        # input
        # my_output = Label(text="Vehicles in use")
        # my_output=extra.int+10
        # self.add_widget(my_output)

        # default=10
        # Here we "bind" the callback to the TextInput's 'text' property
        # If you skip this step, you won't see the changes ever take place
        food.bind(text=A.setter('text'))
        vehicle.bind(text=(B.setter('text'))


class GuiApp(App):

    def build(self):
        return Order()


if __name__ == '__main__':
    GuiApp().run()

# car=default+vehicle
# print(car)

# if __name__ == '__main__':
#     MyApp().run()
