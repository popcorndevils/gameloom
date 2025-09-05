import tkinter
import sv_ttk
import logging
import sys
from game_loom import GameLoom

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

root = tkinter.Tk()

gm_app = GameLoom(root)

# set theme
sv_ttk.set_theme("dark")

root.mainloop()
