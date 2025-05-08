import tkinter as d3
import time

global time_lbl
global date_lbl
global root
global running
running = False

global font_for_clock
font_for_clock = ("Alien Encounters", 60, "bold")

global font_for_other
font_for_other = ("Alien Encounters", 20, "bold")

global font_for_other2
font_for_other2 = ("Alien Encounters", 12, "bold")

def update():
    global seconds_lbl
    global time_lbl
    global date_lbl
    global root
    global running
    global time_format
    global time_string
    global seconds_string
    global date_string
    global am_pm
    
    if running:
        if time_format == 12:
            time_string = time.strftime("%I:%M")
            am_pm.configure(text=time.strftime("%p"))
        else:
            time_string = time.strftime("%H:%M")
            am_pm.configure(text="")
        seconds_string = time.strftime("%S")
        date_string = time.strftime("%A, %B %d, %G")
        time_lbl.configure(text=time_string)
        seconds_lbl.configure(text=seconds_string)
        date_lbl.configure(text=date_string)
        root.after(250, update)

def change_format():
    global time_format
    global format_
    
    if time_format == 12:
        time_format = 24
        format_.configure(text="24h")
    else:
        time_format = 12
        format_.configure(text="12h")

    
def create(page, root_):
    global time_lbl
    global seconds_lbl
    global date_lbl
    global root
    global running
    global time_format
    global time_string
    global seconds_string
    global date_string
    page.page_frame.configure(bg = "black")
    with open("apps/_clock/settings.txt", "r") as f:
        settings = f.readlines()
        time_format = int(str.strip(settings[0], "\n"))
    root = root_
    time_string = "00:00"
    seconds_string = "00"
    date_string = ""
    
    global time_lbl
    time_lbl = d3.Label(page.page_frame, text=time_string, fg="lime green", bg="black", anchor = "e")
    time_lbl.place(relx=0.033, rely=0.27, relwidth=0.75, relheight=0.4, anchor = "nw")
    time_lbl.configure(font=font_for_clock)


    global seconds_lbl
    seconds_lbl = d3.Label(page.page_frame, text=seconds_string, fg="lime green", bg="black", justify = "left", anchor = "w")
    seconds_lbl.place(relx=0.78, rely=0.424, width=45, relheight=0.2)
    seconds_lbl.configure(font=font_for_other)
    
    date_lbl = d3.Label(page.page_frame, text=date_string, fg="lime green", bg="black")
    date_lbl.place(relx=0.5, rely=0.61, relwidth=0.9, relheight=0.1, anchor = "center")
    date_lbl.configure(font=font_for_other2)
    
    global am_pm
    am_pm = d3.Label(page.page_frame, text=time_string, fg="lime green", bg="black")
    am_pm.place(relx=0.8, rely=1, relwidth=0.15, relheight=0.2, anchor="sw")
    am_pm.configure(font=font_for_other)

    global format_
    format_ = d3.Button(page.page_frame, text="", fg="red", bg="black", command=change_format)
    if time_format == 12:
        format_.configure(text="12h")
    else:
        format_.configure(text="24h")
    
    format_.configure(font=font_for_other)
    format_.place(relx=0, rely=1, relheight=.18, relwidth=0.21, anchor="sw")


    running = True
    root.after(50,update)

def destroy(page, root):
    global running
    running = False
    page.page_frame.destroy()
    with open("apps/_clock/settings.txt", "w") as f:
        root.update_idletasks()
        f.write(str(time_format))






