import tkinter as d3
from random import randint
import random

global moveable_box

# VARIABLE THAT HOLDS THE CURRENT X COORDINATE OF THE BOX
global curr_x
curr_x = 150


class BlockoidApp:
    def __init__(self):
        self.moveable_box = None
        self.curr_x = 150
        self.curr_y = 160
        self.landscape_y = []
        self.frames = []
        self.filler_frames = []

    def key_pressed(self, event):
        # GET THE CHARACTER THAT CORROSPONDS TO THE BUTTON PRESS
        k = str.lower(event.char)
        print(k)
        if k == "r":
            loading_screen_text = d3.Label(
                self.page.page_frame,
                text="LOADING...",
                bg="black",
                fg="lime green",
                activebackground="dark grey",
                font=("Alien Encounters", 20, "bold"),
            )
            loading_screen_text.place(relx=0.5, rely=0.5, anchor="center")
            self.page.page_frame.update()
            for block in self.frames:
                block.destroy()
            self.landscape_y = []
            i = 0

            prev_gen_y = 170
            while i < 30:
                gen_x = i * 10
                gen_y = 170
                # randomly decides whether to go up, down or straight (it has a built-in preference for straight so its kinda more normal)
                rand = random.randrange(1, 5)
                if rand == 1 or 4:
                    gen_y = prev_gen_y
                if rand == 2:
                    gen_y = prev_gen_y - 10
                    prev_gen_y = gen_y
                if rand == 3:
                    gen_y = prev_gen_y + 10
                    prev_gen_y = gen_y

                self.landscape_y.append(str(gen_y))
                i += 1

            # makes block
            i = 0
            self.frames = []

            while i < len(self.landscape_y):
                self.frames.append([])
                self.frames[i] = d3.Label(self.page.page_frame, bg="#363636")
                i += 1

            # FILLS IN UNDER GRASS BY GENERATING STRIPS OF COLOR THAT EXTEND FROM UNDER THE GRASS TO THE BOTTOM OF THE FRAME
            filler_x = 0
            filler_y = 290
            for column in self.filler_frames:
                for block in column:
                    try:
                        block.destroy()
                    except AttributeError:
                        column.remove(block)

            self.filler_frames = []

            while filler_x < 300:
                box_above = int(self.landscape_y[int(filler_x / 10)])
                filler_y = box_above + 10
                # CHANGE COLOR TO ANYTHING YOU LIKE -----.|
                #                                        V
                self.filler_frames.append([])
                self.frames[int(filler_x / 10)].place(
                    height=10,
                    width=10,
                    x=int(filler_x / 10) * 10,
                    y=int(self.landscape_y[int(filler_x / 10)]),
                )
                while filler_y < 300:
                    int_o = 0
                    curr_frame = d3.Label(self.page.page_frame, bg="black")
                    self.filler_frames[int(filler_x / 10)].append(curr_frame)
                    curr_frame.place(height=10, width=10, x=filler_x, y=filler_y)
                    self.page.page_frame.update()
                    filler_y += 10
                    int_o += 1

                filler_x += 10
            self.curr_y = int(self.landscape_y[15]) - 10

            # CREATE THE MOVEABLE BOX
            self.page.page_frame.update()
            loading_screen_text.destroy()
            self.page.page_frame.update()
            self.moveable_box.place(x=self.curr_x, y=self.curr_y)

        elif k == " ":
            # CHECKS IF THE BOX IS WITHIN THE BOUNDS AND CHANGES THE Y VALUE IF IT IS
            box_below = int(self.curr_x / 10)
            # v---- Makes sure that the player is jumping off a block, not air
            if int(self.landscape_y[(box_below)]) == (self.curr_y + 10):
                if self.curr_y > 0:
                    self.curr_y -= 10
            # MOVES THE BOX TO THE NEW LOCATION
            self.moveable_box.place(x=self.curr_x, y=self.curr_y)

        elif k == "a":
            if self.curr_x > 0:
                # CHECKS IF THE BOX IS WITHIN THE BOUNDS AND CHANGES THE X VALUE IF IT IS AND DEALS WITH GRAVITY

                # v---- Finds the box directly below the player
                box_below = int(self.curr_x / 10)

                # v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is straight
                if int(self.landscape_y[(box_below - 1)]) == (self.curr_y + 10):
                    self.curr_x -= 10

                # v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is blocking the player
                elif int(self.landscape_y[(box_below - 1)]) == (self.curr_y):
                    pass

                # v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is one block below the player
                elif int(self.landscape_y[(box_below - 1)]) == (self.curr_y + 20):
                    self.curr_x -= 10
                    self.curr_y += 10

                # v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is two blocks below the player (in case they are jumping off a ledge)
                elif int(self.landscape_y[(box_below - 1)]) == (self.curr_y + 30):
                    self.curr_x -= 10
                    self.curr_y += 20
                # MOVES THE BOX TO THE NEW LOCATION
                self.moveable_box.place(x=self.curr_x, y=self.curr_y)

        elif k == "d":
            if self.curr_x < 290:
                # CHECKS IF THE BOX IS WITHIN THE BOUNDS AND CHANGES THE X VALUE IF IT IS AND DEALS WITH GRAVITY
                box_below = int(self.curr_x / 10)

                # v---- Figures out whether the box below and to the left of the player (since that is where the player is moving) is straight
                if int(self.landscape_y[(box_below + 1)]) == (self.curr_y + 10):
                    self.curr_x += 10

                # v---- Figures out whether the box below and to the right of the player (since that is where the player is moving) is blocking the player
                elif int(self.landscape_y[(box_below + 1)]) == (self.curr_y):
                    pass

                # v---- Figures out whether the box below and to the right of the player (since that is where the player is moving) is one block below the player
                elif int(self.landscape_y[(box_below + 1)]) == (self.curr_y + 20):
                    self.curr_x += 10
                    self.curr_y += 10

                # v---- Figures out whether the box below and to the right of the player (since that is where the player is moving) is two blocks below the player (in case they are jumping off a ledge)
                elif int(self.landscape_y[(box_below + 1)]) == (self.curr_y + 30):
                    self.curr_x += 10
                    self.curr_y += 20
                # MOVES THE BOX TO THE NEW LOCATION
                self.moveable_box.place(x=self.curr_x, y=self.curr_y)

    def clouds(self):
        if self.running:
            if self.cloud1x < 260:
                self.cloud1x += 1
            else:
                self.cloud1x = 0
            self.cloud1.place(x=self.cloud1x, y=self.cloud1y)
            num = randint(600, 1100)
            self.root.after(num, self.clouds)

    def play(self, btn, lbl):
        btn.destroy()
        lbl.destroy()
        # VARIABLE THAT HOLDS THE CURRENT Y COORDINATE OF THE BOX
        self.curr_y = 160
        self.cloud1 = d3.Frame(self.page.page_frame, height=20, width=40, bg="dark red")
        self.cloud1x = 10
        self.cloud1y = 10
        self.landscape_y = []
        self.frames = []
        self.filler_frames = []
        self.moveable_box = d3.Frame(
            self.page.page_frame, height=10, width=10, bg="red"
        )
        self.running = True
        self.page.page_frame.configure(bg="dimgrey")
        loading_screen_text = d3.Label(
            self.page.page_frame,
            text="LOADING...",
            bg="black",
            fg="lime green",
            activebackground="dark grey",
            font=("Alien Encounters", 20, "bold"),
        )
        loading_screen_text.place(relx=0.5, rely=0.5, anchor="center")
        self.page.page_frame.update()

        # GENERATE LANDSCAPE
        #   v----- The list where the y_coordinates of all the blocks are stored
        self.landscape_y = []

        i = 0
        prev_gen_y = 170

        with open("apps/_blockoid/world.txt", "r") as f:
            self.landscape_y = f.readlines()
            i = 0
            while i < (len(self.landscape_y)):
                self.landscape_y[i] = self.landscape_y[i].strip("\n")
                i += 1

        if self.landscape_y == []:
            while i < 30:
                gen_x = i * 10
                gen_y = 170
                # randomly decides whether to go up, down or straight (it has a built-in preference for straight so its kinda more normal)
                rand = random.randrange(1, 5)
                if rand == 1 or 4:
                    gen_y = prev_gen_y
                if rand == 2:
                    gen_y = prev_gen_y - 10
                    prev_gen_y = gen_y
                if rand == 3:
                    gen_y = prev_gen_y + 10
                    prev_gen_y = gen_y

                self.landscape_y.append(str(gen_y))
                i += 1
            with open("world.txt", "w") as f:
                f.write("")
            with open("world.txt", "a") as f:
                i = 0
                while i < (len(self.landscape_y)):
                    f.write(self.landscape_y[i] + "\n")
                    i += 1

        # makes block
        i = 0
        self.frames = []

        while i < len(self.landscape_y):
            self.frames.append([])
            self.frames[i] = d3.Label(self.page.page_frame, bg="#363636")
            self.frames[i].place(
                height=10, width=10, x=i * 10, y=int(self.landscape_y[i])
            )
            self.page.page_frame.update()
            i += 1

        # FILLS IN UNDER GRASS BY GENERATING STRIPS OF COLOR THAT EXTEND FROM UNDER THE GRASS TO THE BOTTOM OF THE FRAME

        self.filler_frames = []
        filler_x = 0
        filler_y = 290

        while filler_x < 300:
            box_above = int(self.landscape_y[int(filler_x / 10)])
            filler_y = box_above + 10
            # CHANGE COLOR TO ANYTHING YOU LIKE -----------------------------------.|
            #                                                                                                                  V
            self.filler_frames.append([])
            while filler_y < 300:
                int_o = 0
                curr_frame = d3.Label(self.page.page_frame, bg="black")
                self.filler_frames[int(filler_x / 10)].append(curr_frame)
                curr_frame.place(height=10, width=10, x=filler_x, y=filler_y)
                filler_y += 10
                int_o += 1
                self.page.page_frame.update()

            filler_x += 10
        self.curr_y = int(self.landscape_y[15]) - 10

        # CREATE THE MOVEABLE BOX
        self.moveable_box = d3.Frame(
            self.page.page_frame, height=10, width=10, bg="red"
        )
        self.moveable_box.place(x=self.curr_x, y=self.curr_y)

        self.cloud1 = d3.Frame(self.page.page_frame, height=20, width=40, bg="dark red")

        self.cloud1x = 10

        self.cloud1y = 10
        self.cloud1.place(x=self.cloud1x, y=self.cloud1y)
        self.page.page_frame.update()
        loading_screen_text.destroy()
        self.page.page_frame.update()
        self.root.bind("<Key>", self.key_pressed)
        self.root.after(100, self.clouds)

    def create_widgets(self, page):
        self.running = False
        self.page = page
        self.page.page_frame.configure(bg="black")
        txt = d3.Label(
            page.page_frame,
            fg="lime green",
            bg="black",
            text="BLOCKOID",
            font=("Alien Encounters", 40, "bold"),
        )
        txt.place(relx=0.5, rely=0.3, anchor="center")
        play_btn = d3.Button(
            page.page_frame,
            text="PLAY",
            bg="black",
            fg="lime green",
            activebackground="dark grey",
            font=("Alien Encounters", 20, "bold"),
        )
        play_btn.configure(command=lambda pla=play_btn, lbl=txt: self.play(pla, lbl))
        play_btn.place(relx=0.5, rely=0.5, anchor="center")

    def destroy_app(self):
        if self.running:
            with open("apps/_blockoid/world.txt", "w") as f:
                f.write("")
            with open("apps/_blockoid/world.txt", "a") as f:
                i = 0
                while i < (len(self.landscape_y)):
                    f.write(self.landscape_y[i] + "\n")
                    i += 1

        self.running = False
        self.page.page_frame.destroy()


_blockoid_instance = None


def create(_page, _root):
    global _blockoid_instance
    _blockoid_instance = BlockoidApp()
    _blockoid_instance.root = _root
    _blockoid_instance.create_widgets(_page)


def destroy(page, root):
    global _blockoid_instance
    if _blockoid_instance:
        _blockoid_instance.destroy_app()
        _blockoid_instance = None
