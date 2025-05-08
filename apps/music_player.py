import tkinter as d3

global font_default
font_default = ("Alien Encounters", 60, "bold")

global state
state = False

def play():
    global pause_play
    global state

    if state:
        pause_play.configure(text = "\u23F5")
    else:
        pause_play.configure(text = "\u23F8")
    state = not state

def create(page, root):
    page.page_frame.configure(bg = "black")
    global pause_play
    pause_play = d3.Button(page.page_frame, text = "\u23F5",font = font_default,command = play)
    pause_play.place(relx=0.5,rely=0.8,relheight=0.2,relwidth=.2,anchor = "center")

def destroy(page, root):
    page.page_frame.destroy()
