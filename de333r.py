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
        switch_btn_l = d3.Button(root, text="<")
        switch_btn_l.place(x=0, y=0, width=window_config.BUTTON_WIDTH, relheight=1)

        switch_btn_r = d3.Button(root, text=">")
        switch_btn_r.place(
            relx=1, y=0, width=window_config.BUTTON_WIDTH, relheight=1, anchor="ne"
        )

        return root, bg_root, switch_btn_l, switch_btn_r, None, None, None


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
    """Empty shell of popup frame - tests should fail."""

    def __init__(self, parent, title):
        """Create empty popup shell.

        Args:
            parent: Parent window
            title: Title of the popup
        """
        self.overlay = None
        self.content_frame = None
        self.title_label = None

        # Close button
        self.close_btn = None

    def close(self):
        """Empty shell method."""
        pass

    def add_button(self, text, command):
        """Empty shell method.

        Args:
            text: Button text
            command: Function to call when button is clicked
        """
        pass

    def add_label(self, text):
        """Empty shell method.

        Args:
            text: Label text
        """
        pass
