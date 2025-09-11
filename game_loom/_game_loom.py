import logging

from ._art_clipper import ArtClipper
from ._lore_keeper import LoreKeeper

from tkinter import ttk as tw


class GameLoom:
    def __init__(self, root):
        logging.info("Loading main application window.")

        self.root = root

        # configure windows
        self._view_main = tw.Frame(self.root, padding=(5, 5, 5, 5))
        self._view_functions = tw.Notebook(self._view_main, width=800, height=800, padding=10)

        self._pdf_browser = ArtClipper(self._view_functions)
        self._note_taker = LoreKeeper(self._view_functions)

        self._view_functions.add(self._pdf_browser, text="Art Clipper")
        self._view_functions.add(self._note_taker, text="Lore Keeper")

        # set view weights
        self._view_main.columnconfigure(0, weight=1)
        self._view_main.rowconfigure(0, weight=1)
        self._view_functions.columnconfigure(0, weight=1)
        self._view_functions.rowconfigure(0, weight=1)

        # set styling
        self._view_main.grid(column=0, row=0, sticky="nesw")
        self._view_functions.grid(column=0, row=0, sticky="nesw")
