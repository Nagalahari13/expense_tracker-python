import tkinter as tk
from gui.login_window import LoginWindow
from database.db import create_tables


create_tables()


root = tk.Tk()

LoginWindow(root)

root.mainloop()