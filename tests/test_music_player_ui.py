import importlib
import sys
import os
from unittest.mock import MagicMock, patch, call
import pytest


@pytest.fixture
def mock_ui_imports():
    """Mock necessary UI imports for testing."""
    # Mock tkinter
    mock_tk = MagicMock()
    mock_tk.Label = MagicMock(return_value=MagicMock())
    mock_tk.Button = MagicMock(return_value=MagicMock())
    mock_tk.Frame = MagicMock(return_value=MagicMock())
    mock_tk.Scale = MagicMock(return_value=MagicMock())
    mock_tk.StringVar = MagicMock(return_value=MagicMock())
    mock_tk.Canvas = MagicMock(return_value=MagicMock())
    mock_tk.Scrollbar = MagicMock(return_value=MagicMock())
    mock_tk.OptionMenu = MagicMock(return_value=MagicMock())
    mock_tk.Entry = MagicMock(return_value=MagicMock())
    mock_tk.Listbox = MagicMock(return_value=MagicMock())

    # Mock pygame
    mock_pygame = MagicMock()
    mock_pygame.mixer = MagicMock()
    mock_pygame.mixer.init = MagicMock(return_value=True)
    mock_pygame.mixer.get_init = MagicMock(return_value=True)
    mock_pygame.mixer.music = MagicMock()
    mock_pygame.mixer.music.load = MagicMock()
    mock_pygame.mixer.music.play = MagicMock()
    mock_pygame.mixer.music.pause = MagicMock()
    mock_pygame.mixer.music.unpause = MagicMock()
    mock_pygame.mixer.music.stop = MagicMock()
    mock_pygame.mixer.music.get_busy = MagicMock(return_value=False)
    mock_pygame.mixer.music.get_pos = MagicMock(return_value=-1)
    mock_pygame.mixer.Sound = MagicMock()
    mock_pygame.mixer.Sound.return_value = MagicMock()
    mock_pygame.mixer.Sound.return_value.get_length = MagicMock(return_value=180)

    # Mock config
    mock_config = {
        "ui": MagicMock(
            FONT_FAMILY="Arial",
            BACKGROUND_COLOR="#000000",
            PRIMARY_COLOR="#FFFFFF",
            ACTIVE_BACKGROUND_COLOR="#333333",
            LOADING_FONT_SIZE=14,
            TITLE_FONT_SIZE=16,
            BUTTON_FONT_SIZE=12,
        ),
        "animation": MagicMock(
            TWEEN_DURATION=100,
        ),
        "window": MagicMock(
            FRAME_WIDTH=400,
            FRAME_HEIGHT=300,
        ),
    }

    mock_config_module = MagicMock()
    mock_config_module.config = mock_config

    # Apply mocks
    sys.modules["tkinter"] = mock_tk
    sys.modules["pygame"] = mock_pygame
    sys.modules["config"] = mock_config_module

    yield mock_tk, mock_pygame, mock_config_module

    # Remove mocks after test
    if "tkinter" in sys.modules:
        del sys.modules["tkinter"]
    if "pygame" in sys.modules:
        del sys.modules["pygame"]
    if "config" in sys.modules:
        del sys.modules["config"]


