import logging

from tkinter import filedialog
from tkinter import ttk as tw
from .filecabinet import FileCabinet


class PDFBrowser(tw.Frame):
    def __init__(self, root):
        logging.info("Loading PDFBrowser component.")
        super().__init__(root, padding=5)

        self._root = root
        self.grid(column=0, row=0, sticky="nesw")

        # pdf handler
        self._cabinet = FileCabinet()

        # configure frame layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(1, minsize=5)

        # Placeholder
        self._button1 = tw.Button(
            self,
            text="Load PDFs",
            command=self._handle_load_pdf
        )

        self._button2 = tw.Button(
            self,
            text="TEST BUTTON 2"
        )

        self._button1.grid(column=0, row=0, sticky="nesw")
        self._button2.grid(column=0, row=2, sticky="nesw")

    @property
    def root(self):
        return self._root

    def _handle_load_pdf(self):
        _files = filedialog.askopenfiles()
        self._cabinet.add([f.name for f in _files])
        logging.info(f"{len(_files)} files have been loaded.")
