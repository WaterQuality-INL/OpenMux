from tkinter import *
from tkinter import ttk
import tkinter_tools_module as ttm
from PIL import ImageTk, Image


class StatusLED(Frame):
    def __init__(self, master, status: bool = None, **kwargs):
        super().__init__(master=master, bd=1, relief=SUNKEN)
        Label(self, text=kwargs["text"], width=10, fg="grey").grid(row=0, column=0)
        self.LED = Frame(self, width=10, height=10)
        self.LED.grid(row=0, column=1)

        self.set_led_status(status)


    def set_led_status(self, status: bool):
        if status:
            self.LED.configure(background="Green")
        else:
            self.LED.configure(background="Red")

    def set_stby_status(self):
        self.LED.configure(background="Yellow")


class CostumeNoteBook(ttk.Notebook):
    """
    Costume Notebook. Implemented methods to add and remove costume tabs and variables to track existent tabs
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tabs_list = []
        self.idx = 1

    def add_costume_tab(self, **kwargs):
        cost_tab = ttm.NewTabGUI(self, **kwargs)
        self.tabs_list.append(cost_tab)
        return cost_tab

    def remove_tab(self, costume_tab):
        self.tabs_list.remove(costume_tab)

    def get_costume_tab(self):
        """ Retrieves the active costume tab """
        return self.tabs_list[self.index(self.select())]


class IconWidget(Button):
    def __init__(self, master, path: str, size: tuple = (50, 50), **kwargs):
        self.path = path

        self.icon = self.get_and_scale_icon(size)

        super().__init__(master=master, image=self.icon, command=kwargs["command"], relief=FLAT, bd=0, bg=kwargs["bg"])

    def get_and_scale_icon(self, size):
        icon = Image.open(self.path)
        icon = icon.resize(size)
        return ImageTk.PhotoImage(icon)


class NiceButton(Button):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, background="Azure", **kwargs)
