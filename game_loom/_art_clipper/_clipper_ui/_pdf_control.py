
from tkinter import ttk as tw
from ...LoomTypes._loomframe import LoomEvent, LoomFrame


class PageIndex:
    def __init__(self, index = None, change = None):
        self.index = index
        self.change = change


class PDFControl(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # INTERFACE
        # frames
        self._frm_pdf_ctr = LoomFrame(self)
        self._frm_pg_ctr = LoomFrame(self)
        # pdf selector
        self._cmb_pdf_sel = tw.Combobox(self._frm_pdf_ctr)
        self._cmb_pdf_sel.state(["readonly"])
        self._btn_load = tw.Button(self._frm_pdf_ctr, text="Load PDFs")
        # page controls
        self._btn_pg_left = tw.Button(self._frm_pg_ctr, text="<")
        self._btn_pg_left_ten = tw.Button(self._frm_pg_ctr, text="<<")
        self._btn_pg_left_all = tw.Button(self._frm_pg_ctr, text="<<<")
        self._cmb_page_sel = tw.Combobox(self._frm_pg_ctr, width=3)
        self._cmb_page_sel.state(["readonly"])
        self._btn_pg_right = tw.Button(self._frm_pg_ctr, text=">")
        self._btn_pg_right_ten = tw.Button(self._frm_pg_ctr, text=">>")
        self._btn_pg_right_all = tw.Button(self._frm_pg_ctr, text=">>>")

        # STYLING
        # frames
        self._frm_pdf_ctr.grid(column=0, row=0, sticky="nw")
        self._frm_pg_ctr.grid(column=0, row=1, sticky="nw")
        # pdf select
        self._cmb_pdf_sel.grid(column=0, row=0)
        self._btn_load.grid(column=1, row=0)
        # page controls
        self._btn_pg_left_all.grid(column=0, row=0)
        self._btn_pg_left_ten.grid(column=1, row=0)
        self._btn_pg_left.grid(column=2, row=0)
        self._cmb_page_sel.grid(column=3, row=0)
        self._btn_pg_right.grid(column=4, row=0)
        self._btn_pg_right_ten.grid(column=5, row=0)
        self._btn_pg_right_all.grid(column=6, row=0)

        # EVENTS
        # definition
        self.register_event(LoomEvent("load_pdfs", None))
        self.register_event(LoomEvent("selection", ["selection"]))
        self.register_event(LoomEvent("page_select", ["page_index"]))

        # registration
        self._cmb_pdf_sel.bind(
            "<<ComboboxSelected>>",
            lambda _: self.fire_event("selection", selection=self._cmb_pdf_sel.get()))
        self._btn_load.configure(
            command=lambda: self.fire_event("load_pdfs"))
        self._btn_pg_left.configure(command=lambda: self._change_index(index=PageIndex(change=-1)))
        self._btn_pg_left_ten.configure(command=lambda: self._change_index(index=PageIndex(change=-10)))
        self._cmb_page_sel.bind("<<ComboboxSelected>>", lambda _: self._change_index(None))
        self._btn_pg_right.configure(command=lambda: self._change_index(index=PageIndex(change=1)))
        self._btn_pg_right_ten.configure(command=lambda: self._change_index(index=PageIndex(change=10)))

    @property
    def page_index(self):
        return int(self._cmb_page_sel.get()) - 1

    @page_index.setter
    def page_index(self, val: int):
        self._cmb_page_sel.set(str(val + 1))
        self._change_index(None)

    @property
    def pdf_selection(self):
        return self._cmb_pdf_sel.get()

    @property
    def pdf_options(self):
        return self._cmb_pdf_sel["values"]

    @pdf_options.setter
    def pdf_options(self, options):
        self._cmb_pdf_sel["values"] = options

    @property
    def num_pages(self):
        return len(self._cmb_page_sel["values"])

    @num_pages.setter
    def num_pages(self, val: int):
        self._cmb_page_sel["values"] = [i + 1 for i in range(val)]

    def _change_index(self, index: PageIndex = None):
        if index is None:
            self.fire_event("page_select", page_index=self.page_index)
        else:
            _new_index = self.page_index + index.change
            _new_index = min(max(_new_index, 0), self.num_pages)
            self.page_index = _new_index
