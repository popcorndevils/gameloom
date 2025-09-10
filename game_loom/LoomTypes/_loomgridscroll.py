import tkinter as tk
from tkinter import ttk
from ._loomframe import LoomFrame
from ._loomgrid import LoomGrid


class LoomGridScroll(LoomFrame):
    def __init__(self, *args, **kwargs):
        # ... (previous setup code is the same) ...
        super().__init__(*args, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._grid = LoomGrid(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self._grid, anchor="nw"
        )

        # --- MODIFIED BINDINGS ---
        self._grid.bind("<Configure>", self._on_grid_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_mousewheel()

    @property
    def num_columns(self):
        return self._grid.num_columns

    @num_columns.setter
    def num_columns(self, val):
        self._grid.num_columns = val

    @property
    def num_rows(self):
        return self._grid.num_rows

    @num_rows.setter
    def num_rows(self, val):
        self._grid.num_rows = val

    @property
    def display_grid(self):
        return self._grid

    def _on_grid_configure(self, event):
        # Update the scrollregion of the canvas to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # When the canvas resizes, update the width of the inner grid to match
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self):
        # ... (this method is unchanged) ...
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        # ... (this method is unchanged) ...
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def clear_grid(self):
        self._grid.clear_grid()
        # After clearing the grid, its size changes. We need to manually refresh the
        # scroll region to make the canvas and scrollbar update accordingly.
        self.refresh_scroll_region()

    def update_display(self):
        self._grid.update_display()

    def refresh_scroll_region(self):
        """
        Forces an update of the canvas scroll region and resets the view.
        """
        # Allow tkinter to process all pending events, including geometry changes
        self.update_idletasks()
        # Re-calculate the bounding box of all content on the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Scroll the canvas view back to the top
        self.canvas.yview_moveto(0)
