import logging
from tkinter import ttk as tw
from .filecabinet import FileCabinet
from ._clipper_ui import PageImages, PageExport


class ArtClipper(tw.Frame):
    def __init__(self, *args, **kwargs):
        logging.info("Loading ArtClipper.")
        super().__init__(*args, **kwargs)
        self.configure(padding=5)

        # components
        self._view_main = tw.Frame(self, padding=(5, 5, 5, 5))
        self._view_functions = tw.Notebook(self._view_main, padding=10)
        self._page_images = PageImages(self._view_functions)
        self._page_export = PageExport(self._view_functions)

        self._view_functions.add(self._page_images, text="Image Select")
        self._view_functions.add(self._page_export, text="Export Images")

        # pdf file handler
        self._cabinet = FileCabinet()
        self._page_images.cabinet = self._cabinet

        # styling
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._view_main.grid(column=0, row=0, sticky="nsew")
        self._view_main.columnconfigure(0, weight=1)
        self._view_main.rowconfigure(0, weight=1)
        self._view_functions.grid(column=0, row=0, sticky="nsew")
