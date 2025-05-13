import pytest
import importlib.util
from unittest.mock import MagicMock, patch, ANY


# Use importlib to load modules properly to avoid execution of module-level code
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load modules without executing module-level code that might try to access filesystem
config = load_module_from_path("config", "config.py")
de333r = load_module_from_path("de333r", "de333r.py")

# For main and apper, we need to patch before import
with patch("apper._get_app_list", return_value=["clock", "stopwatch"]):
    with patch("apper._app_modules", [MagicMock(), MagicMock()]):
        main = load_module_from_path("main", "main.py")
        apper = load_module_from_path("apper", "apper.py")


class TestTitanApp:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.app = main.TitanApp()

    def test_init(self):
        """Test that main app initializes correctly."""
        assert self.app.list_apps is not None
        assert self.app.current_page == 0
        assert self.app.loaded_page is None
        assert self.app.loaded_app is None
        assert self.app.root is None
        assert self.app.bg_root is None
        assert self.app.switch_l is None
        assert self.app.switch_r is None
        assert (
            self.app.anim_config.TWEEN_DURATION
            == config.config["animation"].TWEEN_DURATION
        )
        assert (
            self.app.anim_config.TWEEN_CHECK_INTERVAL
            == config.config["animation"].TWEEN_CHECK_INTERVAL
        )
        assert (
            self.app.anim_config.TWEEN_STEP_SIZE
            == config.config["animation"].TWEEN_STEP_SIZE
        )

    def test_get_next_page_index_forward(self):
        """Test getting the next page index when going forward."""
        # Set up test case
        self.app.list_apps = ["app1", "app2", "app3"]
        self.app.current_page = 0

        # Test going forward
        next_index = self.app._get_next_page_index(1)
        assert next_index == 1

        # Test wrapping around when at the end
        self.app.current_page = 2
        next_index = self.app._get_next_page_index(1)
        assert next_index == 0

    def test_get_next_page_index_backward(self):
        """Test getting the next page index when going backward."""
        # Set up test case
        self.app.list_apps = ["app1", "app2", "app3"]
        self.app.current_page = 1

        # Test going backward
        next_index = self.app._get_next_page_index(-1)
        assert next_index == 0

        # Test wrapping around when at the beginning
        self.app.current_page = 0
        next_index = self.app._get_next_page_index(-1)
        assert next_index == 2

    @pytest.mark.parametrize(
        "index,expected_class",
        [
            (0, "clock"),  # First app based on priority
            (1, "stopwatch"),  # Second app based on priority
        ],
    )
    def test_list_priority_order(self, index, expected_class):
        """Test that app priority order is respected."""
        apps = apper.list()
        assert apps[index] == expected_class

    @patch("de333r.main.create")
    @patch("apper.app")
    @patch("main.titan.page")
    def test_run_initializes_first_app(self, mock_page, mock_app, mock_create):
        """Test that the run method initializes the first app."""
        # Mock the UI components
        mock_root = MagicMock()
        mock_bg_root = MagicMock()
        mock_switch_l = MagicMock()
        mock_switch_r = MagicMock()
        mock_create.return_value = (
            mock_root,
            mock_bg_root,
            mock_switch_l,
            mock_switch_r,
        )

        # Mock page and app creation
        mock_loaded_page = MagicMock()
        mock_loaded_page.page_frame = MagicMock()
        mock_page.return_value = mock_loaded_page

        mock_loaded_app = MagicMock()
        mock_app.return_value = mock_loaded_app

        # Call run method
        with patch.object(mock_root, "mainloop"):  # Prevent actual UI loop
            self.app.run()

        # Assertions
        mock_create.assert_called_once()
        assert self.app.root == mock_root
        assert self.app.bg_root == mock_bg_root
        assert self.app.switch_l == mock_switch_l
        assert self.app.switch_r == mock_switch_r

        # Verify switch commands are set
        mock_switch_l.configure.assert_called_with(command=ANY)
        mock_switch_r.configure.assert_called_with(command=ANY)

    def test_switch_forward(self):
        """Test switching forward to the next app."""
        # Set up test case
        self.app.list_apps = ["app1", "app2", "app3"]
        self.app.current_page = 0
        self.app.loaded_page = MagicMock()
        self.app.loaded_app = MagicMock()
        self.app.root = MagicMock()
        self.app.bg_root = MagicMock()
        self.app.switch_l = MagicMock()
        self.app.switch_r = MagicMock()

        # Mock the necessary methods
        with patch.object(self.app, "_create_next_page_and_app") as mock_create:
            mock_create.return_value = (MagicMock(), MagicMock())

            # Call switch
            self.app.switch(1)

            # Verify switches were disabled
            self.app.switch_l.configure.assert_called_with(state="disabled")
            self.app.switch_r.configure.assert_called_with(state="disabled")

            # Verify tween was called
            self.app.loaded_page.tween.assert_called_once()

    def test_switch_backward(self):
        """Test switching backward to the previous app."""
        # Set up test case
        self.app.list_apps = ["app1", "app2", "app3"]
        self.app.current_page = 1
        self.app.loaded_page = MagicMock()
        self.app.loaded_app = MagicMock()
        self.app.root = MagicMock()
        self.app.bg_root = MagicMock()
        self.app.switch_l = MagicMock()
        self.app.switch_r = MagicMock()

        # Mock the necessary methods
        with patch.object(self.app, "_create_next_page_and_app") as mock_create:
            mock_create.return_value = (MagicMock(), MagicMock())

            # Call switch
            self.app.switch(-1)

            # Verify switches were disabled
            self.app.switch_l.configure.assert_called_with(state="disabled")
            self.app.switch_r.configure.assert_called_with(state="disabled")

            # Verify tween was called with correct direction
            self.app.loaded_page.tween.assert_called_once()
            args = self.app.loaded_page.tween.call_args[1]
            assert args["direction"] == -1

    def test_transition_complete(self):
        """Test that transition completion is handled correctly."""
        # Import the actual TitanApp class
        spec = importlib.util.spec_from_file_location("main", "main.py")
        main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main)

        # Create a real TitanApp instance
        app = main.TitanApp()

        # Create and store mocks
        loaded_page_mock = MagicMock()
        mock_app_module = MagicMock()
        loaded_app_mock = MagicMock()
        root_mock = MagicMock()

        # Set up the mocks
        app.loaded_page = loaded_page_mock
        app.loaded_app = loaded_app_mock
        app.loaded_app.app = mock_app_module
        app.loaded_app.app.destroy = MagicMock()
        app.root = root_mock
        app._enable_switches = MagicMock()

        # Create next state
        next_page = MagicMock()
        next_app = MagicMock()
        next_index = 1

        # Call the actual transition complete method
        assert app.loaded_app.app == mock_app_module
        app._transition_complete(next_app, next_page, next_index)

        # Verify old app was destroyed with correct arguments
        mock_app_module.destroy.assert_called_once_with(loaded_page_mock, root_mock)

        # Verify state updates
        assert app.current_page == next_index
        assert app.loaded_page == next_page
        assert app.loaded_app == next_app
        app._enable_switches.assert_called_once()

    def test_check_tween_complete_when_finished(self):
        """Test tween completion check when animation is finished."""
        # Set up test case
        self.app.loaded_page = MagicMock()
        self.app.loaded_page.finished = True
        self.app.root = MagicMock()

        next_page = MagicMock()
        next_app = MagicMock()
        next_index = 1

        # Mock transition complete
        with patch.object(self.app, "_transition_complete") as mock_transition:
            # Call check tween complete
            self.app._check_tween_complete(next_app, next_page, next_index)

            # Verify transition complete was called
            mock_transition.assert_called_once_with(next_app, next_page, next_index)

            # Verify root.after was not called (since we're finished)
            self.app.root.after.assert_not_called()

    def test_check_tween_complete_when_not_finished(self):
        """Test tween completion check when animation is not finished."""
        # Set up test case
        self.app.loaded_page = MagicMock()
        self.app.loaded_page.finished = False
        self.app.root = MagicMock()

        next_page = MagicMock()
        next_app = MagicMock()
        next_index = 1

        # Mock transition complete
        with patch.object(self.app, "_transition_complete") as mock_transition:
            # Call check tween complete
            self.app._check_tween_complete(next_app, next_page, next_index)

            # Verify transition complete was not called
            mock_transition.assert_not_called()

            # Verify root.after was called to check again
            self.app.root.after.assert_called_once_with(
                self.app.anim_config.TWEEN_CHECK_INTERVAL, ANY  # The lambda function
            )

    def test_enable_switches(self):
        """Test that switch buttons are properly enabled."""
        # Set up test case
        self.app.switch_l = MagicMock()
        self.app.switch_r = MagicMock()

        # Call the method
        self.app._enable_switches()

        # Verify both switches were configured to normal state
        self.app.switch_l.configure.assert_called_once_with(state="normal")
        self.app.switch_r.configure.assert_called_once_with(state="normal")

    @patch("main.titan.page")
    @patch("apper.app")
    def test_create_next_page_and_app(self, mock_app, mock_page):
        """Test creation of next page and app."""
        # Set up test case
        self.app.list_apps = ["clock", "stopwatch"]
        self.app.bg_root = MagicMock()
        self.app.root = MagicMock()
        next_index = 1

        # Mock the page and app creation
        mock_next_page = MagicMock()
        mock_next_app = MagicMock()
        mock_page.return_value = mock_next_page
        mock_app.return_value = mock_next_app

        # Call the method
        result_page, result_app = self.app._create_next_page_and_app(next_index)

        # Verify page was created with correct parameters
        mock_page.assert_called_once_with(self.app.bg_root, self.app.root)
        assert result_page == mock_next_page

        # Verify app was created with correct parameters
        mock_app.assert_called_once_with(mock_next_page, "stopwatch", self.app.root)
        assert result_app == mock_next_app


