"""Test Navigation App

This app demonstrates the back button functionality and running apps tracking.
"""

import tkinter as d3
from config import config

# Global variable to track if the app is running a background loop
_is_running = False


def create(page, root):
    """Create the test navigation app.

    Args:
        page: The page to create the app on
        root: The root window
    """
    global _is_running

    # Get UI configuration
    ui_config = config["ui"]
    window_config = config["window"]

    # Create the main frame
    main_frame = d3.Frame(
        page.page_frame,
        bg=ui_config.BACKGROUND_COLOR,
        width=window_config.FRAME_WIDTH,
        height=window_config.FRAME_HEIGHT,
    )
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a title with smaller font
    title_label = d3.Label(
        main_frame,
        text="Navigation Test App",
        font=(ui_config.FONT_FAMILY, 14),  # Reduced from 18
        fg=ui_config.PRIMARY_COLOR,
        bg=ui_config.BACKGROUND_COLOR,
    )
    title_label.pack(pady=5)  # Reduced padding

    # Create navigation indicators
    nav_frame = d3.Frame(main_frame, bg=ui_config.BACKGROUND_COLOR)
    nav_frame.pack(pady=3)  # Reduced padding

    # Create stack of "pages" to demonstrate back button
    page_stack = []
    current_page_var = d3.StringVar(value="Main Page")

    # Create a label to show current page
    page_label = d3.Label(
        nav_frame,
        textvariable=current_page_var,
        font=(ui_config.FONT_FAMILY, 10),  # Reduced from 12
        fg=ui_config.PRIMARY_COLOR,
        bg=ui_config.BACKGROUND_COLOR,
    )
    page_label.pack(pady=3)  # Reduced padding

    # Function to navigate to a new page
    def navigate_to_page(page_name):
        page_stack.append(current_page_var.get())
        current_page_var.set(page_name)
        back_btn.config(state="normal" if page_stack else "disabled")

    # Create buttons with a grid layout to prevent overflow
    buttons_frame = d3.Frame(main_frame, bg=ui_config.BACKGROUND_COLOR)
    buttons_frame.pack(pady=3)  # Reduced padding

    # Create a 2x2 grid for navigation buttons
    left_buttons = d3.Frame(buttons_frame, bg=ui_config.BACKGROUND_COLOR)
    left_buttons.pack(side="left", padx=5)

    right_buttons = d3.Frame(buttons_frame, bg=ui_config.BACKGROUND_COLOR)
    right_buttons.pack(side="right", padx=5)

    # Page 1 button (left column)
    page1_btn = d3.Button(
        left_buttons,
        text="Page 1",  # Shortened text
        command=lambda: navigate_to_page("Page 1"),
        bg=ui_config.PRIMARY_COLOR,
        font=(ui_config.FONT_FAMILY, 8),  # Smaller font
    )
    page1_btn.pack(pady=2)

    # Page 2 button (left column)
    page2_btn = d3.Button(
        left_buttons,
        text="Page 2",  # Shortened text
        command=lambda: navigate_to_page("Page 2"),
        bg=ui_config.PRIMARY_COLOR,
        font=(ui_config.FONT_FAMILY, 8),  # Smaller font
    )
    page2_btn.pack(pady=2)

    # Page 3 button (right column)
    page3_btn = d3.Button(
        right_buttons,
        text="Page 3",  # Shortened text
        command=lambda: navigate_to_page("Page 3"),
        bg=ui_config.PRIMARY_COLOR,
        font=(ui_config.FONT_FAMILY, 8),  # Smaller font
    )
    page3_btn.pack(pady=2)

    # Back button (right column)
    back_btn = d3.Button(
        right_buttons,
        text="Back",  # Shortened text
        command=lambda: on_back_internal(),
        state="disabled",
        bg=ui_config.SECONDARY_COLOR,
        font=(ui_config.FONT_FAMILY, 8),  # Smaller font
    )
    back_btn.pack(pady=2)

    # Function for internal back button
    def on_back_internal():
        if page_stack:
            current_page_var.set(page_stack.pop())
            back_btn.config(state="normal" if page_stack else "disabled")

    # Toggle for running state to appear in recent apps
    run_var = d3.BooleanVar(value=_is_running)

    def toggle_running():
        global _is_running
        _is_running = not _is_running
        run_var.set(_is_running)
        run_status_label.config(text=f"Running: {'Yes' if _is_running else 'No'}")

    # Create a frame for the running status
    run_frame = d3.Frame(main_frame, bg=ui_config.BACKGROUND_COLOR)
    run_frame.pack(pady=3)  # Reduced padding

    # Put status and toggle in a horizontal layout
    status_frame = d3.Frame(run_frame, bg=ui_config.BACKGROUND_COLOR)
    status_frame.pack(side="left", padx=5)

    toggle_frame = d3.Frame(run_frame, bg=ui_config.BACKGROUND_COLOR)
    toggle_frame.pack(side="right", padx=5)

    run_status_label = d3.Label(
        status_frame,
        text=f"Running: {'Yes' if _is_running else 'No'}",
        font=(ui_config.FONT_FAMILY, 8),  # Reduced from 10
        fg=ui_config.PRIMARY_COLOR,
        bg=ui_config.BACKGROUND_COLOR,
    )
    run_status_label.pack(pady=2)

    toggle_btn = d3.Button(
        toggle_frame,
        text="Toggle",  # Shortened text
        command=toggle_running,
        bg=ui_config.PRIMARY_COLOR,
        font=(ui_config.FONT_FAMILY, 8),  # Smaller font
    )
    toggle_btn.pack(pady=2)

    # Store references for access from other functions
    page.app_data = {
        "main_frame": main_frame,
        "page_stack": page_stack,
        "current_page_var": current_page_var,
        "back_btn": back_btn,
        "on_back_internal": on_back_internal,
    }


def on_back(page, root):
    """Handle the back button press from the navigation bar.

    Args:
        page: The current page
        root: The root window
    """
    # Check if we have app_data and can go back
    if hasattr(page, "app_data") and page.app_data["page_stack"]:
        page.app_data["on_back_internal"]()
        return True
    return False


def destroy(page, root):
    """Clean up when app is closed.

    Args:
        page: The page being destroyed
        root: The root window
    """
    global _is_running
    _is_running = False

    if hasattr(page, "app_data"):
        if "main_frame" in page.app_data:
            page.app_data["main_frame"].destroy()


def is_running():
    """Check if the app is running a background task.

    Returns:
        bool: True if the app is running, False otherwise
    """
    global _is_running
    return _is_running
