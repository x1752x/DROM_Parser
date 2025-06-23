import os.path
import sys

from tkinter import *
from MainController import MainController

class MainView:
    def __init__(self):
        self.controller = MainController(self)

        self.root = Tk()
        self.root.title("DROM Parser")
        self.root.geometry("640x480")
        self.root.protocol("WM_DELETE_WINDOW", self.controller.onclose)

        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "static", "icon.ico")
        else:
            icon_path = "static/icon.ico"
        self.root.iconbitmap(icon_path)

        self.result_listbox_label = Label(text="Results:")
        self.result_listbox_label.pack()

        self.result_listbox = Listbox()
        self.result_listbox.bind("<Double-Button-1>", self.controller.result_listbox_ondoubleclick)
        self.result_listbox.pack(fill='both')

        self.buttons_frame = Frame()
        self.start_button = Button(self.buttons_frame, text="Start", state="active", command=self.controller.start_button_onclick)
        self.stop_button = Button(self.buttons_frame, text="Stop", state="disabled", command=self.controller.stop_button_onclick)
        self.start_button.grid(row=0, column=0, padx = 5)
        self.stop_button.grid(row=0, column=1, padx = 5)
        self.buttons_frame.pack(pady = 10)

        self.options_frame = Frame()
        self.dromru_option = Checkbutton(self.options_frame, text="Drom.RU")
        self.autoru_option = Checkbutton(self.options_frame, text="Auto.RU")
        self.dromru_option.grid(row=0, column=0, padx=5)
        self.autoru_option.grid(row=0, column=1, padx=5)
        self.options_frame.pack()

        self.settings_frame = Frame()
        self.primary_label_from = Label(self.settings_frame, text="Primary registration year from:")
        self.primary_label_to = Label(self.settings_frame, text="Primary registration year to:")
        self.production_label_from = Label(self.settings_frame, text="Production year from:")
        self.production_label_to = Label(self.settings_frame, text="Production year to:")
        self.page_label_to = Label(self.settings_frame, text="Parse to page:")
        self.primary_entry_from = Entry(self.settings_frame)
        self.primary_entry_to = Entry(self.settings_frame)
        self.production_entry_from = Entry(self.settings_frame)
        self.production_entry_to = Entry(self.settings_frame)
        self.page_entry_to = Entry(self.settings_frame)
        self.primary_label_from.grid(row=0, column=0)
        self.primary_label_to.grid(row=1, column=0)
        self.production_label_from.grid(row=2, column=0)
        self.production_label_to.grid(row=3, column=0)
        self.page_label_to.grid(row=4, column=0)
        self.page_entry_to = Entry(self.settings_frame)
        self.primary_entry_from.grid(row=0, column=1)
        self.primary_entry_to.grid(row=1, column=1)
        self.production_entry_from.grid(row=2, column=1)
        self.production_entry_to.grid(row=3, column=1)
        self.page_entry_to.grid(row=4, column=1)
        self.settings_frame.pack()

        self.status_label = Label(text="Stopped")
        self.status_label.pack()

    def show(self):
        self.controller.onload()
        self.root.mainloop()