class TestApperModule:
    def test_list_returns_apps(self):
        """Test that the list function returns available apps."""
        apps = apper.list()
        assert isinstance(apps, list)
        assert len(apps) > 0
        assert "clock" in apps  # Clock should be in the list based on config

    def test_app_creation(self):
        """Test that app module can be imported and loaded."""
        # Get the first app from the list
        apps = apper.list()
        first_app = apps[0]

        # Create a mock page
        page_mock = MagicMock()
        page_mock.page_frame = MagicMock()

        # Create an app instance
        app_instance = apper.app(page_mock, first_app, MagicMock())

        assert app_instance.code == first_app
        assert app_instance.app is not None


class TestConfigModule:
    def test_config_has_window_settings(self):
        """Test that config has window settings."""
        assert hasattr(config.config["window"], "WINDOW_WIDTH")
        assert hasattr(config.config["window"], "WINDOW_HEIGHT")
        assert hasattr(config.config["window"], "FRAME_WIDTH")
        assert hasattr(config.config["window"], "FRAME_HEIGHT")

    def test_config_has_animation_settings(self):
        """Test that config has animation settings."""
        assert hasattr(config.config["animation"], "TWEEN_DURATION")
        assert hasattr(config.config["animation"], "TWEEN_CHECK_INTERVAL")
        assert hasattr(config.config["animation"], "TWEEN_STEP_SIZE")


