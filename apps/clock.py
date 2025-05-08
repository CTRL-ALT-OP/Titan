import tkinter as d3
import time
from config import config


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

        # Get configuration
        class ui_config(config["ui"], config["clock"]):
            pass

        self.ui_config = ui_config()

        # Fonts
        self.font_for_clock = (
            self.ui_config.FONT_FAMILY,
            self.ui_config.CLOCK_MAIN_FONT_SIZE,
            "bold",
        )
        self.font_for_other = (
            self.ui_config.FONT_FAMILY,
            self.ui_config.CLOCK_SECONDARY_FONT_SIZE,
            "bold",
        )
        self.font_for_other2 = (
            self.ui_config.FONT_FAMILY,
            self.ui_config.CLOCK_TERTIARY_FONT_SIZE,
            "bold",
        )

    def update(self):
        """Update the clock display."""
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

            self.root.after(self.ui_config.CLOCK_UPDATE_INTERVAL, self.update)

    def change_format(self):
        """Toggle between 12h and 24h format."""
        if self.time_format == 12:
            self.time_format = 24
            self.format_.configure(text="24h")
        else:
            self.time_format = 12
            self.format_.configure(text="12h")

    def create_widgets(self, page):
        """Create all clock widgets."""
        page.page_frame.configure(bg=self.ui_config.BACKGROUND_COLOR)

        # Load settings
        with open("apps/_clock/settings.txt", "r") as f:
            settings = f.readlines()
            self.time_format = int(str.strip(settings[0], "\n"))

        time_string = "00:00"
        seconds_string = "00"
        date_string = ""

        # Time label
        self.time_lbl = d3.Label(
            page.page_frame,
            text=time_string,
            fg=self.ui_config.PRIMARY_COLOR,
            bg=self.ui_config.BACKGROUND_COLOR,
            anchor="e",
        )
        self.time_lbl.place(
            relx=0.033, rely=0.27, relwidth=0.75, relheight=0.4, anchor="nw"
        )
        self.time_lbl.configure(font=self.font_for_clock)

        # Seconds label
        self.seconds_lbl = d3.Label(
            page.page_frame,
            text=seconds_string,
            fg=self.ui_config.PRIMARY_COLOR,
            bg=self.ui_config.BACKGROUND_COLOR,
            justify="left",
            anchor="w",
        )
        self.seconds_lbl.place(relx=0.78, rely=0.424, width=45, relheight=0.2)
        self.seconds_lbl.configure(font=self.font_for_other)

        # Date label
        self.date_lbl = d3.Label(
            page.page_frame,
            text=date_string,
            fg=self.ui_config.PRIMARY_COLOR,
            bg=self.ui_config.BACKGROUND_COLOR,
        )
        self.date_lbl.place(
            relx=0.5, rely=0.61, relwidth=0.9, relheight=0.1, anchor="center"
        )
        self.date_lbl.configure(font=self.font_for_other2)

        # AM/PM label
        self.am_pm = d3.Label(
            page.page_frame,
            text="",
            fg=self.ui_config.PRIMARY_COLOR,
            bg=self.ui_config.BACKGROUND_COLOR,
        )
        self.am_pm.place(relx=0.8, rely=1, relwidth=0.15, relheight=0.2, anchor="sw")
        self.am_pm.configure(font=self.font_for_other)

        # Format toggle button
        self.format_ = d3.Button(
            page.page_frame,
            text="",
            fg=self.ui_config.SECONDARY_COLOR,
            bg=self.ui_config.BACKGROUND_COLOR,
            command=self.change_format,
        )
        if self.time_format == 12:
            self.format_.configure(text="12h")
        else:
            self.format_.configure(text="24h")

        self.format_.configure(font=self.font_for_other)
        self.format_.place(relx=0, rely=1, relheight=0.18, relwidth=0.21, anchor="sw")

        self.running = True
        self.root.after(self.ui_config.CLOCK_STARTUP_DELAY, self.update)

    def destroy_app(self, page):
        """Clean up when app is closed."""
        self.running = False
        page.page_frame.destroy()
        with open("apps/_clock/settings.txt", "w") as f:
            self.root.update_idletasks()
            f.write(str(self.time_format))


# Module-level instance to maintain state
_clock_instance = None


def create(page, root_):
    """Create clock app instance."""
    global _clock_instance
    _clock_instance = ClockApp()
    _clock_instance.root = root_
    _clock_instance.create_widgets(page)


def destroy(page, root):
    """Destroy clock app instance."""
    global _clock_instance
    if _clock_instance:
        _clock_instance.destroy_app(page)
        _clock_instance = None
