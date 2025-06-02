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

    def create_notification(self, text, type="info"):
        """Create a notification frame.

        Args:
            text: Text to display in notification
            type: Type of notification ("info", "success", "warning", "error")

        Returns:
            notification: The created notification instance
        """
        return notification(self.true_root, text, type)

    def create_popup(self, title, content: d3.Frame):
        """Create a popup frame.

        Args:
            title: Title of the popup
            content: Content frame to display in popup

        Returns:
            popup: The created popup instance
        """
        popup_instance = popup(self.true_root, title)

        # If content frame is provided, pack it into the popup's content frame
        if content:
            content.pack(in_=popup_instance.content_frame, fill="both", expand=True)

        return popup_instance

    def create_warning(self, text):
        return self.create_notification(text, "warning")

    def create_error(self, text):
        return self.create_notification(text, "error")

    def create_success(self, text):
        return self.create_notification(text, "success")

    def create_info(self, text):
        return self.create_notification(text, "info")


class notification:
    def __init__(
        self,
        parent,
        text,
        type="info",
        duration=config["animation"].NOTIFICATION_DURATION,
    ):
        """Create and display a notification.

        Args:
            parent: Parent widget to place notification on
            text: Text to display in notification
            type: Type of notification ("info", "success", "warning", "error")
            duration: Duration to show notification in milliseconds
        """
        self.parent = parent
        self.root = parent.nametowidget(".")
        self.text = text
        self.type = type
        self.duration = duration
        self.notification_timer = None

        # Get UI configuration
        ui_config = config["ui"]

        # Choose colors based on notification type
        bg_color = ui_config.BACKGROUND_COLOR
        fg_color = ui_config.PRIMARY_COLOR

        if type == "success":
            bg_color = "#ccffcc"
            fg_color = "#006600"
        elif type == "warning":
            bg_color = "#fff3cd"
            fg_color = "#856404"
        elif type == "error":
            bg_color = "#f8d7da"
            fg_color = "#721c24"

        # Create notification frame
        self.notification_frame = d3.Frame(
            parent,
            bg=bg_color,
            highlightthickness=1,
            highlightbackground=fg_color,
        )

        # Create notification label
        self.notification_label = d3.Label(
            self.notification_frame,
            text=text,
            font=(ui_config.FONT_FAMILY, 10),
            bg=bg_color,
            fg=fg_color,
            wraplength=350,
            justify="center",
            padx=10,
            pady=10,
        )
        self.notification_label.pack(expand=True, fill="both")

        # Position in the center of the screen
        self.notification_frame.place(
            relx=0.5, rely=0.4, anchor="center", width=350, height=100
        )

        # Schedule the notification to disappear
        self.notification_timer = self.root.after(duration, self._hide_notification)

    def _hide_notification(self):
        """Hide the notification by removing it from view."""
        if self.notification_frame:
            self.notification_frame.place_forget()
            self.notification_frame.destroy()

    def close(self):
        """Manually close the notification."""
        if self.notification_timer:
            self.root.after_cancel(self.notification_timer)
            self.notification_timer = None
        self._hide_notification()


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
