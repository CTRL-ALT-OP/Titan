import tkinter as d3
from random import randint
import random

global moveable_box

#VARIABLE THAT HOLDS THE CURRENT X COORDINATE OF THE BOX
global curr_x
curr_x = 150
def key_pressed(event):
    global moveable_box
    global page
    global root
    global moveable_box
    global curr_x
    global curr_y
    global landscape_y
    global frames
    global filler_frames
    #GET THE CHARACTER THAT CORROSPONDS TO THE BUTTON PRESS
    k=str.lower(event.char)
    print(k)
    if k == "r":
        loading_screen_text = d3.Label(page.page_frame, text = "LOADING...", bg = "black",
                         fg = "lime green", activebackground = "dark grey",
                         font = ("Alien Encounters", 20, "bold"))
        loading_screen_text.place(relx = 0.5, rely = 0.5, anchor = "center")
        page.page_frame.update()
        for block in frames:
            block.destroy()
        landscape_y = []
        i = 0
        
        prev_gen_y = 170
        while i < 30:
            gen_x = i * 10
            gen_y = 170
            #randomly decides whether to go up, down or straight (it has a built-in preference for straight so its kinda more normal)
            rand = random.randrange(1,5)
            if rand == 1 or 4:
                gen_y = prev_gen_y
            if rand == 2:
                gen_y = prev_gen_y - 10
                prev_gen_y = gen_y
            if rand == 3:
                gen_y = prev_gen_y + 10
                prev_gen_y = gen_y
            
            landscape_y.append(str(gen_y))
            i+=1
        
    
        #makes block
        i = 0
        frames = []
        
        while i < len(landscape_y):
            frames.append([])
            frames[i] = d3.Label(page.page_frame,bg="#363636")
            i+=1
        
        #FILLS IN UNDER GRASS BY GENERATING STRIPS OF COLOR THAT EXTEND FROM UNDER THE GRASS TO THE BOTTOM OF THE FRAME
        filler_x = 0
        filler_y = 290
        for column in filler_frames:
            for block in column:
                try:
                    block.destroy()
                except AttributeError:
                    column.remove(block)
            
        filler_frames = []
        
        while filler_x < 300:
            box_above = int(landscape_y[int(filler_x/10)])
            filler_y = box_above + 10
            #CHANGE COLOR TO ANYTHING YOU LIKE -----.|
            #                                        V
            filler_frames.append([])
            frames[int(filler_x/10)].place(height=10,width=10,x = int(filler_x/10)*10, y = int(landscape_y[int(filler_x/10)]))
            while filler_y < 300:
                int_o = 0
                curr_frame = d3.Label(page.page_frame,bg="black")
                filler_frames[int(filler_x/10)].append(curr_frame)
                curr_frame.place(height=10,width=10,x = filler_x, y = filler_y)
                page.page_frame.update()
                filler_y += 10
                int_o += 1
            
            filler_x += 10
        curr_y = int(landscape_y[15]) - 10

        #CREATE THE MOVEABLE BOX
        page.page_frame.update()
        loading_screen_text.destroy()
        page.page_frame.update()
        moveable_box.place(x=curr_x, y=curr_y)
        
    elif k == " ":
        #CHECKS IF THE BOX IS WITHIN THE BOUNDS AND CHANGES THE Y VALUE IF IT IS
        box_below =int(curr_x/10)
        #v---- Makes sure that the player is jumping off a block, not air
        if int(landscape_y[(box_below)]) == (curr_y+10):
            if curr_y > 0:
                curr_y -= 10
        #MOVES THE BOX TO THE NEW LOCATION
        moveable_box.place(x=curr_x, y=curr_y)
    
    elif k == "a":
        if curr_x > 0:
            #CHECKS IF THE BOX IS WITHIN THE BOUNDS AND CHANGES THE X VALUE IF IT IS AND DEALS WITH GRAVITY
            
            #v---- Finds the box directly below the player
            box_below =int(curr_x/10)
            
            #v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is straight
            if int(landscape_y[(box_below-1)]) == (curr_y+10):
                curr_x -= 10
            
            #v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is blocking the player
            elif int(landscape_y[(box_below-1)]) == (curr_y):
                pass
            
            #v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is one block below the player
            elif int(landscape_y[(box_below-1)]) == (curr_y+20):
                curr_x -= 10
                curr_y += 10
            
            #v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is two blocks below the player (in case they are jumping off a ledge)
            elif int(landscape_y[(box_below-1)]) == (curr_y+30):
                curr_x -= 10
                curr_y += 20
            #MOVES THE BOX TO THE NEW LOCATION
            moveable_box.place(x=curr_x, y=curr_y)
        
    elif k == "d":
        if curr_x < 290:
            #CHECKS IF THE BOX IS WITHIN THE BOUNDS AND CHANGES THE X VALUE IF IT IS AND DEALS WITH GRAVITY
            box_below =int(curr_x/10)
            
            #v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is straight
            if int(landscape_y[(box_below+1)]) == (curr_y+10):
                curr_x += 10
            
            #v---- Figures out whether the box below and to the right of the player (since that is where the player is moving) is blocking the player
            elif int(landscape_y[(box_below+1)]) == (curr_y):
                pass
            
            #v---- Figures out whether the box below and to the right of the player (since that is where the player is moving) is one block below the player
            elif int(landscape_y[(box_below+1)]) == (curr_y+20):
                curr_x += 10
                curr_y += 10
            
            #v---- Figures out whether the box below and to the right of the player (since that is where the player is moving) is two blocks below the player (in case they are jumping off a ledge)
            elif int(landscape_y[(box_below+1)]) == (curr_y+30):
                curr_x += 10
                curr_y += 20
            #MOVES THE BOX TO THE NEW LOCATION
            moveable_box.place(x=curr_x, y=curr_y)

