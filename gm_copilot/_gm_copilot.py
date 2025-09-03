import tkinter as tk
from tkinter import ttk as tw


class GMCopilot:
    def __init__(self, root):
        self.root = root

        # configure root
        self.root.title("GM Assist")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._view_main = tw.Frame(self.root, padding=(5, 5, 5, 5))
        self._view_main.columnconfigure(0, weight=1)
        self._view_main.rowconfigure(0, weight=1)
        self._view_main.rowconfigure(1, weight=1)

        self._label = tw.Label(self._view_main, text="THIS IS A LABEL")
        self._button = tw.Button(self._view_main, text="HELLO")

        # set grids
        self._view_main.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self._label.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self._button.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.W, tk.E))
