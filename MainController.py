import json
import os.path
import sys
import threading
import webbrowser

import requests.exceptions
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from DromParser import DromParser
from EntryUtils import EntryUtils
from Settings import Settings

class MainController:
    def __init__(self, view):
        """
        :type view: MainView.MainView
        """

        self.view = view
        self.parser: DromParser | None = None # will initialize later in onload handler
        self.parser_thread: threading.Thread | None = None # will initialize later in onload handler
        self.is_parsing: bool = False
        self.parsing_termination: bool = False
        self.listbox_dict: dict[str, str] = {}

    @staticmethod
    def get_config_path():
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), "config", "settings.json")
        return os.path.join("config", "settings.json")

    @staticmethod
    def get_notification_path():
        if getattr(sys, 'frozen', False):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, 'static', "notification.wav")

    def retrieve_settings(self):
        return Settings(
            primary_from = int(self.view.primary_entry_from.get()),
            primary_to = int(self.view.primary_entry_to.get()),
            production_from = int(self.view.production_entry_from.get()),
            production_to = int(self.view.production_entry_to.get()),
            page = int(self.view.page_entry_to.get())
        )

    def worker(self):
        while True:
            if self.parsing_termination:
                break

            if not self.is_parsing:
                continue

            try:
                temp = self.parser.parse()
            except requests.exceptions.ConnectionError:
                self.stop_button_onclick()
                self.view.status_label.config(text="Connection error. Try again later.")
                continue

            if not self.is_parsing:
                continue
            self.view.result_listbox.delete(0, "end")

            if not self.is_parsing:
                continue
            for key in temp.keys():
                self.view.result_listbox.insert("end", key)

            if temp != self.listbox_dict:
                self.listbox_dict = temp
                PlaySound(self.get_notification_path(), SND_FILENAME | SND_ASYNC)


    def onload(self):
        path = self.get_config_path()
        if os.path.exists(path):
            with open(path, 'r') as file:
                settings = json.load(file)

            EntryUtils.set_text(settings['primary_from'], self.view.primary_entry_from)
            EntryUtils.set_text(settings['primary_to'], self.view.primary_entry_to)
            EntryUtils.set_text(settings['production_from'], self.view.production_entry_from)
            EntryUtils.set_text(settings['production_to'], self.view.production_entry_to)
            EntryUtils.set_text(settings['page'], self.view.page_entry_to)

        self.parser_thread = threading.Thread(target=self.worker, args=())

    def onclose(self):
        self.is_parsing = False
        self.parsing_termination = True
        if self.parser_thread.is_alive():
            self.parser_thread.join(timeout=0.1)

        try:
            settings_dict = self.retrieve_settings().__dict__
        except ValueError:
            self.view.root.destroy()
            return

        os.makedirs(os.path.dirname(self.get_config_path()), exist_ok=True)
        with open(self.get_config_path(), "w") as file:
            json.dump(settings_dict, file)

        self.view.root.destroy()
        os._exit(0)

    def start_button_onclick(self):
        try:
            settings = self.retrieve_settings()
        except ValueError:
            self.view.status_label.config(text="Wrong values")
            return

        if not self.parser:
            self.parser = DromParser(settings)

        self.view.start_button.config(state="disabled")
        self.view.stop_button.config(state="active")
        self.view.status_label.config(text="Parsing...")

        if not self.parser_thread.is_alive():
            self.parser_thread.start()
        self.is_parsing = True

    def result_listbox_ondoubleclick(self, event):
        """
        :type event: tkinter.Event
        """
        selection = self.view.result_listbox.curselection()
        if not selection:
            return

        title = self.view.result_listbox.get(selection[0])
        webbrowser.open(self.listbox_dict[title])

    def stop_button_onclick(self):
        self.is_parsing = False
        self.view.start_button.config(state="active")
        self.view.stop_button.config(state="disabled")
        self.view.status_label.config(text="Stopped")