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

gameloom_icon = tkinter.PhotoImage(file="./res/logo_icon.png")

root.title("Game Loom")
root.iconphoto(False, gameloom_icon)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

gm_app = GameLoom(root)

# set theme
sv_ttk.set_theme("dark")

root.mainloop()
