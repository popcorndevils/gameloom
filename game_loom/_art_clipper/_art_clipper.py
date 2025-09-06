import logging

from tkinter import filedialog
from tkinter import ttk as tw
from .filecabinet import FileCabinet
from .pdf_components import PDFSelector


class ArtClipper(tw.Frame):
    def __init__(self, root):
        logging.info("Loading ArtClipper.")
        super().__init__(root, padding=5)

        self._root = root

        # pdf handler
        self._cabinet = FileCabinet()

        # browser components
        self._selector = PDFSelector(self)

        # styling
        self._selector.grid(column=0, row=0)

        # event handling
        self._selector.observe("load_pdfs", self._handle_load_pdfs)
        self._selector.observe("selection", self._handle_pdf_select)

        # image testing
        self._test_image = tw.Label()

    @property
    def root(self):
        return self._root

    def _handle_load_pdfs(self):
        _files = filedialog.askopenfiles()
        for f in _files:
            self._cabinet.add(f)
        self._selector.pdf_options = self._cabinet.file_names
        logging.info(f"{len(_files)} files have been loaded.")

    def _handle_pdf_select(self, selection):
        logging.info(f"New pdf '{selection}' selected.")
