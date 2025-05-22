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

    # Create the main frame
    main_frame = d3.Frame(page.page_frame, bg=ui_config.BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=True)

    # Create a title
    title_label = d3.Label(
        main_frame,
        text="Navigation Test App",
        font=(ui_config.FONT_FAMILY, ui_config.TITLE_FONT_SIZE),
        fg=ui_config.PRIMARY_COLOR,
        bg=ui_config.BACKGROUND_COLOR,
    )
    title_label.pack(pady=20)

    # Create navigation indicators
    nav_frame = d3.Frame(main_frame, bg=ui_config.BACKGROUND_COLOR)
    nav_frame.pack(pady=10)

    # Create stack of "pages" to demonstrate back button
    page_stack = []
    current_page_var = d3.StringVar(value="Main Page")

    # Create a label to show current page
    page_label = d3.Label(
        nav_frame,
        textvariable=current_page_var,
        font=(ui_config.FONT_FAMILY, 16),
        fg=ui_config.PRIMARY_COLOR,
        bg=ui_config.BACKGROUND_COLOR,
    )
    page_label.pack(pady=10)

    # Function to navigate to a new page
    def navigate_to_page(page_name):
        page_stack.append(current_page_var.get())
        current_page_var.set(page_name)
        back_btn.config(state="normal" if page_stack else "disabled")

    # Create buttons to navigate to "pages"
    buttons_frame = d3.Frame(main_frame, bg=ui_config.BACKGROUND_COLOR)
    buttons_frame.pack(pady=20)

    # Page 1 button
    page1_btn = d3.Button(
        buttons_frame,
        text="Go to Page 1",
        command=lambda: navigate_to_page("Page 1"),
        bg=ui_config.PRIMARY_COLOR,
    )
    page1_btn.pack(pady=5)

    # Page 2 button
    page2_btn = d3.Button(
        buttons_frame,
        text="Go to Page 2",
        command=lambda: navigate_to_page("Page 2"),
        bg=ui_config.PRIMARY_COLOR,
    )
    page2_btn.pack(pady=5)

    # Page 3 button
    page3_btn = d3.Button(
        buttons_frame,
        text="Go to Page 3",
        command=lambda: navigate_to_page("Page 3"),
        bg=ui_config.PRIMARY_COLOR,
    )
    page3_btn.pack(pady=5)

    # Back button to demonstrate internal navigation
    back_btn = d3.Button(
        buttons_frame,
        text="Back (Internal)",
        command=lambda: on_back_internal(),
        state="disabled",
        bg=ui_config.SECONDARY_COLOR,
    )
    back_btn.pack(pady=10)

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
    run_frame.pack(pady=20)

    run_status_label = d3.Label(
        run_frame,
        text=f"Running: {'Yes' if _is_running else 'No'}",
        font=(ui_config.FONT_FAMILY, 14),
        fg=ui_config.PRIMARY_COLOR,
        bg=ui_config.BACKGROUND_COLOR,
    )
    run_status_label.pack(pady=5)

    toggle_btn = d3.Button(
        run_frame,
        text="Toggle Running State",
        command=toggle_running,
        bg=ui_config.PRIMARY_COLOR,
    )
    toggle_btn.pack(pady=5)

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
