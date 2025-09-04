import logging

from ._pdf_browser import PDFBrowser
from ._note_taker import NoteTaker

from tkinter import ttk as tw


class GMCopilot:
    def __init__(self, root):
        logging.info("Loading main application window.")

        self.root = root

        # configure window
        self.root.title("GM Copilot")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._view_main = tw.Frame(self.root, padding=(5, 5, 5, 5))
        self._view_functions = tw.Notebook(self._view_main, width=800, height=600, padding=10)

        self._pdf_browser = PDFBrowser(self._view_functions)
        self._note_taker = NoteTaker(self._view_functions)

        self._view_functions.add(self._pdf_browser, text="PDF Browser")
        self._view_functions.add(self._note_taker, text="Note Taker")

        # set view weights
        self._view_main.columnconfigure(0, weight=1)
        self._view_main.rowconfigure(0, weight=1)
        self._view_functions.columnconfigure(0, weight=1)
        self._view_functions.rowconfigure(0, weight=1)

        # set grids
        self._view_main.grid(column=0, row=0, sticky="nesw")
        self._view_functions.grid(column=0, row=0, sticky="nesw")
