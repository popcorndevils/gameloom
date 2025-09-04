__version__ = "0.0.2-alpha"

import tkinter
import sv_ttk

from gm_copilot import GMCopilot

root = tkinter.Tk()

gm_app = GMCopilot(root)

# set theme
sv_ttk.set_theme("dark")

root.mainloop()
