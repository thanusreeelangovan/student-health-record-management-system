import tkinter as tk
from gui import HealthApp
from db import create_table

create_table()

root = tk.Tk()
app = HealthApp(root)
root.mainloop()
