import logging

from tkinter import filedialog
from tkinter import ttk as tw
from .filecabinet import FileCabinet
from ._clipper_ui import PDFControl, ImageControl
from ..LoomTypes import LoomGrid


class ArtClipper(tw.Frame):
    def __init__(self, root):
        logging.info("Loading ArtClipper.")
        super().__init__(root, padding=5)

        self._root = root

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # pdf handler
        self._cabinet = FileCabinet()

        # browser components
        self._selector = PDFControl(self)
        self._image_grid = LoomGrid(self)

        # styling
        self._selector.grid(column=0, row=0, sticky="w")
        self._image_grid.grid(column=0, row=1, sticky="nsew")
        self._image_grid.num_columns = 4

        # event handling
        self._selector.observe_event("load_pdfs", self._handle_load_pdfs)
        self._selector.observe_event("selection", self._handle_pdf_select)
        self._selector.observe_event("page_select", self._handle_page_select)

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
        doc = self._cabinet[selection]
        self._selector.num_pages = len(doc)
        self._selector.page_index = 0

    def _handle_page_select(self, page_index):
        _doc = self._cabinet[self._selector.pdf_selection]
        _page = _doc[page_index]
        _img_list = _page.get_images(full=True)
        self._image_grid.clear_grid()

        for img in _img_list:
            xref = img[0]
            _new_ic = ImageControl(self._image_grid)
            _new_ic.image_data = _doc.extract_image(xref)

        self._image_grid.update_display()
