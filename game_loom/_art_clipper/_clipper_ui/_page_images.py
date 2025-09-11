import logging
from tkinter import filedialog
from ._image_control import ImageControl
from tkinter import ttk as tw
from ...LoomTypes import LoomFrame, LoomGridScroll
from ._pdf_control import PDFControl
from ..filecabinet import PageObj


class PageImages(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cabinet = None
        self._image_grid = None
        self._no_images_label = None
        self.configure(padding=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # browser components
        self._selector = PDFControl(self)

        # styling
        self._selector.grid(column=0, row=0, sticky="w")

        # event handling
        self._selector.observe_event("load_pdfs", self._handle_load_pdfs)
        self._selector.observe_event("selection", self._handle_pdf_select)
        self._selector.observe_event("page_select", self._handle_page_select)

        # setup grid
        self._create_grid()

    @property
    def cabinet(self):
        return self._cabinet

    @cabinet.setter
    def cabinet(self, obj):
        self._cabinet = obj

    def _handle_load_pdfs(self):
        _files = filedialog.askopenfiles()
        for f in _files:
            self._cabinet.add(f)
        self._selector.pdf_options = self._cabinet.file_names
        logging.info(f"{len(_files)} files have been loaded.")

    def _handle_pdf_select(self, selection):
        doc = self._cabinet[selection]
        logging.info(f"New pdf '{selection}' selected. {doc.page_count} pages available.")
        self._selector.num_pages = doc.page_count
        self._selector.page_index = None

    def _handle_page_select(self, page_index):
        _doc = self._cabinet[self._selector.pdf_selection]
        page: PageObj = _doc[page_index]

        self._clear_grid()

        if not page.images:
            # If there are no images, display a message.
            self._no_images_label = tw.Label(self, text="No Images To Load", font=("Helvetica", 16, "bold"), anchor="center")
            self._no_images_label.grid(column=0, row=1, sticky="nsew")
        else:
            # Otherwise, create the grid and populate it with images.
            self._create_grid()
            for img in page:
                ImageControl(img, self._image_grid._grid)
            self._image_grid.update_display()

    def _create_grid(self):
        self._image_grid = LoomGridScroll(self)
        self._image_grid.grid(column=0, row=1, sticky="nsew")
        self._image_grid.num_columns = 3

    def _clear_grid(self):
        if self._image_grid:
            self._image_grid.destroy()
            self._image_grid = None
        if self._no_images_label:
            self._no_images_label.destroy()
            self._no_images_label = None
