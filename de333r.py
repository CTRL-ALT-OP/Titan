import tkinter as d3
from config import config


class main:
    @staticmethod
    def create():
        """Create the main window and its components."""
        root = d3.Tk()
        root.resizable(False, False)

        window_config = config["window"]

        # Create foreground frame
        fg_root = d3.Frame(
            root, width=window_config.WINDOW_WIDTH, height=window_config.WINDOW_HEIGHT
        )
        fg_root.pack()

        # Create background frame
        bg_root = d3.Frame(
            root, width=window_config.FRAME_WIDTH, height=window_config.FRAME_HEIGHT
        )
        bg_root.place(x=window_config.FRAME_X_OFFSET, y=window_config.FRAME_Y_OFFSET)

        # Create navigation buttons
        switch_btn_l = d3.Button(
            root,
            text="<",
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            font=(config["ui"].FONT_FAMILY, config["ui"].BUTTON_FONT_SIZE),
        )
        switch_btn_l.place(
            x=0,
            y=0,
            width=window_config.BUTTON_WIDTH,
            height=window_config.WINDOW_HEIGHT,
        )

        switch_btn_r = d3.Button(
            root,
            text=">",
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            font=(config["ui"].FONT_FAMILY, config["ui"].BUTTON_FONT_SIZE),
        )
        switch_btn_r.place(
            relx=1,
            y=0,
            width=window_config.BUTTON_WIDTH,
            height=window_config.WINDOW_HEIGHT,
            anchor="ne",
        )

        # Create bottom navigation buttons
        bottom_frame = d3.Frame(
            root,
            width=window_config.FRAME_WIDTH,
            height=window_config.BOTTOM_NAV_HEIGHT,
            bg=config["ui"].BACKGROUND_COLOR,
        )
        bottom_frame.place(
            x=window_config.FRAME_X_OFFSET,
            y=window_config.FRAME_HEIGHT + window_config.FRAME_Y_OFFSET,
        )

        back_btn = d3.Button(
            bottom_frame,
            text="←",
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            font=(config["ui"].FONT_FAMILY, config["ui"].BUTTON_FONT_SIZE),
        )
        back_btn.place(relx=0.2, rely=0.5, anchor="center", width=40, height=40)

        home_btn = d3.Button(
            bottom_frame,
            text="⌂",
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            font=(config["ui"].FONT_FAMILY, config["ui"].BUTTON_FONT_SIZE),
        )
        home_btn.place(relx=0.5, rely=0.5, anchor="center", width=40, height=40)

        apps_btn = d3.Button(
            bottom_frame,
            text="☰",
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
            font=(config["ui"].FONT_FAMILY, config["ui"].BUTTON_FONT_SIZE),
        )
        apps_btn.place(relx=0.8, rely=0.5, anchor="center", width=40, height=40)

        return root, bg_root, switch_btn_l, switch_btn_r, back_btn, home_btn, apps_btn


class page:
    def create(self):
        """Create a page frame."""
        window_config = config["window"]
        self.page_frame = d3.Frame(
            self.root,
            width=window_config.FRAME_WIDTH,
            height=window_config.FRAME_HEIGHT,
        )

    def tween(self, frame_2, time, direction=1):
        """Animate transition between pages.

        Args:
            frame_2: The page to transition to
            time (int): Total duration of the animation in milliseconds
            direction (int): 1 for forward, -1 for backward
        """
        anim_config = config["animation"]
        window_config = config["window"]

        self.finished = False
        bounding_x = window_config.FRAME_WIDTH
        frame_2.page_frame.place(x=0 + (direction * bounding_x), y=0)

        def looper(self):
            self.curr_x -= anim_config.TWEEN_STEP_SIZE
            frame_2.page_frame.place(x=direction * self.curr_x, y=0)
            self.page_frame.place(x=direction * (self.curr_x - self.bounding_x), y=0)
            if self.curr_x > 0:
                self.true_root.update()
                self.true_root.after(
                    int(time / self.bounding_x), lambda self=self: looper(self)
                )
            else:
                self.finished = True

        self.bounding_x = bounding_x
        self.curr_x = bounding_x
        self.true_root.after(int(time / bounding_x), lambda self=self: looper(self))
        self.page_frame.pack_forget()

    def __init__(self, root, true_root):
        self.root = root
        self.true_root = true_root
        self.finished = False
        self.create()


class popup:
    """Popup frame for displaying app lists or other information."""

    def __init__(self, parent, title):
        """Create a popup frame.

        Args:
            parent: Parent window
            title: Title of the popup
        """
        window_config = config["window"]
        ui_config = config["ui"]

        # Set size and position
        width = window_config.FRAME_WIDTH
        height = window_config.FRAME_HEIGHT

        # Create an overlay frame that covers just the content area
        self.overlay = d3.Frame(
            parent,
            width=window_config.FRAME_WIDTH,
            height=window_config.FRAME_HEIGHT,
            bg=config["ui"].BACKGROUND_COLOR,
        )

        # Place it over the content area
        self.overlay.place(
            x=window_config.FRAME_X_OFFSET, y=window_config.FRAME_Y_OFFSET
        )

        # Create the popup frame
        self.content_frame = d3.Frame(
            self.overlay,
            width=width,
            height=height - 30,
            bg=ui_config.BACKGROUND_COLOR,
        )

        self.content_frame.place(x=0, y=30)

        # Title label at the top
        self.title_label = d3.Label(
            self.overlay,
            text=title,
            font=(ui_config.FONT_FAMILY, 14),
            fg=ui_config.PRIMARY_COLOR,
            bg=ui_config.BACKGROUND_COLOR,
        )
        self.title_label.place(x=0, y=0, width=width, height=30)

        # Close button
        self.close_btn = d3.Button(
            self.overlay,
            text="×",
            fg=ui_config.SECONDARY_COLOR,
            bg=ui_config.BACKGROUND_COLOR,
            font=(ui_config.FONT_FAMILY, ui_config.BUTTON_FONT_SIZE),
            borderwidth=0,
            command=self.close,
        )
        self.close_btn.place(x=width - 30, y=5, width=25, height=25)

        # Current y position for adding elements
        self.current_y = 10

    def close(self):
        """Close the popup by destroying the overlay frame."""
        self.overlay.destroy()

    def add_button(self, text, command):
        """Add a button to the popup.

        Args:
            text: Button text
            command: Function to call when button is clicked
        """

        # Create a wrapper function to close the popup after executing command
        def wrapped_command():
            command()
            self.close()

        button = d3.Button(
            self.content_frame,
            text=text,
            command=wrapped_command,
            bg=config["ui"].PRIMARY_COLOR,
            fg=config["ui"].BACKGROUND_COLOR,
            font=(config["ui"].FONT_FAMILY, 12),
        )
        button.place(
            x=20, y=self.current_y, width=config["window"].FRAME_WIDTH - 40, height=30
        )

        self.current_y += 40

    def add_label(self, text):
        """Add a label to the popup.

        Args:
            text: Label text
        """
        label = d3.Label(
            self.content_frame,
            text=text,
            font=(config["ui"].FONT_FAMILY, 12),
            fg=config["ui"].PRIMARY_COLOR,
            bg=config["ui"].BACKGROUND_COLOR,
        )
        label.place(x=20, y=self.current_y, width=160)

        self.current_y += 30
