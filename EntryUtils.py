class EntryUtils:
    @staticmethod
    def set_text(text, entry):
        """
        :type text: str
        :type entry: tkinter.Entry
        """
        entry.delete(0, "end")
        entry.insert(0, text)