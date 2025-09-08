from ._loomframe import LoomFrame


class LoomGrid(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._num_columns = 1
        self._num_rows = None
        self._padding = 0

    @property
    def num_columns(self):
        return self._num_columns

    @num_columns.setter
    def num_columns(self, val):
        self._num_columns = val

    @property
    def num_rows(self):
        return self._num_rows

    @num_rows.setter
    def num_rows(self, val):
        self._num_rows = val

    def clear_grid(self):
        self.columnconfigure(0, weight=0)
        for i, c in enumerate(self.winfo_children()):
            c.destroy()
            self.rowconfigure(i, weight=0)

    def update_display(self):
        self.columnconfigure(0, weight=1)
        for i, c in enumerate(self.winfo_children()):
            self.rowconfigure(i, weight=1)
            c.grid(column=0, row=i, sticky="nsew")
