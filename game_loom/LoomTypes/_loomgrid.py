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

    def get_xy(self, index):
        return (index % self.num_columns, index // self.num_columns)

    def clear_grid(self):
        self.columnconfigure(0, weight=0)
        for i, c in enumerate(self.winfo_children()):
            c.destroy()
            self.rowconfigure(i, weight=0)

    def update_display(self):
        _cols_config = []
        _rows_config = []

        for i, c in enumerate(self.winfo_children()):
            _x, _y = self.get_xy(i)
            c.grid(column=_x, row=_y, sticky="nsew")
            if _x not in _cols_config:
                self.columnconfigure(_x, weight=1)
            if _y not in _rows_config:
                self.rowconfigure(_y, weight=1)
