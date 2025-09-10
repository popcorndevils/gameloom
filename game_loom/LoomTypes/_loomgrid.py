from ._loomframe import LoomFrame


class LoomGrid(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._num_columns = 1
        self._num_rows = None
        self._padding = 0
        self._active_rows = []
        self._active_cols = []

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

    def get_xy(self, index):
        return (index % self.num_columns, index // self.num_columns)

    def clear_grid(self):
        for i, c in enumerate(self.winfo_children()):
            c.destroy()
        for c in range(self.grid_size()[0]):
            self.columnconfigure(c, weight=0, minsize=0)
        for r in range(self.grid_size()[1]):
            self.rowconfigure(r, weight=0, minsize=0)

    def update_display(self):
        for i, c in enumerate(self.winfo_children()):
            _x, _y = self.get_xy(i)
            c.grid(column=_x, row=_y, sticky="nsew")
            if _x not in self._active_cols:
                self.columnconfigure(_x, weight=1, uniform="group1")
            if _y not in self._active_rows:
                self.rowconfigure(_y, weight=1, uniform="group1")
