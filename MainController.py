import json
import os.path
import sys
import threading
import webbrowser
import requests.exceptions

from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from DromParser import DromParser
from ElementUtils import ElementUtils
from Settings import Settings

class MainController:
    def __init__(self, view):
        """
        :type view: MainView.MainView
        """

        self.view = view
        self.drom_parser: DromParser | None = None # will initialize later in onload handler
        self.drom_parser_thread: threading.Thread | None = None # will initialize later in onload handler
        self.drom_parsing: bool = False
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
            primary_from = ElementUtils.Entry.get_int(self.view.primary_entry_from),
            primary_to = ElementUtils.Entry.get_int(self.view.primary_entry_to),
            production_from = ElementUtils.Entry.get_int(self.view.production_entry_from),
            production_to = ElementUtils.Entry.get_int(self.view.production_entry_to),
            page = ElementUtils.Entry.get_int(self.view.page_entry_to),
            dromru_allowed=ElementUtils.Checkbutton.get_bool(self.view.dromru_option),
            autoru_allowed=ElementUtils.Checkbutton.get_bool(self.view.autoru_option),
        )

    def drom_parser_worker(self):
        while True:
            if self.parsing_termination:
                break

            if not self.drom_parsing:
                continue

            try:
                temp = self.drom_parser.parse()
            except requests.exceptions.ConnectionError:
                self.stop_button_onclick()
                ElementUtils.Label.set_text("Connection error. Try again later.", self.view.status_label)
                continue

            if not self.drom_parsing:
                continue
            ElementUtils.Listbox.clear(self.view.result_listbox)

            if not self.drom_parsing:
                continue
            for key in temp.keys():
                ElementUtils.Listbox.append(key, self.view.result_listbox)

            if temp != self.listbox_dict:
                self.listbox_dict = temp
                PlaySound(self.get_notification_path(), SND_FILENAME | SND_ASYNC)


    def onload(self):
        path = self.get_config_path()
        if os.path.exists(path):
            with open(path, 'r') as file:
                settings = json.load(file)

            ElementUtils.Entry.set_text(settings['primary_from'], self.view.primary_entry_from)
            ElementUtils.Entry.set_text(settings['primary_to'], self.view.primary_entry_to)
            ElementUtils.Entry.set_text(settings['production_from'], self.view.production_entry_from)
            ElementUtils.Entry.set_text(settings['production_to'], self.view.production_entry_to)
            ElementUtils.Entry.set_text(settings['page'], self.view.page_entry_to)

        self.drom_parser_thread = threading.Thread(target=self.drom_parser_worker, args=())

    def onclose(self):
        self.drom_parsing = False
        self.parsing_termination = True
        if self.drom_parser_thread.is_alive():
            self.drom_parser_thread.join(timeout=0.1)

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
            ElementUtils.Label.set_text("Wrong values", self.view.status_label)
            return

        if not settings.dromru_allowed and not settings.autoru_allowed:
            ElementUtils.Label.set_text("Please, choose at least one source", self.view.status_label)
            return

        if settings.dromru_allowed:
            if not self.drom_parser:
                self.drom_parser = DromParser(settings)
            if not self.drom_parser_thread.is_alive():
                self.drom_parser_thread.start()
            self.drom_parsing = True

        ElementUtils.Button.disable(self.view.start_button)
        ElementUtils.Button.enable(self.view.stop_button)
        ElementUtils.Label.set_text("Parsing...", self.view.status_label)

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
        self.drom_parsing = False
        ElementUtils.Button.enable(self.view.start_button)
        ElementUtils.Button.disable(self.view.stop_button)
        ElementUtils.Label.set_text("Stopped", self.view.status_label)