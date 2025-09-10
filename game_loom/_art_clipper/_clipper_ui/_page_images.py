import logging
from tkinter import filedialog
from ._image_control import ImageControl
from ...LoomTypes import LoomFrame, LoomGridScroll
from ._pdf_control import PDFControl


class PageImages(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cabinet = None
        self.configure(padding=5)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # browser components
        self._selector = PDFControl(self)
        self._image_grid = LoomGridScroll(self)

        # styling
        self._selector.grid(column=0, row=0, sticky="w")
        self._image_grid.grid(column=0, row=1, sticky="nsew")
        self._image_grid.num_columns = 3

        # event handling
        self._selector.observe_event("load_pdfs", self._handle_load_pdfs)
        self._selector.observe_event("selection", self._handle_pdf_select)
        self._selector.observe_event("page_select", self._handle_page_select)

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
        logging.info(f"New pdf '{selection}' selected. {len(doc)} pages available.")
        self._selector.num_pages = len(doc)
        self._selector.page_index = None

    def _handle_page_select(self, page_index):
        _doc = self._cabinet[self._selector.pdf_selection]
        _page = _doc[page_index]
        _img_list = _page.get_images(full=True)
        self._image_grid.clear_grid()

        for img in _img_list:
            xref = img[0]
            _new_ic = ImageControl(self._image_grid._grid, max_height_container=self._image_grid)
            _new_ic.image_data = _doc.extract_image(xref)

        self._image_grid.update_display()
        # self._image_grid.refresh_scroll_region()
