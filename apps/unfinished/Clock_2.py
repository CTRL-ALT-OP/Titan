from tkinter import (
    Button,
    Label,
    Canvas,
    Tk,
    StringVar,
    Frame,
    font,
    Toplevel,
    EventType,
    PhotoImage,
)
import time as time


class Clock:
    def __init__(self):
        self.root = Tk()
        self.font_for_clock = ("Alien Encounters", 12, "bold")
        self.font_for_other = ("Alien Encounters", 12, "bold")
        self.time_format = 12
        self.time_string = time.strftime("%I:%M")
        self.lastClickX = 0
        self.lastClickY = 0

        self.setup_ui()
        self.load_settings()
        self.update()

    def setup_ui(self):
        self.canvas = Canvas(self.root, width=3, height=2)

        self.root.bind("<Configure>", self.resize)
        self.root.config(bg="black")
        self.canvas.pack()
        self.root.wait_visibility(self.root)
        self.root.wm_attributes("-alpha", 0.8)
        self.root.wm_attributes("-topmost", True)
        self.root.overrideredirect(1)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.top = Toplevel(self.root)
        self.top.geometry("0x0+10000+10000")  # make it not visible
        # close root window if toplevel is closed
        self.top.protocol("WM_DELETE_WINDOW", self.exit)
        # iconimage = PhotoImage(file="icon.png")
        # self.top.iconphoto(False, iconimage)

        self.frame = Frame(self.root, bg="black")
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.timelbl = Label(
            self.root, text=self.time_string, fg="lime green", bg="black"
        )
        self.timelbl.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        self.timelbl.configure(font=self.font_for_clock)

        self.am_pm = Label(
            self.root, text=self.time_string, fg="lime green", bg="black"
        )
        self.am_pm.place(relx=0.3, rely=1, relwidth=0.15, relheight=0.2, anchor="sw")
        self.am_pm.configure(font=self.font_for_other)

        self.timelbl.bind("<Button-1>", self.SaveLastClickPos)
        self.timelbl.bind("<B1-Motion>", self.Dragging)

        self.grip = Frame(self.root, cursor="sizing", bg="black")
        self.grip.place(relx=1.0, rely=1.0, relheight=0.05, relwidth=0.05, anchor="se")
        self.grip.bind("<B1-Motion>", self.OnMotion)

        self.close = Button(
            self.root, text="X", fg="red", bg="black", command=self.exit
        )
        self.close.configure(font=self.font_for_other)
        self.close.place(
            relx=1, rely=0, relheight=0.18, relwidth=(0.18 / 2.5), anchor="ne"
        )

        self.format = Button(
            self.root, text="", fg="red", bg="black", command=self.change_format
        )
        if self.time_format == 12:
            self.format.configure(text="12h")
        else:
            self.format.configure(text="24h")

        self.format.configure(font=self.font_for_other)
        self.format.place(relx=0, rely=1, relheight=0.18, relwidth=0.21, anchor="sw")

    def resize(self, event):
        self.font_for_other = (
            "Alien Encounters",
            int(self.root.winfo_height() / 7),
            "bold",
        )
        self.font_for_clock = (
            "Alien Encounters",
            int(self.root.winfo_height() / 1.8),
            "bold",
        )
        self.timelbl.configure(font=self.font_for_clock)
        self.format.configure(font=self.font_for_other)
        self.close.configure(font=self.font_for_other)
        self.am_pm.configure(font=self.font_for_other)

    def SaveLastClickPos(self, event):
        self.lastClickX = event.x
        self.lastClickY = event.y

    def Dragging(self, event):
        x, y = (
            event.x - self.lastClickX + self.root.winfo_x(),
            event.y - self.lastClickY + self.root.winfo_y(),
        )
        self.root.geometry("+%s+%s" % (x, y))

    def OnMotion(self, event):
        x1 = self.root.winfo_pointerx()
        y1 = self.root.winfo_pointery()
        x0 = self.root.winfo_rootx()
        y0 = self.root.winfo_rooty()
        if y1 - y0 >= 40:
            self.root.geometry(
                "%sx%s" % ((int(self.root.winfo_height() * 2.5)), (y1 - y0))
            )

    def exit(self):
        with open("settings.txt", "w") as f:
            self.root.update_idletasks()
            f.write(
                str(int(self.root.winfo_width() * 0.985))
                + "\n"
                + str(int(self.root.winfo_height() ** 0.985))
                + "\n"
                + str(self.root.winfo_x())
                + "\n"
                + str(self.root.winfo_y())
                + "\n"
                + str(self.time_format)
            )
        self.root.destroy()
        quit()

    def toggle(self, event):
        if event.type == EventType.Map:
            self.root.deiconify()
        else:
            self.root.withdraw()

    def update(self):
        if self.time_format == 12:
            self.time_string = time.strftime("%I:%M")
            self.am_pm.configure(text=time.strftime("%p"))
        else:
            self.time_string = time.strftime("%H:%M")
            self.am_pm.configure(text="")
        self.timelbl.configure(text=self.time_string)
        self.root.after(250, self.update)

    def change_format(self):
        if self.time_format == 12:
            self.time_format = 24
            self.format.configure(text="24h")
        else:
            self.time_format = 12
            self.format.configure(text="12h")

    def load_settings(self):
        try:
            with open("settings.txt", "r") as f:
                settings = f.readlines()
                self.canvas.configure(
                    width=int(str.strip(settings[0], "\n")),
                    height=int(str.strip(settings[1], "\n")),
                    bg="black",
                )
                self.resize(False)
                self.root.geometry(
                    "+%s+%s"
                    % (
                        int(str.strip(settings[2], "\n")),
                        int(str.strip(settings[3], "\n")),
                    )
                )
                self.time_format = int(str.strip(settings[4], "\n"))
        except:
            # Handle case where settings file doesn't exist or is invalid
            pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    clock = Clock()
    clock.run()
