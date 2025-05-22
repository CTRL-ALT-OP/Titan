import importlib.util
import os
import sys
from unittest.mock import MagicMock, patch

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


# Set up mock for tkinter
with patch.dict("sys.modules", {"tkinter": MagicMock(), "d3": MagicMock()}):
    # Load modules without executing module-level code
    config = load_module_from_path("config", "config.py")
    de333r = load_module_from_path("de333r", "de333r.py")


class TestPopup:
    """Test suite for the popup class in de333r module."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a mock parent for the popup
        self.parent_mock = MagicMock()

        # Mock tkinter elements
        with patch("tkinter.Frame", return_value=MagicMock()) as frame_mock, patch(
            "tkinter.Label", return_value=MagicMock()
        ) as label_mock, patch(
            "tkinter.Button", return_value=MagicMock()
        ) as button_mock:

            # Set up mock attributes
            frame_mock.return_value.kwargs = {"bg": "#FFFFFF"}
            label_mock.return_value.kwargs = {"fg": "#000000", "bg": "#FFFFFF"}
            button_mock.return_value.kwargs = {"fg": "#000000", "bg": "#FFFFFF"}

            # Create a popup instance
            self.popup = de333r.popup(self.parent_mock, "Test Popup")

            # Store mocks for later access
            self.frame_mock = frame_mock
            self.label_mock = label_mock
            self.button_mock = button_mock

    def test_popup_initialization(self):
        """Test that popup initializes correctly."""
        # Verify that an overlay frame was created
        assert hasattr(self.popup, "overlay")

        # Verify that a content frame was created
        assert hasattr(self.popup, "content_frame")

        # Verify that a title label was created
        assert hasattr(self.popup, "title_label")

        # Verify that a close button was created
        assert hasattr(self.popup, "close_btn")

        # Verify that current_y was initialized
        assert hasattr(self.popup, "current_y")
        assert self.popup.current_y > 0

    def test_close_method(self):
        """Test that the close method destroys the overlay."""
        # Call close
        self.popup.close()

        # Verify that overlay.destroy was called
        self.popup.overlay.destroy.assert_called_once()

    def test_add_button(self):
        """Test that add_button creates a button with the given text and command."""
        # Create a mock command
        command_mock = MagicMock()

        # Initial y position
        initial_y = self.popup.current_y

        # Create button instance mock
        button_instance = MagicMock()

        # Patch d3.Button directly
        with patch.object(
            de333r.d3, "Button", return_value=button_instance
        ) as button_mock:
            self.popup.add_button("Test Button", command_mock)

            # Verify that Button was created with correct parameters
            button_mock.assert_called_once()

            # Get the call arguments
            args, kwargs = button_mock.call_args
            assert kwargs["text"] == "Test Button"

            # Verify that current_y was incremented
            assert self.popup.current_y > initial_y

    def test_add_label(self):
        """Test that add_label creates a label with the given text."""
        # Initial y position
        initial_y = self.popup.current_y

        # Create label instance mock
        label_instance = MagicMock()

        # Patch d3.Label directly
        with patch.object(
            de333r.d3, "Label", return_value=label_instance
        ) as label_mock:
            self.popup.add_label("Test Label")

            # Verify that Label was created with correct parameters
            label_mock.assert_called_once()

            # Get the call arguments
            args, kwargs = label_mock.call_args
            assert kwargs["text"] == "Test Label"

            # Verify that current_y was incremented
            assert self.popup.current_y > initial_y

    def test_button_command_wrapper(self):
        """Test that the button command wrapper closes the popup after executing the command."""
        # Create a mock command
        command_mock = MagicMock()

        # Setup to capture the wrapped command
        captured_command = None
        button_instance = MagicMock()

        # Define a mock Button constructor that captures the command
        def mock_button(*args, **kwargs):
            nonlocal captured_command
            captured_command = kwargs.get("command")
            return button_instance

        # Patch d3.Button with our mock
        with patch.object(de333r.d3, "Button", side_effect=mock_button):
            self.popup.add_button("Test Button", command_mock)

            # Verify we captured the command
            assert captured_command is not None

            # Set up a spy on the close method
            original_close = self.popup.close
            close_spy = MagicMock()
            self.popup.close = close_spy

            # Call the captured command
            captured_command()

            # Verify that the original command was called
            command_mock.assert_called_once()

            # Verify that close was called
            close_spy.assert_called_once()

            # Restore original close method
            self.popup.close = original_close

    def test_popup_appearance(self):
        """Test that popup has correct appearance settings."""
        # Create mocks with correct kwargs
        self.popup.content_frame = MagicMock()
        self.popup.content_frame.kwargs = {"bg": config.config["ui"].BACKGROUND_COLOR}

        self.popup.title_label = MagicMock()
        self.popup.title_label.kwargs = {
            "fg": config.config["ui"].PRIMARY_COLOR,
            "bg": config.config["ui"].BACKGROUND_COLOR,
        }

        self.popup.close_btn = MagicMock()
        self.popup.close_btn.kwargs = {
            "fg": config.config["ui"].SECONDARY_COLOR,
            "bg": config.config["ui"].BACKGROUND_COLOR,
        }

        # Get UI config
        ui_config = config.config["ui"]

        # Verify that the content frame has correct background color
        assert self.popup.content_frame.kwargs["bg"] == ui_config.BACKGROUND_COLOR

        # Verify that the title label has correct font and colors
        assert self.popup.title_label.kwargs["fg"] == ui_config.PRIMARY_COLOR
        assert self.popup.title_label.kwargs["bg"] == ui_config.BACKGROUND_COLOR

        # Verify that the close button has correct colors
        assert self.popup.close_btn.kwargs["fg"] == ui_config.SECONDARY_COLOR
        assert self.popup.close_btn.kwargs["bg"] == ui_config.BACKGROUND_COLOR
