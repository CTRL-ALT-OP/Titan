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
        self.back_btn.configure(state="disabled")
        self.home_btn.configure(state="disabled")
        self.apps_btn.configure(state="disabled")

    def _enable_switches(self):
        """Enable navigation buttons after transition."""
        self.switch_l.configure(state="normal")
        self.switch_r.configure(state="normal")
        self.back_btn.configure(state="normal")
        self.home_btn.configure(state="normal")
        self.apps_btn.configure(state="normal")

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

    def go_home(self):
        """Go to the first app in the list or close popup if open."""
        if self.active_popup:
            self.active_popup.close()
            self.active_popup = None
        elif self.current_page != 0:
            self._disable_switches()
            next_index = 0
            next_page, next_app = self._create_next_page_and_app(next_index)

            # Direction is forward if currently at the end, otherwise backward
            direction = 1 if self.current_page == len(self.list_apps) - 1 else -1

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
        """Send a back signal to the current app or close popup if open."""
        if self.active_popup:
            self.active_popup.close()
            self.active_popup = None
        elif hasattr(self.loaded_app.app, "on_back"):
            self.loaded_app.app.on_back(self.loaded_page, self.root)

    def show_running_apps(self):
        """Show apps that are currently running loops."""
        # Create a popup to display running apps
        if self.active_popup:
            self.active_popup.close()
            self.active_popup = None
            return
        self.active_popup = titan.popup(self.root, "Running Apps")

        # Get running apps (those with active loops)
        running_apps = []
        for app_name in self.list_apps:
            app_module = apper.get_app_module(app_name)
            if hasattr(app_module, "is_running") and app_module.is_running():
                running_apps.append(app_name)

        if running_apps:
            for app_name in running_apps:
                # Create a button for each running app
                self.active_popup.add_button(
                    app_name, lambda app=app_name: self.switch_to_app(app)
                )
        else:
            self.active_popup.add_label("No apps running")

    def switch_to_app(self, app_name):
        """Switch directly to a specific app by name."""
        # Close popup if it's open
        if self.active_popup:
            self.active_popup.close()
            self.active_popup = None

        if app_name in self.list_apps:
            target_index = self.list_apps.index(app_name)
            if target_index != self.current_page:
                self._disable_switches()
                next_page, next_app = self._create_next_page_and_app(target_index)

                # Determine direction based on indices
                direction = (
                    1
                    if (
                        target_index > self.current_page
                        or (
                            self.current_page == len(self.list_apps) - 1
                            and target_index == 0
                        )
                    )
                    else -1
                )

                # Start the transition animation
                self.loaded_page.tween(
                    next_page, self.anim_config.TWEEN_DURATION, direction=direction
                )

                # Start checking for transition completion
                self.root.after(
                    self.anim_config.TWEEN_CHECK_INTERVAL,
                    lambda: self._check_tween_complete(
                        next_app, next_page, target_index
                    ),
                )

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
        self.back_btn.configure(command=self.send_back_signal)
        self.home_btn.configure(command=self.go_home)
        self.apps_btn.configure(command=self.show_running_apps)

        # Initialize with the first app
        self.loaded_page = titan.page(self.bg_root, self.root)
        self.loaded_app = apper.app(self.loaded_page, self.list_apps[0], self.root)

        self.loaded_page.page_frame.pack()

        self.root.mainloop()


if __name__ == "__main__":
    app = TitanApp()
    app.run()
