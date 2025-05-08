import tkinter as d3


class StopwatchApp:
    def __init__(self):
        self.time_lbl = None
        self.hundredths_lbl = None
        self.start = None
        self.rst = None
        self.root = None
        self.running = False
        self.minutes = 0
        self.seconds = 0
        self.hundredths = 0

        # Fonts
        self.font_for_clock = ("Alien Encounters", 60, "bold")
        self.font_for_other = ("Alien Encounters", 20, "bold")
        self.font_for_other2 = ("Alien Encounters", 12, "bold")

    def reset(self):
        self.seconds = 0
        self.minutes = 0
        self.hundredths = 0
        time_string = "00:00"
        self.time_lbl.configure(text=time_string)

    def start_stop(self):
        self.running = not self.running
        if self.running:
            self.start.configure(text="Stop")
            self.update()
        else:
            self.start.configure(text="Start")

    def update(self):
        if self.running:
            self.hundredths += 1
            if self.hundredths >= 100:
                self.hundredths = 0
                self.seconds += 1
            if self.seconds >= 60:
                self.seconds = 0
                self.minutes += 1

            middle = ":"
            if self.seconds < 10:
                middle = ":0"

            if self.minutes < 10:
                if self.minutes == 0:
                    minut = "00"
                else:
                    minut = "0" + str(self.minutes)
            else:
                minut = str(self.minutes)

            if self.hundredths < 10:
                if self.hundredths == 0:
                    hundredt = "00"
                else:
                    hundredt = "0" + str(self.hundredths)
            else:
                hundredt = str(self.hundredths)

            time_string = str(minut) + middle + str(self.seconds)
            hundredths_string = "." + str(hundredt)

            self.time_lbl.configure(text=time_string)
            self.hundredths_lbl.configure(text=hundredths_string)

        if self.running:
            self.root.after(10, self.update)

    def create_widgets(self, page):
        page.page_frame.configure(bg="black")

        with open("apps/_clock/settings.txt", "r") as f:
            settings = f.readlines()
            self.time_format = int(str.strip(settings[0], "\n"))

        time_string = "00:00"
        hundredths_string = ".00"

        self.time_lbl = d3.Label(
            page.page_frame, text=time_string, fg="lime green", bg="black", anchor="e"
        )
        self.time_lbl.place(
            relx=0.033, rely=0.27, relwidth=0.75, relheight=0.4, anchor="nw"
        )
        self.time_lbl.configure(font=self.font_for_clock)

        self.hundredths_lbl = d3.Label(
            page.page_frame,
            text=hundredths_string,
            fg="lime green",
            bg="black",
            justify="left",
            anchor="w",
        )
        self.hundredths_lbl.place(relx=0.78, rely=0.424, width=45, relheight=0.2)
        self.hundredths_lbl.configure(font=self.font_for_other)

        self.start = d3.Button(
            page.page_frame,
            text="Start",
            fg="lime green",
            bg="black",
            command=self.start_stop,
        )
        self.start.configure(font=self.font_for_other)
        self.start.place(
            relx=0.75, rely=0.9, relheight=0.2, relwidth=0.3, anchor="center"
        )

        self.rst = d3.Button(
            page.page_frame,
            text="Reset",
            fg="lime green",
            bg="black",
            command=self.reset,
        )
        self.rst.configure(font=self.font_for_other)
        self.rst.place(
            relx=0.25, rely=0.9, relheight=0.2, relwidth=0.3, anchor="center"
        )

    def destroy_app(self, page):
        self.running = False
        page.page_frame.destroy()
        with open("apps/_clock/settings.txt", "w") as f:
            self.root.update_idletasks()
            f.write(str(self.time_format))


# Module-level instance to maintain state
_stopwatch_instance = None


def create(page, root_):
    global _stopwatch_instance
    _stopwatch_instance = StopwatchApp()
    _stopwatch_instance.root = root_
    _stopwatch_instance.create_widgets(page)


def destroy(page, root):
    global _stopwatch_instance
    if _stopwatch_instance:
        _stopwatch_instance.destroy_app(page)
        _stopwatch_instance = None
