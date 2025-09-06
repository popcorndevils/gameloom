import tkinter
import sv_ttk
import logging
import sys
from game_loom import get_resource_path
from game_loom import GameLoom


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

root = tkinter.Tk()

# set application icon
icon_path = get_resource_path("./res/logo_v2.ico")
root.iconbitmap(icon_path)

# configure window
root.title("Game Loom")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

gm_app = GameLoom(root)

# set theme
sv_ttk.set_theme("dark")

root.mainloop()
