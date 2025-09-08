import logging

from tkinter import filedialog
from tkinter import ttk as tw
from .filecabinet import FileCabinet
from ._clipper_ui import PDFControl
from ._clipper_ui import ImageControl
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

        # event handling
        self._selector.observe_event("load_pdfs", self._handle_load_pdfs)
        self._selector.observe_event("selection", self._handle_pdf_select)

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
        page = doc[0]
        img_list = page.get_images(full=True)
        self._image_grid.clear_grid()

        for img in img_list:
            xref = img[0]
            _new_ic = ImageControl(self._image_grid)
            _new_ic.image_data = doc.extract_image(xref)

        self._image_grid.update_display()
