import tkinter as tk
import time
root = tk.Tk()
root.title("Reloj_prueba")
root.config(width=500,height=500)

class App:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(master, text="", font=("Helvetica", 16))
        self.label.pack()
        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.master.after(1000, self.update_clock)
        
app = App(root)

class ven:
    def __init__(self, master):
        self.master = master
        self.button = tk.Button(master, text="Abrir ventana secundaria", command=self.open_window)
        self.button.pack()

    def open_window(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Ventana secundaria")
        new_window.geometry("200x200")
        new_window.mainloop()

root = tk.Tk()

ventana = ven(root)

root.mainloop()