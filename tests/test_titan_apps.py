import pytest
from unittest.mock import MagicMock

# Import the app modules
import importlib
import apper


class TestApps:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.apps = apper.list()

    @pytest.mark.parametrize(
        "app_name",
        ["clock", "calculator", "stopwatch", "blockoid", "5inrow", "TicTacToe"],
    )
    def test_app_module_structure(self, app_name):
        """Test that each app module has the required structure."""
        if app_name in self.apps:
            # Import the app module
            app_module = importlib.import_module(f"apps.{app_name}")

            # Check for required functions
            assert hasattr(
                app_module, "create"
            ), f"{app_name} module doesn't have 'create' function"

            # Not all apps may have destroy
            if hasattr(app_module, "destroy"):
                assert callable(
                    app_module.destroy
                ), f"{app_name}:'destroy' is not callable"

    def test_clock_app(self):
        """Test the clock app module."""
        if "clock" in self.apps:
            clock_module = importlib.import_module("apps.clock")

            # Verify create function structure
            assert callable(clock_module.create)

            # Create mock page and root
            page_mock = MagicMock()
            page_mock.page_frame = MagicMock()
            root_mock = MagicMock()

            # Call create with the mocks
            clock_module.create(page_mock, root_mock)

            # Verify that page_frame was used
            assert (
                page_mock.page_frame.configure.called
                or page_mock.page_frame.config.called
            )

    @pytest.mark.parametrize(
        "app_name", ["calculator", "stopwatch", "blockoid", "5inrow", "TicTacToe"]
    )
    def test_other_apps_create_method(self, app_name):
        """Test that create method doesn't raise exceptions."""
        if app_name in self.apps:
            # Import the app module
            app_module = importlib.import_module(f"apps.{app_name}")

            # Create mock page and root
            page_mock = MagicMock()
            page_mock.page_frame = MagicMock()
            root_mock = MagicMock()

            try:
                # Call create method - this should not raise exceptions
                app_module.create(page_mock, root_mock)
            except Exception as e:
                pytest.fail(f"App '{app_name}' create method raised an exception: {e}")

    def test_app_discovery(self):
        """Test that app discovery works correctly."""
        apps_list = apper.list()

        # Verify apps list is not empty
        assert len(apps_list) > 0

        # Verify special apps are in the list based on config
        assert "clock" in apps_list
        assert "stopwatch" in apps_list
