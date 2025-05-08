from tkinter import *

root = Tk()

root.wm_attributes("-topmost","1")

canvas = Canvas(root,width=100,height=100).pack()

global time
time = 3600

global timer_str
timer_str = Label(root, text = str(time),font=("Helvetica", 20))
timer_str.pack()

def timer():
    global time
    global timer_str
    time -= 1
    timer_str.configure(text = str(time))
    root.after(1000,timer)

timer()
root.mainloop()