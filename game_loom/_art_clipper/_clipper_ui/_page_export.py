from tkinter import ttk as tw
from ...LoomTypes import LoomFrame


class PageExport(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._placeholder = tw.Label(self, text="HELLO THERE")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
