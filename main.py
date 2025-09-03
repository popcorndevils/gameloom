import tkinter
import sv_ttk

from gm_assist import GMAssist

root = tkinter.Tk()

gm_app = GMAssist(root)

# set theme
sv_ttk.set_theme("dark")

root.mainloop()
