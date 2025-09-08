
from tkinter import ttk as tw
from ...LoomTypes._loomframe import LoomEvent, LoomFrame


class PDFControl(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # interface
        self._frm_pdf_ctr = LoomFrame(self)
        self._frm_pg_ctr = LoomFrame(self)
        self._cmb_pdfs = tw.Combobox(self._frm_pdf_ctr)
        self._btn_load = tw.Button(self._frm_pdf_ctr, text="Load PDFs")
        self._lbl_placeholder = tw.Label(self._frm_pg_ctr, text="Placeholder")

        # styling
        self._frm_pdf_ctr.grid(column=0, row=0)
        self._frm_pg_ctr.grid(column=0, row=1)
        self._cmb_pdfs.grid(column=0, row=0)
        self._btn_load.grid(column=1, row=0)
        self._lbl_placeholder.grid(column=0, row=0)
        self._cmb_pdfs.state(["readonly"])

        # define events
        self.register_event(LoomEvent("load_pdfs", None))
        self.register_event(LoomEvent("selection", ["selection"]))

        # register events
        self._cmb_pdfs.bind(
            "<<ComboboxSelected>>", lambda _: self.fire_event("selection", selection=self._cmb_pdfs.get()))
        self._btn_load.configure(command=lambda: self.fire_event("load_pdfs"))

    @property
    def pdf_options(self):
        return self._cmb_pdfs["values"]

    @pdf_options.setter
    def pdf_options(self, options):
        self._cmb_pdfs["values"] = options
