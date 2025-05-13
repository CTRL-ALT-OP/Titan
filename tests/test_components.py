import importlib.util
from unittest.mock import MagicMock, patch


import mock_tk


def test_config_module():
    """Test that the config module loads properly."""
    spec = importlib.util.spec_from_file_location("config", "config.py")
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    config = config_module.config

    # Verify config has expected structure
    assert "window" in config
    assert "animation" in config
    assert "app" in config

    # Verify window config
    assert hasattr(config["window"], "WINDOW_WIDTH")
    assert hasattr(config["window"], "WINDOW_HEIGHT")


def test_de333r_module():
    """Test de333r module with mocked tkinter."""
    # Patch tkinter before importing de333r
    with patch.dict("sys.modules", {"tkinter": mock_tk, "d3": mock_tk}):
        spec = importlib.util.spec_from_file_location("de333r", "de333r.py")
        de333r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(de333r)

        # Test page class
        page = de333r.page(MagicMock(), MagicMock())
        assert not page.finished
        assert page.root is not None
        assert page.true_root is not None


def test_apper_module_basic():
    """Test basic apper module functionality with mocked filesystem."""
    # Mock filesystem to return a mix of valid apps and restricted files
    mock_files = [
        "clock.py",
        "stopwatch.py",
        "calculator.py",
        "__init__.py",
        "__pycache__",
    ]

    # Create a mock config class that matches the actual structure
    class MockAppConfig:
        APPS_DIRECTORY = "apps"
        APPS_PRIORITY_ORDER = ["calculator", "clock"]
        RESTRICTED_FILES = ["__init__.py", "__pycache__"]

    # Create the config dictionary with our mock class
    mock_config = {"app": MockAppConfig}

    def mock_join(*args):
        """Mock os.path.join to handle paths properly."""
        return "/".join(str(arg) for arg in args)

    # Set up all mocks before importing the module
    patches = [
        patch("os.listdir", return_value=mock_files),
        patch("os.path.isdir", return_value=False),
        patch("os.path.join", side_effect=mock_join),
        patch("config.config", mock_config),
    ]

    # Start all patches
    for p in patches:
        p.start()

    try:
        spec = importlib.util.spec_from_file_location("apper", "apper.py")
        apper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(apper)

        # Test list function
        apps = apper.list()

        # Verify basic structure
        assert isinstance(apps, list)
        assert len(apps) > 0
        assert all(isinstance(app, str) for app in apps)

        # Verify app discovery and ordering
        assert "calculator" in apps
        assert "clock" in apps
        assert "stopwatch" in apps
        assert "__init__.py" not in apps
        assert "__pycache__" not in apps

        # Verify priority ordering
        assert apps.index("calculator") < apps.index("clock")
        assert apps.index("clock") < apps.index("stopwatch")

    finally:
        # Stop all patches
        for p in patches:
            p.stop()


def test_page_tween_animation():
    """Test the page tween animation functionality."""
    # Create mock parameters
    with patch.dict("sys.modules", {"tkinter": mock_tk, "d3": mock_tk}):
        spec = importlib.util.spec_from_file_location("de333r", "de333r.py")
        de333r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(de333r)
        root_mock = MagicMock()
        true_root_mock = MagicMock()
        frame_2_mock = MagicMock()
        frame_2_mock.page_frame = MagicMock()

        # Create a page instance
        page = de333r.page(root_mock, true_root_mock)
        page.page_frame = MagicMock()  # Ensure page_frame is a MagicMock

        # Mock the necessary methods
        with patch.object(true_root_mock, "update") as mock_update:
            with patch.object(true_root_mock, "after") as mock_after:
                # Call tween
                page.tween(frame_2_mock, 300, direction=1)

                # Verify initial placement
                frame_2_mock.page_frame.place.assert_called_once()
                page.page_frame.pack_forget.assert_called_once()

                # Verify animation setup
                assert not page.finished
                assert page.bounding_x is not None
                assert page.curr_x is not None

                # Verify after was called to start animation
                mock_after.assert_called_once()


