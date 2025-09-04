__version__ = "0.0.2-alpha"

import tkinter
import sv_ttk
import logging
import sys
from gm_copilot import GMCopilot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

root = tkinter.Tk()

gm_app = GMCopilot(root)

# set theme
sv_ttk.set_theme("dark")

root.mainloop()
