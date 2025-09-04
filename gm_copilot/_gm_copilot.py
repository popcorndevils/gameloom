import tkinter as tk
from tkinter import ttk as tw

from ._pdf_browser import PDFBrowser
from ._note_taker import NoteTaker


class GMCopilot:
    def __init__(self, root):
        self.root = root

        # configure window
        self.root.title("GM Copilot")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._view_main = tw.Frame(self.root, padding=(5, 5, 5, 5))
        self._view_functions = tw.Notebook(self._view_main, width=400, height=300)

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
        self._view_main.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self._view_functions.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
