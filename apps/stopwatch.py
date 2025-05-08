import tkinter as d3
import time
from config import config


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
        self.start_time = 0
        self.elapsed_time = 0
        self.paused_time = 0

        # Fonts using config
        self.font_for_clock = (
            config["ui"].FONT_FAMILY,
            config["clock"].CLOCK_MAIN_FONT_SIZE,
            "bold",
        )
        self.font_for_other = (
            config["ui"].FONT_FAMILY,
            config["clock"].CLOCK_SECONDARY_FONT_SIZE,
            "bold",
        )
        self.font_for_other2 = (
            config["ui"].FONT_FAMILY,
            config["clock"].CLOCK_TERTIARY_FONT_SIZE,
            "bold",
        )

    def reset(self):
        # Save the current running state
        was_running = self.running

        # Reset time values
        self.start_time = time.time()
        self.elapsed_time = 0
        self.paused_time = 0
        self.minutes = 0
        self.seconds = 0
        self.hundredths = 0

        # Update display
        time_string = "00:00"
        self.time_lbl.configure(text=time_string)
        hundredths_string = ".00"
        self.hundredths_lbl.configure(text=hundredths_string)

        # If it was running, keep it running with the new start time
        if was_running:
            self.update()

    def start_stop(self):
        self.running = not self.running
        if self.running:
            self.start.configure(text="Stop")
            self.start_time = time.time() - self.paused_time
            self.update()
        else:
            self.start.configure(text="Start")
            self.paused_time = time.time() - self.start_time

    def update_time(self):
        if self.page.page_frame.winfo_exists():
            total_seconds = int(self.elapsed_time)
            self.minutes = total_seconds // 60
            self.seconds = total_seconds % 60
            self.hundredths = int((self.elapsed_time - total_seconds) * 100)

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

    def update(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.update_time()
            self.root.after(10, self.update)

    def create_widgets(self, page):
        self.page = page
        page.page_frame.configure(bg=config["ui"].BACKGROUND_COLOR)

        with open("apps/_clock/settings.txt", "r") as f:
            settings = f.readlines()
            self.time_format = int(str.strip(settings[0], "\n"))

        time_string = "00:00"
        hundredths_string = ".00"

        self.time_lbl = d3.Label(
            page.page_frame,
            text=time_string,
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            anchor="e",
        )
        self.time_lbl.place(
            relx=0.033, rely=0.27, relwidth=0.75, relheight=0.4, anchor="nw"
        )
        self.time_lbl.configure(font=self.font_for_clock)
        self.hundredths_lbl = d3.Label(
            page.page_frame,
            text=hundredths_string,
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            justify="left",
            anchor="w",
        )
        self.hundredths_lbl.place(relx=0.78, rely=0.424, width=45, relheight=0.2)
        self.hundredths_lbl.configure(font=self.font_for_other)

        self.update_time()
        self.start = d3.Button(
            page.page_frame,
            text="Start" if not self.running else "Stop",
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            command=self.start_stop,
        )
        self.start.configure(font=self.font_for_other)
        self.start.place(
            relx=0.75, rely=0.9, relheight=0.2, relwidth=0.3, anchor="center"
        )

        self.rst = d3.Button(
            page.page_frame,
            text="Reset",
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            command=self.reset,
        )
        self.rst.configure(font=self.font_for_other)
        self.rst.place(
            relx=0.25, rely=0.9, relheight=0.2, relwidth=0.3, anchor="center"
        )

    def destroy_app(self, page):
        page.page_frame.destroy()


# Module-level instance to maintain state
_stopwatch_instance = None


def create(page, root_):
    global _stopwatch_instance
    if _stopwatch_instance is None:
        _stopwatch_instance = StopwatchApp()
    _stopwatch_instance.root = root_
    _stopwatch_instance.create_widgets(page)


def destroy(page, root):
    global _stopwatch_instance
    if _stopwatch_instance:
        _stopwatch_instance.destroy_app(page)
