class MainController:
    def __init__(self, view):
        """
        :type view: MainView.MainView
        """
        self.view = view

    def settings_dict(self):
        settings = {
            "primary_from": int(self.view.primary_entry_from.get()),
            "primary_to": int(self.view.primary_entry_to.get()),
            "production_from": int(self.view.production_entry_from.get()),
            "production_to": int(self.view.production_entry_to.get()),
            "page": int(self.view.page_entry_to.get())
        }

        return settings

    def start_button_onclick(self):
        try:
            settings = self.settings_dict()
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