def clouds():
    global cloud1
    global cloud1x
    global cloud1y
    global root
    global running
    if running:
        if cloud1x < 260:
            cloud1x += 1
        else:
            cloud1x = 0
        cloud1.place(x=cloud1x, y=cloud1y)
        num = randint(600,1100)
        root.after(num,clouds)

def play(btn,lbl):
    btn.destroy()
    lbl.destroy()
    #VARIABLE THAT HOLDS THE CURRENT Y COORDINATE OF THE BOX
    global curr_y
    curr_y = 160
    global cloud1
    global cloud1x
    global cloud1y
    global landscape_y
    global frames
    global filler_frames
    global root
    global page
    global moveable_box
    global running
    running = True
    page.page_frame.configure(bg="dimgrey")
    loading_screen_text = d3.Label(page.page_frame, text = "LOADING...", bg = "black",
                         fg = "lime green", activebackground = "dark grey",
                         font = ("Alien Encounters", 20, "bold"))
    loading_screen_text.place(relx = 0.5, rely = 0.5, anchor = "center")
    page.page_frame.update()
        
    
    #GENERATE LANDSCAPE
    #   v----- The list where the y_coordinates of all the blocks are stored
    landscape_y = []
    
    i = 0
    prev_gen_y = 170
    
    with open("apps/_blockoid/world.txt","r") as f:
        landscape_y = f.readlines()
        i = 0
        while i < (len(landscape_y)):
            landscape_y[i] = landscape_y[i].strip('\n')
            i+=1
    
    if landscape_y == []:
        while i < 30:
            gen_x = i * 10
            gen_y = 170
            #randomly decides whether to go up, down or straight (it has a built-in preference for straight so its kinda more normal)
            rand = random.randrange(1,5)
            if rand == 1 or 4:
                gen_y = prev_gen_y
            if rand == 2:
                gen_y = prev_gen_y - 10
                prev_gen_y = gen_y
            if rand == 3:
                gen_y = prev_gen_y + 10
                prev_gen_y = gen_y
            
            landscape_y.append(str(gen_y))
            i+=1
        with open("world.txt","w") as f:
            f.write('')
        with open("world.txt","a") as f:
            i = 0
            while i < (len(landscape_y)):
                f.write(landscape_y[i]+'\n')
                i+=1
    
    #makes block
    i = 0
    frames = []
    
    while i < len(landscape_y):
        frames.append([])
        frames[i] = d3.Label(page.page_frame,bg="#363636")
        frames[i].place(height=10,width=10,x = i*10, y = int(landscape_y[i]))
        page.page_frame.update()
        i+=1
    
    #FILLS IN UNDER GRASS BY GENERATING STRIPS OF COLOR THAT EXTEND FROM UNDER THE GRASS TO THE BOTTOM OF THE FRAME
    
    filler_frames = []
    filler_x = 0
    filler_y = 290
        
    while filler_x < 300:
        box_above = int(landscape_y[int(filler_x/10)])
        filler_y = box_above + 10
        #CHANGE COLOR TO ANYTHING YOU LIKE -----------------------------------.|
        #                                                                                                                  V
        filler_frames.append([])
        while filler_y < 300:
            int_o = 0
            curr_frame = d3.Label(page.page_frame,bg="black")
            filler_frames[int(filler_x/10)].append(curr_frame)
            curr_frame.place(height=10,width=10,x = filler_x, y = filler_y)
            filler_y += 10
            int_o += 1
            page.page_frame.update()
            
        filler_x += 10
    curr_y = int(landscape_y[15]) - 10
    
    #CREATE THE MOVEABLE BOX
    moveable_box = d3.Frame(page.page_frame,height=10, width=10, bg="red")
    moveable_box.place(x=curr_x, y=curr_y)
    
    
    cloud1 = d3.Frame(page.page_frame,height=20, width=40, bg = "dark red")
    
    cloud1x = 10
    
    cloud1y = 10
    cloud1.place(x=cloud1x,y=cloud1y)
    page.page_frame.update()
    loading_screen_text.destroy()
    page.page_frame.update()
    root.bind("<Key>", key_pressed)
    root.after(100,clouds)
    
def create(_page, _root):
    global running
    running = False
    global root
    root = _root
    global page
    page = _page
    page.page_frame.configure(bg="black")
    txt = d3.Label(page.page_frame, fg = "lime green", bg = "black",
                   text = "BLOCKOID", font = ("Alien Encounters", 40, "bold"))
    txt.place(relx=0.5,rely=0.3,anchor = "center")
    play_btn = d3.Button(page.page_frame, text = "PLAY", bg = "black",
                         fg = "lime green", activebackground = "dark grey",
                         font = ("Alien Encounters", 20, "bold"))
    play_btn.configure(command = lambda pla = play_btn, lbl = txt: play(pla,lbl))
    play_btn.place(relx=0.5,rely=0.5,anchor = "center")
    
def destroy(page, root):
    global running
    if running:
        with open("apps/_blockoid/world.txt","w") as f:
            f.write('')
        with open("apps/_blockoid/world.txt","a") as f:
            i = 0
            while i < (len(landscape_y)):
                f.write(landscape_y[i]+'\n')
                i+=1
        
    running = False
    page.page_frame.destroy()
