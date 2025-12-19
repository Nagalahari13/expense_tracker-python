import tkinter as tk
from gui.main_window import MainWindow
from gui.login_window import LoginWindow
from db.models import create_users_table, create_tables

def open_main_app(root, user_id):
    root=tk.Tk()
    root.geometry("900x600")
    MainWindow(root, user_id, open_main_app)
    root.mainloop()



if __name__ == "__main__":
    create_users_table()
    create_tables()

    root = tk.Tk()
    LoginWindow(root,open_main_app)

    
    root.mainloop()