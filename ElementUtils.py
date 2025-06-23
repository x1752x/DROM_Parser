class ElementUtils:
    class Entry:
        @staticmethod
        def set_text(text, entry) -> None:
            """
            :type text: str
            :type entry: tkinter.Entry
            """
            entry.delete(0, "end")
            entry.insert(0, text)

        @staticmethod
        def get_int(entry) -> int:
            """
            :type entry: tkinter.Entry
            """
            return int(entry.get())

    class Checkbutton:
        @staticmethod
        def get_bool(checkbutton) -> bool:
            """
            :type checkbutton: tkinter.Checkbutton
            """
            return checkbutton.winfo_toplevel().tk.globalgetvar(checkbutton.cget("variable")) == '1'

    class Label:
        @staticmethod
        def set_text(text, label) -> None:
            """
            :type text: str
            :type label: tkinter.Label
            """
            label.config(text=text)

    class Listbox:
        @staticmethod
        def clear(listbox) -> None:
            """
            :type listbox: tkinter.Listbox
            """
            listbox.delete(0, "end")

        @staticmethod
        def append(element, listbox) -> None:
            """
            :type element: Any
            :type listbox: tkinter.Listbox
            """
            listbox.insert("end", element)

    class Button:
        @staticmethod
        def enable(button) -> None:
            """
            :type button: tkinter.Button
            """
            button.config(state="active")

        @staticmethod
        def disable(button) -> None:
            """
            :type button: tkinter.Button
            """
            button.config(state="disabled")