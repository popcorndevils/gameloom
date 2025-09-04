from tkinter import ttk as tw


class NoteTaker(tw.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.grid(column=0, row=0, sticky="nesw")

        # configure frame layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Placeholder
        self._label = tw.Label(self, text="Note Taker!")
        self._button = tw.Button(self, text="TEST BUTTON")

        self._label.grid(column=0, row=0, sticky="nesw")
        self._button.grid(column=0, row=1, sticky="nesw")