@pytest.fixture
def ui_music_player(mock_ui_imports):
    """Create a music player instance ready for UI testing."""
    # Import the module
    if "apps.music_player" in sys.modules:
        del sys.modules["apps.music_player"]

    module = importlib.import_module("apps.music_player")

    # Create a new player
    player = module.MusicPlayer()

    # Create fake song paths and mock directory functions
    fake_songs = ["song1.mp3", "song2.mp3", "song3.mp3"]

    # Mock os functions
    with patch("os.listdir", return_value=fake_songs), patch("os.makedirs"), patch(
        "os.path.isdir", return_value=True
    ), patch("os.path.exists", return_value=True), patch(
        "os.path.isabs", return_value=False
    ), patch(
        "os.path.join", lambda *args: "/".join(args)
    ), patch(
        "builtins.open", MagicMock()
    ):

        # Set up UI elements
        player.root = MagicMock()
        player.page = MagicMock()
        player.page.page_frame = MagicMock()

        # Load songs
        player.playlist.load_songs()

        # Mock UI elements
        player.song_label = MagicMock()
        player.pause_play = MagicMock()
        player.progress_slider = MagicMock()
        player.progress_slider.get.return_value = 50
        player.time_display_label = MagicMock()
        player.canvas = MagicMock()
        player.scrollbar = MagicMock()
        player.scrollable_frame = MagicMock()
        player.playlist_selector = MagicMock()
        player.playlist_selector_var = MagicMock()
        player.playlist_selector_var.get.return_value = "All Songs"
        player.delete_playlist_btn = MagicMock()
        player.create_playlist_btn = MagicMock()
        player.add_song_btn = MagicMock()
        player.remove_song_btn = MagicMock()
        player.notification_frame = MagicMock()
        player.notification_label = MagicMock()
        player.dialog_active = False
        player.dialog_frame = None
        player.notification_timer = None
        player.ui_built = True

        # Return the player
        yield player, module


def test_ui_build_methods(ui_music_player):
    """Test the UI building methods."""
    player, module = ui_music_player

    # Test _build_full_ui
    with patch.object(player, "_create_control_buttons"):
        with patch.object(player, "_create_playlist_container"):
            with patch.object(player, "_create_notification_frame"):
                player._build_full_ui()

    # Test _create_playlist_items with different scenarios
    player._create_playlist_items()

    # Test with no songs
    with patch.object(player.playlist, "has_songs", return_value=False):
        player._create_playlist_items()

    # Test with not loaded
    player.playlist.songs_loaded = False
    player._create_playlist_items()
    player.playlist.songs_loaded = True

    # Test _update_playlist_selector
    player._update_playlist_selector()


def test_dialog_creation_and_callbacks(ui_music_player):
    """Test dialog creation and callbacks."""
    player, module = ui_music_player

    # Test _show_create_playlist_dialog
    # Mock entry widget behavior
    entry_mock = MagicMock()
    entry_mock.get.return_value = "New Test Playlist"

    with patch("tkinter.Entry", return_value=entry_mock):
        with patch("tkinter.Button"):
            with patch("tkinter.Label"):
                with patch("tkinter.Frame"):
                    with patch.object(
                        player.playlist, "create_playlist", return_value=True
                    ):
                        with patch.object(player, "_update_playlist_selector"):
                            with patch.object(player, "_on_playlist_selected"):
                                with patch.object(player, "_show_notification"):
                                    # Show dialog
                                    player._show_create_playlist_dialog()

                                    # Verify dialog state
                                    assert player.dialog_active

                                    # Test with empty playlist name
                                    entry_mock.get.return_value = ""

                                    # Simulate create_playlist failure (duplicate name)
                                    with patch.object(
                                        player.playlist,
                                        "create_playlist",
                                        return_value=False,
                                    ):
                                        player._show_notification.reset_mock()
                                        # This would be called by the button callback
                                        # player._show_notification would be called with error


def test_add_song_dialog(ui_music_player):
    """Test add song dialog."""
    player, module = ui_music_player

    # Test _show_add_song_dialog
    # First test with All Songs playlist
    player.playlist_selector_var.get.return_value = "All Songs"
    with patch.object(player, "_show_notification"):
        player._show_add_song_dialog()
        player._show_notification.assert_called()

    # Now test with custom playlist
    player.playlist_selector_var.get.return_value = "Custom Playlist"
    player.dialog_active = False

    # Mock listbox behavior
    listbox_mock = MagicMock()
    listbox_mock.curselection.return_value = [0, 1]  # Select first two songs
    listbox_mock.get.side_effect = ["Song 1", "Song 2"]

    with patch("tkinter.Listbox", return_value=listbox_mock):
        with patch("tkinter.Frame"):
            with patch("tkinter.Label"):
                with patch("tkinter.Button"):
                    with patch("tkinter.Scrollbar"):
                        with patch.object(
                            player.playlist,
                            "add_song_to_current_playlist",
                            return_value=True,
                        ):
                            with patch.object(player, "_show_notification"):
                                with patch.object(player, "_create_playlist_items"):
                                    # Show dialog
                                    player._show_add_song_dialog()

                                    # Verify dialog was created
                                    assert player.dialog_active


