
from tkinter import ttk as tw


class PDFSelector(tw.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._events = {
            "load_pdfs": [],
            "selection": [],
        }

        # interface
        self._cmb_pdfs = tw.Combobox(self)
        self._btn_load = tw.Button(self, text="Load PDFs")

        # styling
        self._cmb_pdfs.grid(column=0, row=0)
        self._btn_load.grid(column=1, row=0)
        self._cmb_pdfs.state(["readonly"])

        # register events
        self._cmb_pdfs.bind("<<ComboboxSelected>>", lambda _: self._event_fire("selection", self._cmb_pdfs.get()))
        self._btn_load.configure(command=lambda: self._event_fire("load_pdfs"))

    @property
    def pdf_options(self):
        return self._cmb_pdfs["values"]

    @pdf_options.setter
    def pdf_options(self, options):
        self._cmb_pdfs["values"] = options

    @property
    def event_names(self):
        return ", ".join([f"'{k}'" for k in self._events.keys()])

    def observe(self, event_name, func):
        if event_name not in self._events.keys():
            raise ValueError(
                f"Event {event_name} is unknown.  Known events include [{self.event_names}]")
        else:
            self._events[event_name].append(func)

    def _event_fire(self, event_name, *args, **kwargs):
        if event_name not in self._events.keys():
            raise ValueError(
                f"Event {event_name} is unknown.  Known events include [{self.event_names}]")
        else:
            for func in self._events[event_name]:
                func(*args, **kwargs)
