import tkinter
import sv_ttk
import logging
import sys
from gmcopilot import GMCopilot

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
