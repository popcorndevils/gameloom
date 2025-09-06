import io
import logging

from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk as tw
from .filecabinet import FileCabinet
from ._clipper_ui import PDFSelector


class ArtClipper(tw.Frame):
    def __init__(self, root):
        logging.info("Loading ArtClipper.")
        super().__init__(root, padding=5)
        self._original_image = None
        self._tk_image = None

        self._root = root

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # pdf handler
        self._cabinet = FileCabinet()

        # browser components
        self._selector = PDFSelector(self)

        # styling
        self._selector.grid(column=0, row=0, sticky="w")

        # event handling
        self._selector.observe_event("load_pdfs", self._handle_load_pdfs)
        self._selector.observe_event("selection", self._handle_pdf_select)

        # image testing
        self._fr_image = tw.Frame(self)
        self._fr_image.rowconfigure(0, weight=1)
        self._fr_image.grid(column=0, row=1, sticky="nsew")

        self._lbl_image = tw.Label(self._fr_image, text="HELLO THERE")
        self._lbl_image.grid(column=0, row=0, sticky="nsew")

        self._fr_image.bind("<Configure>", self._resize_image)

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
        xref = img_list[0][0]
        base_image = doc.extract_image(xref)
        image_data = base_image["image"]
        image_stream = io.BytesIO(image_data)
        self._original_image = Image.open(image_stream)

        self._resize_image(None)

    def _resize_image(self, event):
        if self._original_image:
            fr_w = self._fr_image.winfo_width()
            fr_h = self._fr_image.winfo_height()

            if fr_w > 0 and fr_h > 0:
                ori_w, ori_h = self._original_image.size
                ratio = min(fr_w / ori_w, fr_h / ori_h)
                new_width = int(ori_w * ratio)
                new_height = int(ori_h * ratio)
                resized_image = self._original_image.resize((new_width, new_height), Image.LANCZOS)
                self._tk_image = ImageTk.PhotoImage(resized_image)

                self._lbl_image.configure(image=self._tk_image)
                self._lbl_image.image = self._tk_image
