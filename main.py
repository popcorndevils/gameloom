import tkinter
import sv_ttk
import logging
import sys
from game_loom import get_resource_path
from game_loom import GameLoom

try:
    # only works during pyinstaller runtime.
    import pyi_splash # type: ignore # noqa
except ImportError:
    # This happens when running the script directly with Python
    pyi_splash = None
    logging.info("Game Loom running directly from code, not a build.")


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

if pyi_splash:
    pyi_splash.close()

# set theme
sv_ttk.set_theme("dark")
root.mainloop()
