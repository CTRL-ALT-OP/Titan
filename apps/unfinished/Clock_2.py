from tkinter import Button, Label, Canvas, Tk, StringVar, Frame, font, Toplevel, EventType, PhotoImage
import time as time


root = Tk()
global font_for_clock
font_for_clock = ("Alien Encounters", 12, "bold")

global font_for_other
font_for_other = ("Alien Encounters", 12, "bold")
global canvas


def resize(event):
    global font_for_clock
    global font_for_other
    font_for_other = ("Alien Encounters", int(root.winfo_height()/7), "bold")
    font_for_clock = ("Alien Encounters", int(root.winfo_height()/1.8), "bold")
    timelbl.configure(font=font_for_clock)
    format.configure(font=font_for_other)
    close.configure(font=font_for_other)
    am_pm.configure(font=font_for_other)


lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - \
        lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x, y))


def OnMotion(event):
    x1 = root.winfo_pointerx()
    y1 = root.winfo_pointery()
    x0 = root.winfo_rootx()
    y0 = root.winfo_rooty()
    if y1-y0 >= 40:
        root.geometry("%sx%s" % ((int(root.winfo_height()*2.5)), (y1-y0)))


def exit():
    global time_format
    global root
    with open("settings.txt", "w") as f:
        root.update_idletasks()
        f.write(str(int(root.winfo_width()*0.985))
                + "\n"
                + str(int(root.winfo_height()**0.985))
                + "\n"
                + str(root.winfo_x())
                + "\n"
                + str(root.winfo_y())
                + "\n"
                + str(time_format))
    root.destroy()
    quit()


global time_format


def toggle(event):
    if event.type == EventType.Map:
        root.deiconify()
    else:
        root.withdraw()


canvas = Canvas(root, width=3, height=2)
time_format = 12

root.bind('<Configure>', resize)
root.config(bg="black")
canvas.pack()
root.wait_visibility(root)
root.wm_attributes('-alpha', 0.8)
root.wm_attributes('-topmost', True)
root.overrideredirect(1)
root.protocol("WM_DELETE_WINDOW", exit)

top = Toplevel(root)
top.geometry('0x0+10000+10000')  # make it not visible
# close root window if toplevel is closed
top.protocol('WM_DELETE_WINDOW', exit)
iconimage = PhotoImage(file="icon.png")
top.iconphoto(False, iconimage)


global time_string
time_string = time.strftime('%I:%M')


def update():
    global time_string
    global timelbl
    global canvas
    global time_format
    if time_format == 12:
        time_string = time.strftime("%I:%M")
        am_pm.configure(text=time.strftime("%p"))
    else:
        time_string = time.strftime("%H:%M")
        am_pm.configure(text="")
    timelbl.configure(text=time_string)
    root.after(250, update)


def change_format():
    global time_format
    if time_format == 12:
        time_format = 24
        format.configure(text="24h")
    else:
        time_format = 12
        format.configure(text="12h")


frame = Frame(root, bg="black")
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

global timelbl
timelbl = Label(root, text=time_string, fg="lime green", bg="black")
timelbl.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
timelbl.configure(font=font_for_clock)

global am_pm
am_pm = Label(root, text=time_string, fg="lime green", bg="black")
am_pm.place(relx=0.3, rely=1, relwidth=0.15, relheight=0.2, anchor="sw")
am_pm.configure(font=font_for_other)

timelbl.bind('<Button-1>', SaveLastClickPos)
timelbl.bind('<B1-Motion>', Dragging)

grip = Frame(root, cursor="sizing", bg="black")
grip.place(relx=1.0, rely=1.0, relheight=0.05, relwidth=0.05, anchor="se")
grip.bind("<B1-Motion>", OnMotion)

close = Button(root, text="X", fg="red", bg="black", command=exit)
close.configure(font=font_for_other)
close.place(relx=1, rely=0, relheight=.18, relwidth=(.18/2.5), anchor="ne")

format = Button(root, text="", fg="red", bg="black", command=change_format)
if time_format == 12:
    format.configure(text="12h")
else:
    format.configure(text="24h")

format.configure(font=font_for_other)
format.place(relx=0, rely=1, relheight=.18, relwidth=0.21, anchor="sw")

with open("settings.txt", "r") as f:
    settings = f.readlines()
    canvas.configure(width=int(str.strip(settings[0], "\n")),
                     height=int(str.strip(settings[1], "\n")),
                     bg="black")
    resize(False)
    root.geometry("+%s+%s" % (int(str.strip(settings[2], "\n")),
                              int(str.strip(settings[3], "\n"))))
    time_format = int(str.strip(settings[4], "\n"))

update()
root.mainloop()
