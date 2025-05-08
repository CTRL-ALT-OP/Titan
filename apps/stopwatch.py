import tkinter as d3
import time

global time_lbl
global date_lbl
global root
global running

global minutes
global seconds
global hundredths
minutes = 0
seconds = 0
hundredths = 0
running = False

global font_for_clock
font_for_clock = ("Alien Encounters", 60, "bold")

global font_for_other
font_for_other = ("Alien Encounters", 20, "bold")

global font_for_other2
font_for_other2 = ("Alien Encounters", 12, "bold")

def reset():
    global time_string
    global time_lbl
    global time_format
    global minutes
    global seconds
    global hundredths
    seconds = 0
    minutes = 0
    hundredths = 0
    time_string = "00:00"
    time_lbl.configure(text=time_string)

def start_stop():
    global start
    global running 
    running = not running
    if running == True:
        start.configure(text = "Stop")
        update()
    else:
        start.configure(text = "Start")


def update():
    global time_lbl
    global date_lbl
    global root
    global running
    global time_format
    global time_string
    global date_string
    global am_pm
    global minutes
    global seconds
    global hundredths
    global hundredths_string
    global hundredths_lbl
    global running
    hundredt = ""
    if running:
        hundredths += 1
        if hundredths >= 100:
            hundredths = 0
            seconds += 1
        if seconds >= 60:
            seconds = 0
            minutes += 1
        middle = ":"
        if seconds < 10:
            middle = ":0"
        if minutes < 10:
            if minutes == 0:
                minut = "00"
            else:
                minut = "0"+str(minutes)
        else:
            minut = str(minutes)
        if hundredths < 10:
            if hundredths == 0:
                hundredt = "00"
            else:
                hundredt = "0"+str(hundredths)
        else:
            hundredt = str(hundredths)
        time_string = str(minut)+middle+str(seconds)
        hundredths_string = "."+str(hundredt)
        minutes = int(minutes)
        time_lbl.configure(text=time_string)
        hundredths_lbl.configure(text=hundredths_string)
    if running:
        root.after(10, update)
 
def create(page, root_):
    global time_lbl
    global date_lbl
    global root
    global running
    global time_format
    global time_string
    global hundredths_string
    
    page.page_frame.configure(bg = "black")
    with open("apps/_clock/settings.txt", "r") as f:
        settings = f.readlines()
        time_format = int(str.strip(settings[0], "\n"))
    root = root_
    time_string = "00:00"
    hundredths_string = ".00"
    date_string = ""
    
    global time_lbl
    time_lbl = d3.Label(page.page_frame, text=time_string, fg="lime green", bg="black", anchor = "e")
    time_lbl.place(relx=0.033, rely=0.27, relwidth=0.75, relheight=0.4, anchor = "nw")
    time_lbl.configure(font=font_for_clock)


    global hundredths_lbl
    hundredths_lbl = d3.Label(page.page_frame, text=hundredths_string, fg="lime green", bg="black", justify = "left", anchor = "w")
    hundredths_lbl.place(relx=0.78, rely=0.424, width=45, relheight=0.2)
    hundredths_lbl.configure(font=font_for_other)

    
    global start
    start = d3.Button(page.page_frame,text="Start",fg = "lime green",bg="black",command = start_stop)
    start.configure(font=font_for_other)
    start.place(relx=0.75, rely=.9, relheight= .2, relwidth = .3, anchor="center")
    
    global rst
    rst = d3.Button(page.page_frame,text="Reset",fg = "lime green",bg="black",command = reset)
    rst.configure(font=font_for_other)
    rst.place(relx=0.25, rely=.9, relheight= .2, relwidth = .3, anchor="center")

def destroy(page, root):
    global running
    running = False
    page.page_frame.destroy()
    with open("apps/_clock/settings.txt", "w") as f:
        root.update_idletasks()
        f.write(str(time_format))
