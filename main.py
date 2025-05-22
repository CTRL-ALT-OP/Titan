import de333r as titan
import apper
from config import config


class TitanApp:
    def __init__(self):
        self.list_apps = apper.list()
        self.current_page = 0
        self.loaded_page = None
        self.loaded_app = None
        self.root = None
        self.bg_root = None
        self.switch_l = None
        self.switch_r = None
        self.back_btn = None
        self.home_btn = None
        self.apps_btn = None

        # Track running apps
        self.running_apps = []

        # Track active popup
        self.active_popup = None

        # Configuration
        self.anim_config = config["animation"]

    def _disable_switches(self):
        """Disable navigation buttons during transition."""
        self.switch_l.configure(state="disabled")
        self.switch_r.configure(state="disabled")

    def _enable_switches(self):
        """Enable navigation buttons after transition."""
        self.switch_l.configure(state="normal")
        self.switch_r.configure(state="normal")

    def _get_next_page_index(self, direction):
        """Calculate the next page index based on direction."""
        if direction == 1:  # Going forward
            if self.current_page == len(self.list_apps) - 1:
                return 0  # Wrap to beginning
        elif self.current_page == 0:
            return len(self.list_apps) - 1  # Wrap to end
        return self.current_page + direction

    def _create_next_page_and_app(self, next_index):
        """Create the next page and app instances."""
        next_page = titan.page(self.bg_root, self.root)
        app = self.list_apps[next_index]
        next_app = apper.app(next_page, app, self.root)
        return next_page, next_app

    def _transition_complete(self, next_app, next_page, next_index):
        """Handle completion of page transition."""
        self.current_page = next_index
        self.loaded_app.app.destroy(self.loaded_page, self.root)
        self.loaded_page = next_page
        self.loaded_app = next_app
        self._enable_switches()

    def _check_tween_complete(self, next_app, next_page, next_index):
        """Check if page transition is complete."""
        if self.loaded_page.finished:
            self._transition_complete(next_app, next_page, next_index)
        else:
            self.root.after(
                self.anim_config.TWEEN_CHECK_INTERVAL,
                lambda: self._check_tween_complete(next_app, next_page, next_index),
            )

    def switch(self, direction):
        """Switch to the next or previous app.

        Args:
            direction (int): 1 for forward, -1 for backward
        """
        if self.active_popup:
            self.active_popup.close()
            self.active_popup = None
        self._disable_switches()
        next_index = self._get_next_page_index(direction)
        next_page, next_app = self._create_next_page_and_app(next_index)

        # Start the transition animation
        self.loaded_page.tween(
            next_page, self.anim_config.TWEEN_DURATION, direction=direction
        )

        # Start checking for transition completion
        self.root.after(
            self.anim_config.TWEEN_CHECK_INTERVAL,
            lambda: self._check_tween_complete(next_app, next_page, next_index),
        )

    def send_back_signal(self):
        """Send a back signal to the current app."""
        pass

    def go_home(self):
        """Go to the first app in the list.d"""
        pass

    def show_running_apps(self):
        """Show apps that are currently running loops."""
        pass

    def switch_to_app(self, app_name):
        """Switch directly to a specific app by name."""
        pass

    def run(self):
        """Initialize and run the Titan application."""
        (
            self.root,
            self.bg_root,
            self.switch_l,
            self.switch_r,
            self.back_btn,
            self.home_btn,
            self.apps_btn,
        ) = titan.main.create()

        self.switch_l.configure(command=lambda: self.switch(-1))
        self.switch_r.configure(command=lambda: self.switch(1))

        # Initialize with the first app
        self.loaded_page = titan.page(self.bg_root, self.root)
        self.loaded_app = apper.app(self.loaded_page, self.list_apps[0], self.root)

        self.loaded_page.page_frame.pack()

        self.root.mainloop()


if __name__ == "__main__":
    app = TitanApp()
    app.run()