class TestDe333rModule:
    @patch("tkinter.Tk")
    @patch("tkinter.Frame")
    @patch("tkinter.Button")
    def test_main_create(self, mock_button, mock_frame, mock_tk):
        """Test that de333r.main.create returns expected components."""
        # Mock tkinter components
        mock_tk.return_value = MagicMock()
        mock_frame.return_value = MagicMock()
        mock_button.return_value = MagicMock()

        # Call the create method
        components = de333r.main.create()

        # Verify components
        assert len(components) == 4
        assert components[0] is not None  # root
        assert components[1] is not None  # bg_root
        assert components[2] is not None  # switch_btn_l
        assert components[3] is not None  # switch_btn_r

    def test_page_initialization(self):
        """Test page class initialization."""
        # Create mock parameters
        root_mock = MagicMock()
        true_root_mock = MagicMock()

        # Create a page instance
        page = de333r.page(root_mock, true_root_mock)

        # Verify page state
        assert page.root == root_mock
        assert page.true_root == true_root_mock
        assert page.finished is False


class TestApperAppClass:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.page_mock = MagicMock()
        self.page_mock.page_frame = MagicMock()
        self.root_mock = MagicMock()
        # Mock the module-level variables
        self.original_app_list = apper._app_list
        self.original_app_modules = apper._app_modules

    def teardown_method(self):
        """Restore original module-level variables after each test."""
        apper._app_list = self.original_app_list
        apper._app_modules = self.original_app_modules

    def test_app_initialization_exact_implementation(self):
        """Test the exact implementation of app initialization."""
        # Create mock app module
        mock_app_module = MagicMock()
        mock_app_module.create = MagicMock()

        # Set up the module-level variables
        apper._app_list = ["test_app"]
        apper._app_modules = [mock_app_module]

        # Create app instance
        app_instance = apper.app(self.page_mock, "test_app", self.root_mock)

        # Verify exact implementation details
        assert app_instance.code == "test_app"  # Tests self.code = code
        assert (
            app_instance.app == mock_app_module
        )  # Tests self.app = _app_modules[_app_list.index(code)]
        mock_app_module.create.assert_called_once_with(
            self.page_mock, self.root_mock
        )  # Tests self.app.create(page, root)

    def test_app_module_index_lookup(self):
        """Test that app module is correctly looked up using index."""
        # Create mock app modules
        mock_module1 = MagicMock()
        mock_module2 = MagicMock()

        # Set up the module-level variables with multiple apps
        apper._app_list = ["app1", "app2"]
        apper._app_modules = [mock_module1, mock_module2]

        # Create app instance for second app
        app_instance = apper.app(self.page_mock, "app2", self.root_mock)

        # Verify correct module was loaded
        assert app_instance.app == mock_module2
        assert app_instance.app != mock_module1

    def test_app_create_called_with_correct_params(self):
        """Test that app.create is called with exactly the right parameters."""
        # Create mock app module
        mock_app_module = MagicMock()
        mock_app_module.create = MagicMock()

        # Set up the module-level variables
        apper._app_list = ["test_app"]
        apper._app_modules = [mock_app_module]

        # Create app instance
        apper.app(self.page_mock, "test_app", self.root_mock)

        # Verify create was called with exact parameters
        mock_app_module.create.assert_called_once_with(self.page_mock, self.root_mock)

    def test_app_with_nonexistent_code(self):
        """Test that app raises ValueError when code is not in _app_list."""
        # Set up the module-level variables
        apper._app_list = ["app1"]
        apper._app_modules = [MagicMock()]

        # Attempt to create app with nonexistent code
        with pytest.raises(ValueError):
            apper.app(self.page_mock, "nonexistent", self.root_mock)
