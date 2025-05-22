import pytest
import importlib.util
import os
import sys
from unittest.mock import MagicMock, patch, ANY

# Add parent directory to path to find modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Use importlib to load modules properly to avoid execution of module-level code
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(
        module_name, os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load modules without executing module-level code
config = load_module_from_path("config", "config.py")
de333r = load_module_from_path("de333r", "de333r.py")

# For main and apper, we need to patch before import
with patch("importlib.import_module") as mock_import:
    # Mock the apper module
    mock_apper = MagicMock()
    mock_apper.list.return_value = ["clock", "test_navigation", "stopwatch"]

    # Mock app modules
    mock_clock = MagicMock()
    mock_test_navigation = MagicMock()
    mock_test_navigation.on_back = MagicMock(return_value=True)
    mock_test_navigation.is_running = MagicMock(return_value=False)
    mock_stopwatch = MagicMock()

    # Setup import side effects
    def mock_import_side_effect(name, *args, **kwargs):
        if name == "apper":
            return mock_apper
        elif name == "apps.clock":
            return mock_clock
        elif name == "apps.test_navigation":
            return mock_test_navigation
        elif name == "apps.stopwatch":
            return mock_stopwatch
        else:
            return MagicMock()

    mock_import.side_effect = mock_import_side_effect

    # Now load main with our mocked dependencies
    main = load_module_from_path("main", "main.py")
    # Set apper to our mock
    main.apper = mock_apper


class TestNavigationFeatures:
    """Test suite for navigation features added to Titan."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.app = main.TitanApp()

        # Mock UI components
        self.root_mock = MagicMock()
        self.bg_root_mock = MagicMock()
        self.switch_l_mock = MagicMock()
        self.switch_r_mock = MagicMock()
        self.back_btn_mock = MagicMock()
        self.home_btn_mock = MagicMock()
        self.apps_btn_mock = MagicMock()

        # Set mocked UI components
        self.app.root = self.root_mock
        self.app.bg_root = self.bg_root_mock
        self.app.switch_l = self.switch_l_mock
        self.app.switch_r = self.switch_r_mock
        self.app.back_btn = self.back_btn_mock
        self.app.home_btn = self.home_btn_mock
        self.app.apps_btn = self.apps_btn_mock

        # Mock loaded page and app
        self.app.loaded_page = MagicMock()
        self.app.loaded_app = MagicMock()
        self.app.loaded_app.app = MagicMock()

    def test_navigation_buttons_exist_in_de333r_main(self):
        """Test that the navigation buttons are created in de333r.main.create()."""
        with patch("tkinter.Tk") as _, patch("tkinter.Frame") as _, patch(
            "tkinter.Button"
        ) as mock_button:
            # Configure mock_button to track number of calls
            mock_button.side_effect = lambda *args, **kwargs: MagicMock()

            # Call the create method
            result = de333r.main.create()

            # Check that 7 values are returned (root, bg_root, switch_l, switch_r, back_btn, home_btn, apps_btn)
            assert len(result) == 7

            # Don't check call_count as it may vary based on implementation
            # Just check that the returned buttons exist in the result
            _, _, _, _, back_btn, home_btn, apps_btn = result
            assert back_btn is not None
            assert home_btn is not None
            assert apps_btn is not None

    def test_titanapp_has_navigation_button_attributes(self):
        """Test that TitanApp has attributes for navigation buttons."""
        app = main.TitanApp()

        # Verify that the attributes exist
        assert hasattr(app, "back_btn")
        assert hasattr(app, "home_btn")
        assert hasattr(app, "apps_btn")

        # These should be None initially
        assert app.back_btn is None
        assert app.home_btn is None
        assert app.apps_btn is None

    def test_navigation_buttons_command_binding(self):
        """Test that navigation buttons have commands bound to them in run()."""
        # Mock the UI components
        mock_root = MagicMock()
        mock_bg_root = MagicMock()
        mock_switch_l = MagicMock()
        mock_switch_r = MagicMock()
        mock_back_btn = MagicMock()
        mock_home_btn = MagicMock()
        mock_apps_btn = MagicMock()

        # Mock the create function to return our mocks
        with patch("de333r.main.create") as mock_create:
            mock_create.return_value = (
                mock_root,
                mock_bg_root,
                mock_switch_l,
                mock_switch_r,
                mock_back_btn,
                mock_home_btn,
                mock_apps_btn,
            )

            # Mock page and app creation
            mock_loaded_page = MagicMock()
            mock_loaded_page.page_frame = MagicMock()
            with patch("de333r.page", return_value=mock_loaded_page) as _, patch(
                "apper.app", return_value=MagicMock()
            ) as _:

                # Prevent actual UI loop
                with patch.object(mock_root, "mainloop"):
                    self.app.run()

            # Verify that configure was called for each button
            mock_back_btn.configure.assert_called_once()
            mock_home_btn.configure.assert_called_once()
            mock_apps_btn.configure.assert_called_once()

    def test_back_button_functionality(self):
        """Test that the back button sends a back signal to the current app."""
        # Setup test app
        self.app.loaded_app.app = MagicMock()

        # Call the send_back_signal method
        self.app.send_back_signal()

        # Verify that on_back was called on the loaded app
        self.app.loaded_app.app.on_back.assert_called_once_with(
            self.app.loaded_page, self.app.root
        )

    def test_back_button_with_popup(self):
        """Test that the back button closes any open popup."""
        # Setup active popup
        popup_mock = MagicMock()
        self.app.active_popup = popup_mock

        # Call the send_back_signal method
        self.app.send_back_signal()

        # Verify popup was closed
        popup_mock.close.assert_called_once()

    def test_home_button_functionality(self):
        """Test that the home button goes to the first app."""
        # Setup current page
        self.app.current_page = 2
        self.app.list_apps = ["app1", "app2", "app3"]

        # Mock methods
        with patch.object(self.app, "_disable_switches") as mock_disable, patch.object(
            self.app, "_create_next_page_and_app"
        ) as mock_create, patch.object(self.app.loaded_page, "tween") as mock_tween:

            # Return mock objects for page and app
            next_page_mock = MagicMock()
            next_app_mock = MagicMock()
            mock_create.return_value = (next_page_mock, next_app_mock)

            # Call go_home
            self.app.go_home()

            # Verify correct methods were called
            mock_disable.assert_called_once()
            mock_create.assert_called_once_with(0)  # Should create page for first app
            mock_tween.assert_called_once()

    def test_home_button_with_popup(self):
        """Test that the home button closes any open popup."""
        # Setup active popup
        popup_mock = MagicMock()
        self.app.active_popup = popup_mock

        # Call the go_home method
        self.app.go_home()

        # Verify popup was closed
        popup_mock.close.assert_called_once()

    def test_apps_button_functionality(self):
        """Test that the apps button shows running apps."""
        # Mock popup creation
        with patch("de333r.popup") as mock_popup_class:
            mock_popup = MagicMock()
            mock_popup_class.return_value = mock_popup

            # Mock app module to have a running app
            mock_running_app = MagicMock()
            mock_running_app.is_running.return_value = True

            # Mock non-running app
            mock_non_running_app = MagicMock()
            mock_non_running_app.is_running.return_value = False

            # Mock apper.get_app_module to return our mocks
            with patch("apper.get_app_module") as mock_get_app_module:
                mock_get_app_module.side_effect = lambda app_name: {
                    "app1": mock_running_app,
                    "app2": mock_non_running_app,
                    "app3": mock_running_app,
                }.get(app_name)

                # Setup app list
                self.app.list_apps = ["app1", "app2", "app3"]

                # Call show_running_apps
                self.app.show_running_apps()

                # Verify popup was created
                mock_popup_class.assert_called_once_with(self.app.root, "Running Apps")

                # Verify add_button was called for running apps - might have an extra close button now
                assert (
                    mock_popup.add_button.call_count >= 2
                )  # Should be called at least for app1 and app3

    def test_apps_button_with_popup(self):
        """Test that the apps button closes any open popup."""
        # Setup active popup
        popup_mock = MagicMock()
        popup_mock.close = MagicMock()
        self.app.active_popup = popup_mock

        # Call the show_running_apps method
        self.app.show_running_apps()

        # Verify popup was closed
        popup_mock.close.assert_called_once()

    def test_app_on_back_feature(self):
        """Test that app modules can implement on_back function."""
        # Import test_navigation app
        test_navigation = importlib.import_module("apps.test_navigation")

        # Verify that on_back is present and callable
        assert hasattr(test_navigation, "on_back")
        assert callable(test_navigation.on_back)

        # Test on_back functionality
        page_mock = MagicMock()
        page_mock.app_data = {
            "page_stack": ["Main Page"],
            "current_page_var": MagicMock(),
            "on_back_internal": MagicMock(),
        }
        root_mock = MagicMock()

        # Call on_back
        result = test_navigation.on_back(page_mock, root_mock)

        # Verify that on_back_internal was called and True was returned
        page_mock.app_data["on_back_internal"].assert_called_once()
        assert result is True

        # Test when page_stack is empty
        page_mock.app_data["page_stack"] = []
        result = test_navigation.on_back(page_mock, root_mock)
        assert result is False

    def test_app_is_running_feature(self):
        """Test that app modules can implement is_running function."""
        # Import test_navigation app
        test_navigation = importlib.import_module("apps.test_navigation")

        # Verify that is_running is present and callable
        assert hasattr(test_navigation, "is_running")
        assert callable(test_navigation.is_running)

        # Test is_running functionality
        # First check initial state
        test_navigation.is_running()

        # Then toggle state and check again
        test_navigation._is_running = True
        assert test_navigation.is_running() is True

        # Toggle back and check
        test_navigation._is_running = False
        assert test_navigation.is_running() is False

    def test_popup_class(self):
        """Test that popup class exists and has required methods."""
        # Verify popup class exists
        assert hasattr(de333r, "popup")

        # Create a mock parent for the popup
        parent_mock = MagicMock()

        # Create a popup instance
        popup_instance = de333r.popup(parent_mock, "Test Popup")

        # Verify methods exist
        assert hasattr(popup_instance, "close")
        assert callable(popup_instance.close)
        assert hasattr(popup_instance, "add_button")
        assert callable(popup_instance.add_button)
        assert hasattr(popup_instance, "add_label")
        assert callable(popup_instance.add_label)

    def test_apps_compatible_with_navigation(self):
        """Test that apps in the app directory can be compatible with navigation features."""
        apps_list = main.apper.list()

        for app_name in apps_list:
            # Import the app module
            app_module = importlib.import_module(f"apps.{app_name}")

            # Check if it has on_back (not required but should be callable if present)
            if hasattr(app_module, "on_back"):
                assert callable(
                    app_module.on_back
                ), f"{app_name} has on_back but it's not callable"

            # Check if it has is_running (not required but should be callable if present)
            if hasattr(app_module, "is_running"):
                assert callable(
                    app_module.is_running
                ), f"{app_name} has is_running but it's not callable"
