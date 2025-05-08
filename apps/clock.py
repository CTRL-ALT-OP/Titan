import tkinter as d3
import time


class ClockApp:
    def __init__(self):
        self.time_lbl = None
        self.seconds_lbl = None
        self.date_lbl = None
        self.am_pm = None
        self.format_ = None
        self.root = None
        self.running = False
        self.time_format = 12

        # Fonts
        self.font_for_clock = ("Alien Encounters", 60, "bold")
        self.font_for_other = ("Alien Encounters", 20, "bold")
        self.font_for_other2 = ("Alien Encounters", 12, "bold")

    def update(self):
        if self.running:
            if self.time_format == 12:
                time_string = time.strftime("%I:%M")
                self.am_pm.configure(text=time.strftime("%p"))
            else:
                time_string = time.strftime("%H:%M")
                self.am_pm.configure(text="")

            seconds_string = time.strftime("%S")
            date_string = time.strftime("%A, %B %d, %G")

            self.time_lbl.configure(text=time_string)
            self.seconds_lbl.configure(text=seconds_string)
            self.date_lbl.configure(text=date_string)

            self.root.after(250, self.update)

    def change_format(self):
        if self.time_format == 12:
            self.time_format = 24
            self.format_.configure(text="24h")
        else:
            self.time_format = 12
            self.format_.configure(text="12h")

    def create_widgets(self, page):
        page.page_frame.configure(bg="black")

        with open("apps/_clock/settings.txt", "r") as f:
            settings = f.readlines()
            self.time_format = int(str.strip(settings[0], "\n"))

        time_string = "00:00"
        seconds_string = "00"
        date_string = ""

        self.time_lbl = d3.Label(
            page.page_frame, text=time_string, fg="lime green", bg="black", anchor="e"
        )
        self.time_lbl.place(
            relx=0.033, rely=0.27, relwidth=0.75, relheight=0.4, anchor="nw"
        )
        self.time_lbl.configure(font=self.font_for_clock)

        self.seconds_lbl = d3.Label(
            page.page_frame,
            text=seconds_string,
            fg="lime green",
            bg="black",
            justify="left",
            anchor="w",
        )
        self.seconds_lbl.place(relx=0.78, rely=0.424, width=45, relheight=0.2)
        self.seconds_lbl.configure(font=self.font_for_other)

        self.date_lbl = d3.Label(
            page.page_frame, text=date_string, fg="lime green", bg="black"
        )
        self.date_lbl.place(
            relx=0.5, rely=0.61, relwidth=0.9, relheight=0.1, anchor="center"
        )
        self.date_lbl.configure(font=self.font_for_other2)

        self.am_pm = d3.Label(page.page_frame, text="", fg="lime green", bg="black")
        self.am_pm.place(relx=0.8, rely=1, relwidth=0.15, relheight=0.2, anchor="sw")
        self.am_pm.configure(font=self.font_for_other)

        self.format_ = d3.Button(
            page.page_frame, text="", fg="red", bg="black", command=self.change_format
        )
        if self.time_format == 12:
            self.format_.configure(text="12h")
        else:
            self.format_.configure(text="24h")

        self.format_.configure(font=self.font_for_other)
        self.format_.place(relx=0, rely=1, relheight=0.18, relwidth=0.21, anchor="sw")

        self.running = True
        self.root.after(50, self.update)

    def destroy_app(self, page):
        self.running = False
        page.page_frame.destroy()
        with open("apps/_clock/settings.txt", "w") as f:
            self.root.update_idletasks()
            f.write(str(self.time_format))


# Module-level instance to maintain state
_clock_instance = None


def create(page, root_):
    global _clock_instance
    _clock_instance = ClockApp()
    _clock_instance.root = root_
    _clock_instance.create_widgets(page)


def destroy(page, root):
    global _clock_instance
    if _clock_instance:
        _clock_instance.destroy_app(page)
        _clock_instance = None
