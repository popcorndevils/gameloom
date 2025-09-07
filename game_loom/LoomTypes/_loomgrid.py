from ._loomframe import LoomFrame


class LoomGrid(LoomFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._num_columns = 1
        self._num_rows = None

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