def test_page_tween_animation_backward():
    """Test the page tween animation functionality in backward direction."""
    # Create mock parameters
    with patch.dict("sys.modules", {"tkinter": mock_tk, "d3": mock_tk}):
        spec = importlib.util.spec_from_file_location("de333r", "de333r.py")
        de333r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(de333r)
        root_mock = MagicMock()
        true_root_mock = MagicMock()
        frame_2_mock = MagicMock()
        frame_2_mock.page_frame = MagicMock()

        # Create a page instance
        page = de333r.page(root_mock, true_root_mock)
        page.page_frame = MagicMock()  # Ensure page_frame is a MagicMock

        # Mock the necessary methods
        with patch.object(true_root_mock, "update") as mock_update:
            with patch.object(true_root_mock, "after") as mock_after:
                # Call tween with backward direction
                page.tween(frame_2_mock, 300, direction=-1)

                # Verify initial placement with negative direction
                frame_2_mock.page_frame.place.assert_called_once()
                args = frame_2_mock.page_frame.place.call_args[1]
                assert args["x"] < 0  # Should be negative for backward direction

                # Verify animation setup
                assert not page.finished
                assert page.bounding_x is not None
                assert page.curr_x is not None

                # Verify after was called to start animation
                mock_after.assert_called_once()


def test_page_create():
    """Test page creation and frame setup."""
    with patch.dict("sys.modules", {"tkinter": mock_tk, "d3": mock_tk}):
        spec = importlib.util.spec_from_file_location("de333r", "de333r.py")
        de333r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(de333r)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        # Create mock parameters
        root_mock = MagicMock()
        true_root_mock = MagicMock()

        # Mock Frame creation
        mock_frame = MagicMock()
        with patch("tkinter.Frame", return_value=mock_frame) as mock_frame_class:
            # Create a page instance
            page = de333r.page(root_mock, true_root_mock)

            # Verify page frame was created
            assert hasattr(page, "page_frame")
            assert page.page_frame is not None

            # Verify frame dimensions match config
            window_config = config.config["window"]
            mock_frame_class.assert_called_with(
                root_mock,
                width=window_config.FRAME_WIDTH,
                height=window_config.FRAME_HEIGHT,
            )


def test_main_create_window_geometry():
    """Test that main window is created with correct geometry."""
    # Mock tkinter components
    mock_tk_instance = MagicMock()
    mock_frame = MagicMock()
    mock_button = MagicMock()

    with patch.dict("sys.modules", {"tkinter": mock_tk, "d3": mock_tk}):
        with patch("tkinter.Tk", return_value=mock_tk_instance):
            with patch("tkinter.Frame", return_value=mock_frame) as mock_frame_class:
                with patch("tkinter.Button", return_value=mock_button):
                    spec = importlib.util.spec_from_file_location("de333r", "de333r.py")
                    de333r = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(de333r)
                    config = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(config)

                    # Call create
                    root, bg_root, switch_l, switch_r = de333r.main.create()

                    # Verify window is not resizable
                    mock_tk_instance.resizable.assert_called_with(False, False)

                    # Verify frame dimensions
                    window_config = config.config["window"]
                    mock_frame_class.assert_called_with(
                        mock_tk_instance,
                        width=window_config.FRAME_WIDTH,
                        height=window_config.FRAME_HEIGHT,
                    )

                    # Verify button placement
                    switch_l.place.assert_called()
                    switch_r.place.assert_called()


def test_page_tween_looper():
    """Test the looper function within page tween animation."""
    with patch.dict("sys.modules", {"tkinter": mock_tk, "d3": mock_tk}):
        spec = importlib.util.spec_from_file_location("de333r", "de333r.py")
        de333r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(de333r)

        # Create mock parameters
        root_mock = MagicMock()
        true_root_mock = MagicMock()
        frame_2_mock = MagicMock()
        frame_2_mock.page_frame = MagicMock()

        # Create a page instance
        page = de333r.page(root_mock, true_root_mock)
        page.page_frame = MagicMock()

        # Set up initial state
        page.bounding_x = 100
        page.curr_x = 100

        # Mock the necessary methods
        with patch.object(true_root_mock, "update") as mock_update:
            with patch.object(true_root_mock, "after") as mock_after:
                # Start the tween animation
                page.tween(frame_2_mock, 300, direction=1)

                # Get the looper function that was passed to after
                looper_func = mock_after.call_args[0][1]

                # Simulate first iteration of looper
                looper_func(page)

                # Verify frame positions were updated
                frame_2_mock.page_frame.place.assert_called()
                page.page_frame.place.assert_called()

                # Verify curr_x was decremented
                assert page.curr_x == 285  # 100 - TWEEN_STEP_SIZE(15)

                # Verify after was called for next iteration
                mock_after.assert_called()

                # Simulate final iteration (curr_x <= 0)
                page.curr_x = 0
                looper_func(page)

                # Verify finished flag was set
                assert page.finished

                # Verify no more after calls were made
                assert mock_after.call_count == 2  # Initial + one iteration