def test_player_initialization_and_destroy(ui_music_player):
    """Test player initialization and cleanup."""
    player, module = ui_music_player

    # Test create_widgets
    mock_page = MagicMock()
    mock_page.page_frame = MagicMock()
    mock_root = MagicMock()

    # Make after call the function immediately
    mock_root.after.side_effect = lambda delay, func: func()

    # Mock _initialize_player
    with patch.object(player, "_initialize_player"):
        player.root = mock_root
        player.create_widgets(mock_page)
        player._initialize_player.assert_called_once()

    # Test destroy
    module._music_player_instance = player

    # Mock pygame mixer state
    with patch.object(player, "_unbind_scroll_events"):
        with patch.object(player, "_stop_song_end_checker"):
            with patch.object(player, "_stop_progress_updates"):
                with patch("pygame.mixer.get_init", return_value=True):
                    with patch("pygame.mixer.music.stop"):
                        with patch("pygame.mixer.quit"):
                            module.destroy(mock_page, mock_root)


def test_notification_system(ui_music_player):
    """Test the notification system."""
    player, module = ui_music_player

    # Set up notification components
    player.notification_frame = MagicMock()
    player.notification_label = MagicMock()
    player.root = MagicMock()

    # Test with existing timer
    player.notification_timer = 123
    player._show_notification("Test notification", duration=1000)
    player.root.after_cancel.assert_called_with(123)

    # Test with success type
    player._show_notification("Success!", notification_type="success", duration=2000)

    # Test notification disappearing
    player.notification_timer = 456
    player.notification_frame.place_forget.reset_mock()
    # Manually trigger the after callback
    player.root.after.side_effect = lambda ms, func: func()
    player._show_notification("Quick notification", duration=10)
    player.notification_frame.place_forget.assert_called_once()


def test_additional_methods(ui_music_player):
    """Test additional methods for coverage."""
    player, module = ui_music_player

    # Test start_current_song
    with patch("sys.modules") as mock_modules:
        # Mock pygame.mixer and its methods
        mock_mixer = MagicMock()
        mock_mixer_music = MagicMock()
        mock_sound = MagicMock()

        # Set up the mock_sound to return a mock with get_length method
        mock_sound_instance = MagicMock()
        mock_sound_instance.get_length.return_value = 180  # 3 minutes
        mock_sound.return_value = mock_sound_instance

        # Connect the mocks
        mock_mixer.music = mock_mixer_music
        mock_mixer.Sound = mock_sound

        # Set up the pygame mock
        mock_pygame = MagicMock()
        mock_pygame.mixer = mock_mixer

        # Replace the sys.modules entry
        mock_modules.__getitem__.return_value = mock_pygame
        mock_modules.__contains__.return_value = True

        # Setup for successful test
        player.state.current_song_index = 0
        with patch.object(
            player.playlist, "get_current_song_path", return_value="song1.mp3"
        ):
            player._start_current_song()
            assert player.state.is_playing

    # Test _pause_playback and _resume_playback
    with patch.object(player, "_stop_progress_updates"):
        player._pause_playback()
        assert not player.state.is_playing
        assert player.state.song_paused

    with patch.object(player, "_update_playing_state_ui"):
        # Test when paused
        player.state.song_paused = True
        with patch.object(player, "_start_progress_updates"):
            player._resume_playback()

        # Test when not paused (should call _start_current_song)
        player.state.song_paused = False
        with patch.object(player, "_start_current_song"):
            player._resume_playback()
