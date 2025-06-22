import json

from EntryUtils import EntryUtils
from Settings import Settings

class MainController:
    def __init__(self, view):
        """
        :type view: MainView.MainView
        """
        self.view = view

    def retrieve_settings(self):
        return Settings(
            primary_from = int(self.view.primary_entry_from.get()),
            primary_to = int(self.view.primary_entry_to.get()),
            production_from = int(self.view.production_entry_from.get()),
            production_to = int(self.view.production_entry_to.get()),
            page = int(self.view.page_entry_to.get())
        )

    def onload(self):
        with open("config/settings.json", 'r') as file:
            settings = json.load(file)

        EntryUtils.set_text(settings['primary_from'], self.view.primary_entry_from)
        EntryUtils.set_text(settings['primary_to'], self.view.primary_entry_to)
        EntryUtils.set_text(settings['production_from'], self.view.production_entry_from)
        EntryUtils.set_text(settings['production_to'], self.view.production_entry_to)
        EntryUtils.set_text(settings['page'], self.view.page_entry_to)

    def onclose(self):
        try:
            settings_dict = self.retrieve_settings().__dict__
        except ValueError:
            self.view.root.destroy()
            return

        with open("config/settings.json", "w") as file:
            json.dump(settings_dict, file)

        self.view.root.destroy()

    def start_button_onclick(self):
        try:
            settings = self.retrieve_settings()
        except ValueError:
            self.view.status_label.config(text="Wrong values")
            return

        self.view.start_button.config(state="disabled")
        self.view.stop_button.config(state="active")
        self.view.status_label.config(text="Parsing...")

        # here we parse...

    def stop_button_onclick(self):
        self.view.start_button.config(state="active")
        self.view.stop_button.config(state="disabled")
        self.view.status_label.config(text="Stopped")

        # here we stop...