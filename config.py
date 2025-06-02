"""Configuration module for the Titan application.

This module contains all configurable values for the application,
centralizing hard-coded values that were scattered throughout the codebase.
"""


class WindowConfig:
    """Window geometry and layout configuration."""

    WINDOW_WIDTH = 350
    WINDOW_HEIGHT = 300
    FRAME_WIDTH = 300
    FRAME_HEIGHT = 250  # Reduced to account for bottom nav
    FRAME_X_OFFSET = 25
    FRAME_Y_OFFSET = 0
    BUTTON_WIDTH = 25
    BOTTOM_NAV_HEIGHT = 50


class AnimationConfig:
    """Animation timing configuration."""

    TWEEN_DURATION = 300  # milliseconds
    TWEEN_CHECK_INTERVAL = 20  # milliseconds
    TWEEN_STEP_SIZE = 15  # pixels

    NOTIFICATION_DURATION = 500  # milliseconds


class AppConfig:
    """Application-specific configuration."""

    APPS_DIRECTORY = "apps"
    APPS_PRIORITY_ORDER = [
        "clock",
        "stopwatch",
    ]  # Apps that should appear first
    RESTRICTED_FILES = ["__init__.py", "__pycache__"]


class UIConfig:
    """User interface configuration."""

    FONT_FAMILY = "Alien Encounters"

    # Colors
    PRIMARY_COLOR = "lime green"
    SECONDARY_COLOR = "red"
    BACKGROUND_COLOR = "black"
    ACTIVE_BACKGROUND_COLOR = "dark grey"

    # Font settings
    TITLE_FONT_SIZE = 40
    BUTTON_FONT_SIZE = 20
    LOADING_FONT_SIZE = 20


class ClockConfig:
    """Clock app specific settings."""

    CLOCK_MAIN_FONT_SIZE = 60
    CLOCK_SECONDARY_FONT_SIZE = 20
    CLOCK_TERTIARY_FONT_SIZE = 12
    CLOCK_UPDATE_INTERVAL = 250  # milliseconds
    CLOCK_STARTUP_DELAY = 50  # milliseconds


class BlockoidConfig:
    """Blockoid game specific settings."""

    # Game dimensions
    GAME_HEIGHT = 300

    # Block dimensions
    BLOCK_SIZE = 10

    # Colors
    PLAYER_COLOR = "red"
    GROUND_COLOR = "#363636"
    SKY_COLOR = "dimgrey"
    CLOUD_COLOR = "dark red"


# Create a single configuration instance
config = {
    "window": WindowConfig,
    "animation": AnimationConfig,
    "app": AppConfig,
    "ui": UIConfig,
    "clock": ClockConfig,
}
