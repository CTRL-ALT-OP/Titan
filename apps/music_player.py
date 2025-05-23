import tkinter as d3
import os
import pygame
import time
from config import config

# Define constants
SONG_END_CHECK_INTERVAL_MS = 1000
PROGRESS_UPDATE_INTERVAL_MS = 250
TIME_DISPLAY_FORMAT = "{current_min}:{current_sec:02d} / {total_min}:{total_sec:02d}"

# Module-level instance
_music_player_instance = None


class PlaybackState:
    """Class to manage playback state and timing logic"""

    def __init__(self):
        self.is_playing = False
        self.song_paused = False
        self.is_seeking = False
        self.current_song_index = 0
        self.current_song_length = 0
        self.song_start_time = 0
        self.seek_offset = 0
        self.pause_time = 0

    def pause(self):
        self.is_playing = False
        self.song_paused = True
        self.pause_time = time.time()

    def resume(self):
        self.is_playing = True
        if self.song_paused:
            pause_duration = time.time() - self.pause_time
            self.song_start_time += pause_duration
            self.pause_time = 0
            self.song_paused = False

    def start_new_song(self):
        self.song_start_time = time.time()
        self.seek_offset = 0
        self.song_paused = False
        self.is_playing = True

    def seek_to_position(self, position_percent, song_length):
        if song_length <= 0:
            return 0

        new_position_seconds = max(0, (position_percent / 100) * (song_length / 1000))
        self.song_start_time = time.time() - new_position_seconds
        self.seek_offset = new_position_seconds * 1000  # Convert to milliseconds

        return new_position_seconds

    def get_elapsed_time_ms(self):
        if not self.is_playing and not self.song_paused:
            return 0

        return (time.time() - self.song_start_time) * 1000  # ms


class Playlist:
    """Class to represent a single playlist"""

    def __init__(self, name, songs=None):
        self.name = name
        self.song_paths = [] if songs is None else songs
        self.display_names = []
        self._update_display_names()

    def _update_display_names(self):
        """Update display names from song paths"""
        self.display_names = []
        for path in self.song_paths:
            filename = os.path.basename(path)
            self.display_names.append(os.path.splitext(filename)[0])

    def add_song(self, song_path):
        """Add a song to the playlist"""
        if song_path not in self.song_paths:
            self.song_paths.append(song_path)
            self._update_display_names()
            return True
        return False

    def remove_song(self, index):
        """Remove a song from the playlist"""
        if 0 <= index < len(self.song_paths):
            self.song_paths.pop(index)
            self._update_display_names()
            return True
        return False

    def has_songs(self):
        """Check if the playlist has any songs"""
        return bool(self.song_paths)

    def get_song_path(self, index):
        """Get the path of a song by index"""
        if not self.song_paths or index >= len(self.song_paths):
            return None
        return self.song_paths[index]

    def get_song_name(self, index):
        """Get the display name of a song by index"""
        if not self.display_names or index >= len(self.display_names):
            return "No song selected"
        return self.display_names[index]


class PlaylistManager:
    """Class to manage playlist operations"""

    def __init__(
        self,
        songs_folder="apps/_music_player/songs",
        playlists_file="apps/_music_player/playlists.txt",
    ):
        self.songs_folder = songs_folder
        self.playlists_file = playlists_file
        self.available_songs = []  # All songs in the songs folder
        self.available_song_names = []  # Display names for all available songs
        self.playlists = []  # List of Playlist objects
        self.current_playlist_index = 0
        self.songs_loaded = False

        # Make sure directories exist
        os.makedirs(os.path.dirname(songs_folder), exist_ok=True)
        os.makedirs(os.path.dirname(playlists_file), exist_ok=True)

    def load_songs(self):
        """Load songs from the songs folder"""
        self.available_songs = []
        self.available_song_names = []

        # Ensure directories exist
        os.makedirs(os.path.dirname(self.songs_folder), exist_ok=True)
        os.makedirs(os.path.dirname(self.playlists_file), exist_ok=True)

        if not os.path.isdir(self.songs_folder):
            print(f"Songs folder not found: {self.songs_folder}")
            self.available_song_names = ["No songs found"]
            self.songs_loaded = True
            return

        for filename in os.listdir(self.songs_folder):
            if filename.endswith((".mp3", ".wav")):
                full_path = os.path.join(self.songs_folder, filename)
                self.available_songs.append(full_path)
                self.available_song_names.append(os.path.splitext(filename)[0])

        if not self.available_songs:
            self.available_song_names = ["No songs found"]

        # Create a default "All Songs" playlist if we have songs
        if self.available_songs and not self.playlists:
            all_songs_playlist = Playlist("All Songs", self.available_songs.copy())
            self.playlists.append(all_songs_playlist)

        self.load_playlists()
        self.songs_loaded = True

    def get_current_song_path(self, index):
        if not self.playlists or self.current_playlist_index >= len(self.playlists):
            return None
        song_path = self.playlists[self.current_playlist_index].get_song_path(index)

        # If path doesn't include the songs folder, add it
        if (
            song_path
            and not os.path.isabs(song_path)
            and not song_path.startswith(self.songs_folder)
        ):
            return os.path.join(self.songs_folder, song_path)
        return song_path

    def get_current_song_name(self, index):
        if not self.playlists or self.current_playlist_index >= len(self.playlists):
            return "No song selected"
        return self.playlists[self.current_playlist_index].get_song_name(index)

    def has_songs(self):
        if not self.playlists or self.current_playlist_index >= len(self.playlists):
            return False
        return self.playlists[self.current_playlist_index].has_songs()

    def get_playlist_display_names(self):
        """Get all playlist names"""
        return [playlist.name for playlist in self.playlists]

    def create_playlist(self, name):
        """Create a new playlist with the given name"""
        # Check if playlist with the same name already exists
        for playlist in self.playlists:
            if playlist.name.lower() == name.lower():
                return False

        self.playlists.append(Playlist(name))
        self.save_playlists()
        return True

    def delete_playlist(self, index):
        """Delete a playlist by index"""
        if 0 <= index < len(self.playlists):
            self.playlists.pop(index)
            if self.current_playlist_index >= len(self.playlists) and self.playlists:
                self.current_playlist_index = len(self.playlists) - 1
            self.save_playlists()
            return True
        return False

    def switch_playlist(self, index):
        """Switch to a different playlist"""
        if 0 <= index < len(self.playlists):
            self.current_playlist_index = index
            return True
        return False

    def add_song_to_current_playlist(self, song_index):
        """Add a song from available songs to current playlist"""
        if (
            self.playlists
            and self.current_playlist_index < len(self.playlists)
            and 0 <= song_index < len(self.available_songs)
        ):
            song_path = self.available_songs[song_index]

            # For custom playlists, store only the filename, not the full path
            if self.playlists[self.current_playlist_index].name != "All Songs":
                song_path = os.path.basename(song_path)

            return self.playlists[self.current_playlist_index].add_song(song_path)
        return False

    def remove_song_from_current_playlist(self, song_index):
        """Remove a song from current playlist"""
        if self.playlists and self.current_playlist_index < len(self.playlists):
            result = self.playlists[self.current_playlist_index].remove_song(song_index)
            if result:
                self.save_playlists()
            return result
        return False

    def save_playlists(self):
        """Save playlists to file"""
        try:
            with open(self.playlists_file, "w") as f:
                for playlist in self.playlists:
                    # Skip the "All Songs" playlist as it's generated automatically
                    if playlist.name == "All Songs":
                        continue

                    f.write(f"[{playlist.name}]\n")
                    for song_path in playlist.song_paths:
                        # Save only the filename, not the full path
                        filename = os.path.basename(song_path)
                        f.write(f"{filename}\n")
                    f.write("\n")  # Empty line between playlists
            return True
        except Exception as e:
            print(f"Error saving playlists: {e}")
            return False

    def load_playlists(self):
        """Load playlists from file"""
        if not os.path.exists(self.playlists_file):
            # Create an "All Songs" playlist if we have no saved playlists
            if self.available_songs and not self.playlists:
                all_songs_playlist = Playlist("All Songs", self.available_songs.copy())
                self.playlists = [all_songs_playlist]
            return

        try:
            # Create an "All Songs" playlist first
            all_songs_playlist = Playlist("All Songs", self.available_songs.copy())
            playlists = [all_songs_playlist]

            current_playlist = None
            with open(self.playlists_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        current_playlist = None
                        continue

                    if line.startswith("[") and line.endswith("]"):
                        playlist_name = line[1:-1]
                        current_playlist = Playlist(playlist_name)
                        playlists.append(current_playlist)
                    elif current_playlist is not None:
                        # This is a song filename, not a full path
                        # Check if the song file exists
                        filename = line
                        full_path = os.path.join(self.songs_folder, filename)
                        if os.path.exists(full_path):
                            # Only add the filename, not the full path
                            current_playlist.add_song(filename)

            self.playlists = playlists
            self.current_playlist_index = 0
            return True
        except Exception as e:
            print(f"Error loading playlists: {e}")
            return False

    @property
    def playlist_files(self):
        """Get song paths from current playlist (for backward compatibility)"""
        if not self.playlists or self.current_playlist_index >= len(self.playlists):
            return []

        # Need to convert relative paths to full paths
        full_paths = []
        for path in self.playlists[self.current_playlist_index].song_paths:
            if not os.path.isabs(path) and not path.startswith(self.songs_folder):
                full_paths.append(os.path.join(self.songs_folder, path))
            else:
                full_paths.append(path)
        return full_paths

    @property
    def playlist_display_names(self):
        """Get song names from current playlist (for backward compatibility)"""
        if not self.playlists or self.current_playlist_index >= len(self.playlists):
            return ["No songs found"]
        return self.playlists[self.current_playlist_index].display_names


class MusicPlayer:
    ICON_PLAY = "⏵"
    ICON_PAUSE = "⏸"

    def __init__(self):
        # State objects
        self.state = PlaybackState()
        self.playlist = PlaylistManager()

        # UI elements
        self.root = None
        self.page = None
        self.ui_built = False
        self.font_default = None

        # UI widgets
        self.song_label = None
        self.prev_btn = None
        self.next_btn = None
        self.pause_play = None
        self.progress_slider = None
        self.time_display_label = None
        self.playlist_container = None
        self.canvas = None
        self.scrollbar = None
        self.scrollable_frame = None
        self.loading_label_main_ui = None

        # Playlist UI elements
        self.playlist_selector = None
        self.playlist_selector_var = None
        self.playlist_frame = None
        self.create_playlist_btn = None
        self.delete_playlist_btn = None
        self.add_song_btn = None
        self.remove_song_btn = None
        self.playlist_name_entry = None

        # Dialog frames
        self.dialog_frame = None
        self.dialog_content_frame = None
        self.dialog_active = False
        self.notification_frame = None
        self.notification_label = None
        self.notification_timer = None

        # Timers and checkers
        self.song_end_check_id = None
        self.progress_update_id = None

        # Scroll event bindings
        self.wheel_bindings = []

    def play(self):
        """Toggle play/pause state and update button icon"""
        if not self.ui_built or not self.playlist.has_songs():
            return

        if self.state.is_playing:
            self._pause_playback()
        else:
            self._resume_playback()

    def _pause_playback(self):
        """Pause the current playback and update UI"""
        pygame.mixer.music.pause()
        self.pause_play.configure(text=self.ICON_PLAY)
        self.state.pause()
        self._stop_progress_updates()

    def _resume_playback(self):
        """Resume playback from paused state or start new playback"""
        if self.state.song_paused:
            pygame.mixer.music.unpause()
            self.state.resume()
        elif not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() < 0:
            self._start_current_song()

        self._update_playing_state_ui()
        self.state.is_playing = True

    def _start_current_song(self):
        """Load and play the current song, resetting necessary states"""
        song_path = self.playlist.get_current_song_path(self.state.current_song_index)
        if not song_path:
            return

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.state.start_new_song()

        try:
            sound = pygame.mixer.Sound(song_path)
            self.state.current_song_length = (
                sound.get_length() * 1000
            )  # Convert to milliseconds
        except Exception as e:
            print(f"Error getting song length: {e}")
            self.state.current_song_length = 0

    def _change_song(self, direction):
        """Change to the next or previous song"""
        if not self.ui_built or not self.playlist.has_songs():
            return

        was_playing = self.state.is_playing
        self.state.current_song_index = (
            self.state.current_song_index + direction
        ) % len(self.playlist.playlist_files)

        # Reset state for new song
        self.state.current_song_length = 0
        self.reset_state()
        # Start playback if it was playing before
        if was_playing:
            self._start_current_song()
            self._update_playing_state_ui()

    def next_song(self):
        """Move to the next song"""
        self._change_song(1)

    def prev_song(self):
        """Move to the previous song"""
        self._change_song(-1)

    def select_song(self, index):
        """Select a specific song from the playlist"""
        if (
            not self.ui_built
            or not self.playlist.has_songs()
            or not 0 <= index < len(self.playlist.playlist_files)
        ):
            return

        self.state.current_song_index = index
        self.state.current_song_length = 0
        self.reset_state()
        self._start_current_song()
        self.state.is_playing = True
        self._update_playing_state_ui()

    def reset_state(self):
        self.state.seek_offset = 0
        self.state.song_paused = False
        if self.progress_slider:
            self.progress_slider.set(0)
        self._update_time_display(0)
        self._update_song_display()

    def _update_song_display(self):
        """Update the song title display"""
        if not self.ui_built:
            if self.loading_label_main_ui:
                self.loading_label_main_ui.configure(text="Loading Songs...")
            return

        song_name = self.playlist.get_current_song_name(self.state.current_song_index)
        if self.song_label:
            self.song_label.configure(text=song_name)

    def create_widgets(self, page):
        """Create the initial UI and schedule full UI build"""
        self.page = page
        ui_config = config["ui"]
        self.page.page_frame.configure(bg=ui_config.BACKGROUND_COLOR)

        # Create loading label
        self.loading_label_main_ui = d3.Label(
            self.page.page_frame,
            text="Loading Music Player...",
            font=(ui_config.FONT_FAMILY, ui_config.LOADING_FONT_SIZE, "bold"),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
        )
        self.loading_label_main_ui.place(relx=0.5, rely=0.5, anchor="center")

        # Defer loading and UI construction
        self.root.after(config["animation"].TWEEN_DURATION, self._initialize_player)

    def _initialize_player(self):
        """Initialize pygame mixer, load songs, and build the full UI"""
        # Initialize pygame mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Load songs if needed
        if not self.playlist.songs_loaded:
            self.playlist.load_songs()

        # Remove loading label
        if self.loading_label_main_ui:
            self.loading_label_main_ui.destroy()
            self.loading_label_main_ui = None

        # Build the full UI
        self._build_full_ui()
        self.ui_built = True
        self._update_song_display()
        self._create_playlist_items()
        self._update_playlist_selector()

        # Set initial playlist selection
        if self.playlist.playlists:
            self.playlist_selector_var.set(self.playlist.playlists[0].name)
            # Disable delete button for "All Songs"
            self.delete_playlist_btn.config(state="disabled")

        # Update UI for current state
        if self.state.is_playing:
            self.pause_play.configure(text=self.ICON_PAUSE)
        else:
            self.pause_play.configure(text=self.ICON_PLAY)

        # Update progress if needed
        if pygame.mixer.get_init() and (
            self.state.is_playing or self.state.song_paused
        ):
            self._update_progress()

        # Ensure checkers are active if playing
        if (
            self.state.is_playing
            and self.playlist.has_songs()
            and pygame.mixer.music.get_busy()
        ):
            self._start_song_end_checker()
            self._start_progress_updates()

    def _build_full_ui(self):
        """Build the main UI components"""
        ui_config = config["ui"]
        button_font = (
            ui_config.FONT_FAMILY,
            int(ui_config.BUTTON_FONT_SIZE * 0.8),
            "bold",
        )
        self.font_default = (ui_config.FONT_FAMILY, ui_config.TITLE_FONT_SIZE, "bold")

        # Playlist management frame
        self.playlist_frame = d3.Frame(
            self.page.page_frame,
            bg=ui_config.BACKGROUND_COLOR,
        )
        self.playlist_frame.place(relx=00, rely=0.05, relwidth=1, height=30)

        # Playlist selector dropdown
        self.playlist_selector_var = d3.StringVar()
        self.playlist_selector = d3.OptionMenu(
            self.playlist_frame,
            self.playlist_selector_var,
            "All Songs",  # Default value
            *["All Songs"],  # Initial options
            command=self._on_playlist_selected,
        )
        self.playlist_selector.config(
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            highlightthickness=0,
            width=7,
        )
        self.playlist_selector.pack(side="left", padx=5)

        # Create playlist button
        self.create_playlist_btn = d3.Button(
            self.playlist_frame,
            text="New",
            font=(ui_config.FONT_FAMILY, 8),
            command=self._show_create_playlist_dialog,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=4,
        )
        self.create_playlist_btn.pack(side="left", padx=2)

        # Delete playlist button
        self.delete_playlist_btn = d3.Button(
            self.playlist_frame,
            text="Delete",
            font=(ui_config.FONT_FAMILY, 8),
            command=self._confirm_delete_playlist,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=6,
        )
        self.delete_playlist_btn.pack(side="left", padx=2)

        # Add song to playlist button
        self.add_song_btn = d3.Button(
            self.playlist_frame,
            text="+ Song",
            font=(ui_config.FONT_FAMILY, 8),
            command=self._show_add_song_dialog,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        )
        self.add_song_btn.pack(side="left", padx=2)

        # Remove song from playlist button
        self.remove_song_btn = d3.Button(
            self.playlist_frame,
            text="- Song",
            font=(ui_config.FONT_FAMILY, 8),
            command=self._confirm_remove_song,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=12,
        )
        self.remove_song_btn.pack(side="left", padx=2)

        # Song title label
        self.song_label = d3.Label(
            self.page.page_frame,
            font=(ui_config.FONT_FAMILY, ui_config.BUTTON_FONT_SIZE, "bold"),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            wraplength=350,
        )
        self.song_label.place(relx=0.5, rely=0.7, anchor="center")

        # Progress slider
        self.progress_slider = d3.Scale(
            self.page.page_frame,
            from_=0,
            to=100,
            orient="horizontal",
            length=300,
            command=self._on_slider_change,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=0,
            troughcolor=ui_config.PRIMARY_COLOR,
            sliderrelief="flat",
            showvalue=False,
        )
        self.progress_slider.place(relx=0.5, rely=0.8, anchor="center")

        # Time display label
        self.time_display_label = d3.Label(
            self.page.page_frame,
            text="0:00 / 0:00",
            font=(ui_config.FONT_FAMILY, 10),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
        )
        self.time_display_label.place(relx=0.75, rely=0.9, anchor="w")
        self._update_time_display(0)

        # Add slider event bindings
        self.progress_slider.bind("<ButtonPress-1>", self._on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self._on_slider_release)

        # Control buttons
        self._create_control_buttons(ui_config, button_font)

        # Playlist container
        self._create_playlist_container(ui_config)

        # Create notification frame for messages
        self._create_notification_frame(ui_config)

    def _create_notification_frame(self, ui_config):
        """Create a frame for showing notifications instead of messageboxes"""
        self.notification_frame = d3.Frame(
            self.page.page_frame,
            bg=ui_config.ACTIVE_BACKGROUND_COLOR,
            highlightthickness=1,
            highlightbackground=ui_config.PRIMARY_COLOR,
        )

        self.notification_label = d3.Label(
            self.notification_frame,
            text="",
            font=(ui_config.FONT_FAMILY, 10),
            bg=ui_config.ACTIVE_BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            wraplength=350,
            justify="center",
            padx=10,
            pady=10,
        )
        self.notification_label.pack(expand=True, fill="both")

        # Hide by default
        self.notification_frame.place_forget()

    def _create_playlist_container(self, ui_config):
        """Create the scrollable playlist container"""
        self.playlist_container = d3.Frame(
            self.page.page_frame,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.playlist_container.place(
            relx=0.1, rely=0.2, relwidth=0.8, relheight=0.45, anchor="nw"
        )

        self.canvas = d3.Canvas(
            self.playlist_container,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=0,
            bd=0,
        )
        self.scrollbar = d3.Scrollbar(
            self.playlist_container,
            orient="vertical",
            command=self.canvas.yview,
            width=10,
        )
        self.scrollable_frame = d3.Frame(
            self.canvas,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=0,
            bd=0,
        )

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Simple direct bindings for Windows and Linux
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)  # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux_up)  # Linux up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux_down)  # Linux down

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_playlist_selected(self, selected_playlist):
        """Handle playlist selection from dropdown"""
        playlist_names = self.playlist.get_playlist_display_names()
        if selected_playlist in playlist_names:
            index = playlist_names.index(selected_playlist)
            if self.playlist.switch_playlist(index):
                # Stop any currently playing music
                if self.state.is_playing:
                    pygame.mixer.music.stop()

                # Reset playback state
                self.state.is_playing = False
                self.state.song_paused = False
                self.state.current_song_index = 0
                self.state.current_song_length = 0
                self.reset_state()

                # Update button icons
                if self.pause_play:
                    self.pause_play.configure(text=self.ICON_PLAY)

                # Stop timers
                self._stop_song_end_checker()
                self._stop_progress_updates()

                # Update UI
                self._create_playlist_items()
                self._update_song_display()

                # Enable/disable delete button (don't allow deleting "All Songs")
                self.delete_playlist_btn.config(
                    state="normal" if selected_playlist != "All Songs" else "disabled"
                )

    def _update_playlist_selector(self):
        """Update the playlist selector dropdown with current playlists"""
        if not self.playlist_selector:
            return

        # Get playlist names
        playlist_names = self.playlist.get_playlist_display_names()

        # Update the dropdown menu
        menu = self.playlist_selector["menu"]
        menu.delete(0, "end")

        for name in playlist_names:
            menu.add_command(
                label=name,
                command=d3._setit(
                    self.playlist_selector_var, name, self._on_playlist_selected
                ),
            )

        # Make sure the current selection is valid
        current_selection = self.playlist_selector_var.get()
        if current_selection not in playlist_names and playlist_names:
            self.playlist_selector_var.set(playlist_names[0])

    def _start_song_end_checker(self):
        """Start checking for song completion"""
        if not self.ui_built or not self.root:
            return

        self._stop_song_end_checker()  # Cancel any existing checker
        is_background = not self.ui_built
        self.song_end_check_id = self.root.after(
            SONG_END_CHECK_INTERVAL_MS,
            lambda: self._check_song_finished(is_background_mode=is_background),
        )

    def _stop_song_end_checker(self):
        """Stop the song end checker"""
        if self.song_end_check_id and self.root:
            self.root.after_cancel(self.song_end_check_id)
            self.song_end_check_id = None

    def _start_progress_updates(self):
        """Start updating the progress slider"""
        if not self.ui_built or not self.root or not self.progress_slider:
            return

        self._stop_progress_updates()  # Cancel any existing updates
        self.progress_update_id = self.root.after(
            PROGRESS_UPDATE_INTERVAL_MS, self._update_progress
        )

    def _stop_progress_updates(self):
        """Stop progress slider updates"""
        if self.progress_update_id and self.root:
            self.root.after_cancel(self.progress_update_id)
            self.progress_update_id = None

    def _update_progress(self):
        """Update the progress slider to match current song position"""
        if (
            not self.ui_built
            or not self.state.is_playing
            or not pygame.mixer.get_init()
            or self.state.is_seeking
        ):
            # Reschedule only if needed
            if (
                self.progress_update_id
                and self.state.is_playing
                and not self.state.is_seeking
            ):
                self.progress_update_id = self.root.after(
                    PROGRESS_UPDATE_INTERVAL_MS, self._update_progress
                )
            return

        try:
            # Get current position
            elapsed_time = self.state.get_elapsed_time_ms()

            # Update slider and time display
            if elapsed_time < 0:
                self.progress_slider.set(0)
                self._update_time_display(0)
            elif self.state.current_song_length > 0:
                position_percent = min(
                    100,
                    max(0, (elapsed_time / self.state.current_song_length) * 100),
                )

                # Only update if significant change to prevent flicker
                current_slider_pos = float(self.progress_slider.get())
                if abs(current_slider_pos - position_percent) > 0.5:
                    self.progress_slider.set(position_percent)

                # Update time display
                self._update_time_display(elapsed_time / 1000)  # Convert to seconds

        except Exception as e:
            print(f"Error updating progress: {e}")

        # Reschedule update
        if (
            self.root
            and self.ui_built
            and self.state.is_playing
            and not self.state.is_seeking
        ):
            self.progress_update_id = self.root.after(
                PROGRESS_UPDATE_INTERVAL_MS, self._update_progress
            )

    def _update_time_display(self, current_seconds):
        """Update the time display label"""
        if not self.time_display_label:
            return

        current_seconds = int(current_seconds)
        total_seconds = (
            int(self.state.current_song_length / 1000)
            if self.state.current_song_length > 0
            else 0
        )

        current_min, current_sec = divmod(current_seconds, 60)
        total_min, total_sec = divmod(total_seconds, 60)

        time_text = TIME_DISPLAY_FORMAT.format(
            current_min=current_min,
            current_sec=current_sec,
            total_min=total_min,
            total_sec=total_sec,
        )
        self.time_display_label.configure(text=time_text)

    def _on_slider_press(self, event):
        """Handle slider press for seeking"""
        if not self.state.is_playing or not self.playlist.has_songs():
            return

        self.state.is_seeking = True
        pygame.mixer.music.pause()  # Pause during seeking

    def _on_slider_release(self, event):
        """Handle slider release after seeking"""
        was_playing = self.state.is_playing

        if (
            not was_playing
            or not self.playlist.has_songs()
            or not self.ui_built
            or not pygame.mixer.get_init()
        ):
            self.state.is_seeking = False
            return

        try:
            self._seek_to_slider_position()
        except Exception as e:
            print(f"Error seeking: {e}")
            try:
                self._restart_song()
            except Exception:
                pass

        self.state.is_seeking = False

        # Resume playback if it was playing before
        if was_playing:
            pygame.mixer.music.unpause()
            self._start_progress_updates()
            self._start_song_end_checker()

    def _restart_song(self):
        """Restart the current song from the beginning"""
        song_path = self.playlist.get_current_song_path(self.state.current_song_index)
        if not song_path:
            return

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.progress_slider.set(0)
        self._update_time_display(0)
        self.state.start_new_song()

    def _seek_to_slider_position(self):
        """Seek to the position indicated by the slider"""
        position_percent = float(self.progress_slider.get())

        # Get song length if needed
        if self.state.current_song_length == 0:
            song_path = self.playlist.get_current_song_path(
                self.state.current_song_index
            )
            if not song_path:
                return

            try:
                sound = pygame.mixer.Sound(song_path)
                self.state.current_song_length = sound.get_length() * 1000
            except Exception as e:
                print(f"Error getting song length for seeking: {e}")
                return
        # Calculate new position and apply seek
        new_position_seconds = self.state.seek_to_position(
            position_percent, self.state.current_song_length
        )

        # Reload and play from new position
        song_path = self.playlist.get_current_song_path(self.state.current_song_index)
        if not song_path:
            return

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(start=new_position_seconds)

        # Update slider and time display
        self.progress_slider.set(position_percent)
        self._update_time_display(new_position_seconds)

    def _on_slider_change(self, value):
        """Update slider visually during dragging"""
        if self.state.is_seeking:
            try:
                position = float(value)
                self.progress_slider.set(position)
            except Exception:
                pass

    def _check_song_finished(self, is_background_mode=False):
        """Check if song has finished and play next if needed"""
        if should_advance := (
            self.state.is_playing
            and self.playlist.has_songs()
            and pygame.mixer.get_init()
            and not pygame.mixer.music.get_busy()
            and not self.state.is_seeking
        ):
            if not is_background_mode and self.ui_built:
                # Full UI mode - use next_song() for complete state management
                self.next_song()
            else:
                # Background mode - simpler handling
                self.state.current_song_index = (
                    self.state.current_song_index + 1
                ) % len(self.playlist.playlist_files)
                try:
                    self._start_current_song()
                    if self.ui_built and self.song_label:
                        self._update_song_display()
                except Exception as e:
                    print(f"Error loading next song in background: {e}")

        # Reschedule if still playing
        if self.root and self.state.is_playing and self.song_end_check_id is not None:
            current_mode_is_background = is_background_mode or not self.ui_built
            self.song_end_check_id = self.root.after(
                SONG_END_CHECK_INTERVAL_MS,
                lambda: self._check_song_finished(
                    is_background_mode=current_mode_is_background
                ),
            )

    def _update_playing_state_ui(self):
        """Update UI elements for playing state"""
        self.pause_play.configure(text=self.ICON_PAUSE)
        self._start_song_end_checker()
        self._start_progress_updates()

    def _show_notification(self, message, duration=500, notification_type="info"):
        """Show a notification message"""
        if not self.notification_frame or not self.notification_label:
            return

        # Choose colors based on notification type
        ui_config = config["ui"]
        bg_color = ui_config.BACKGROUND_COLOR
        fg_color = ui_config.PRIMARY_COLOR

        if notification_type == "success":
            bg_color = "#ccffcc"
            fg_color = "#006600"

        # Configure the notification
        self.notification_frame.configure(bg=bg_color)
        self.notification_label.configure(text=message, bg=bg_color, fg=fg_color)

        # Position in the center of the screen
        self.notification_frame.place(
            relx=0.5, rely=0.4, anchor="center", width=350, height=100
        )

        # Cancel any existing timer
        if self.notification_timer:
            self.root.after_cancel(self.notification_timer)

        # Schedule the notification to disappear
        self.notification_timer = self.root.after(
            duration, self.notification_frame.place_forget
        )

    def _create_control_buttons(self, ui_config, button_font):
        """Create the playback control buttons"""
        # Previous button
        self.prev_btn = d3.Button(
            self.page.page_frame,
            text="⏮",
            font=button_font,
            command=self.prev_song,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=2,
            height=1,
            padx=1,
            pady=1,
        )
        self.prev_btn.place(relx=0.35, rely=0.91, relheight=0.15, anchor="center")

        # Play/Pause button
        self.pause_play = d3.Button(
            self.page.page_frame,
            text=self.ICON_PLAY,
            font=button_font,
            command=self.play,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=2,
            height=1,
            padx=1,
            pady=1,
        )
        self.pause_play.place(relx=0.5, rely=0.91, relheight=0.15, anchor="center")

        # Next button
        self.next_btn = d3.Button(
            self.page.page_frame,
            text="⏭",
            font=button_font,
            command=self.next_song,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=2,
            height=1,
            padx=1,
            pady=1,
        )
        self.next_btn.place(relx=0.65, rely=0.91, relheight=0.15, anchor="center")

    def _on_mousewheel_windows(self, event):
        """Windows mousewheel handler"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def _on_mousewheel_linux_up(self, event):
        """Linux scroll up handler"""
        self.canvas.yview_scroll(-1, "units")
        return "break"

    def _on_mousewheel_linux_down(self, event):
        """Linux scroll down handler"""
        self.canvas.yview_scroll(1, "units")
        return "break"

    def _unbind_scroll_events(self):
        """Unbind scroll wheel events to prevent conflicts"""
        if hasattr(self, "canvas") and self.canvas:
            try:
                self.canvas.unbind_all("<MouseWheel>")
                self.canvas.unbind_all("<Button-4>")
                self.canvas.unbind_all("<Button-5>")
            except Exception:
                pass

    def _create_playlist_items(self):
        """Create the playlist item buttons"""
        ui_config = config["ui"]

        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.playlist.songs_loaded:
            loading_label = d3.Label(
                self.scrollable_frame,
                text="Loading playlist...",
                font=(ui_config.FONT_FAMILY, 12),
                bg=ui_config.BACKGROUND_COLOR,
                fg=ui_config.PRIMARY_COLOR,
                anchor="w",
            )
            loading_label.pack(fill="x", pady=2)
            return

        if not self.playlist.has_songs() or self.playlist.playlist_display_names == [
            "No songs found"
        ]:
            no_songs_label = d3.Label(
                self.scrollable_frame,
                text="No songs found in the current playlist",
                font=(ui_config.FONT_FAMILY, 12),
                bg=ui_config.BACKGROUND_COLOR,
                fg=ui_config.PRIMARY_COLOR,
                anchor="w",
            )
            no_songs_label.pack(fill="x", pady=2)
            return

        # Frame to hold all song buttons
        playlist_inner = d3.Frame(
            self.scrollable_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=5,
            pady=5,
            highlightthickness=0,
        )
        playlist_inner.pack(fill="both", expand=True)

        # Create song buttons
        for i, song_name in enumerate(self.playlist.playlist_display_names):
            song_btn = d3.Button(
                playlist_inner,
                text=song_name,
                font=(ui_config.FONT_FAMILY, 12),
                command=lambda x=i: self.select_song(x),
                bg=ui_config.BACKGROUND_COLOR,
                fg=ui_config.PRIMARY_COLOR,
                activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
                activeforeground=ui_config.PRIMARY_COLOR,
                anchor="w",
                relief="flat",
                wraplength=300,
                justify="left",
                padx=5,
                pady=2,
            )
            song_btn.pack(fill="x", pady=2)

    def _show_create_playlist_dialog(self):
        """Show dialog to create a new playlist"""
        if self.dialog_active:
            return

        ui_config = config["ui"]
        self.dialog_active = True

        # Create the dialog frame
        self.dialog_frame = d3.Frame(
            self.page.page_frame,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=1,
            highlightbackground=ui_config.PRIMARY_COLOR,
        )
        self.dialog_frame.place(
            relx=0.5, rely=0.5, anchor="center", width=300, height=150
        )

        # Dialog header
        header = d3.Label(
            self.dialog_frame,
            text="Create New Playlist",
            font=(ui_config.FONT_FAMILY, 12, "bold"),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
        )
        header.pack(pady=(10, 5))

        # Dialog content
        content_frame = d3.Frame(
            self.dialog_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        content_frame.pack(fill="both", expand=True)

        d3.Label(
            content_frame,
            text="Playlist Name:",
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            anchor="w",
        ).pack(anchor="w")

        name_entry = d3.Entry(content_frame, width=30)
        name_entry.pack(fill="x", pady=5)
        name_entry.focus_set()

        # Buttons frame
        btn_frame = d3.Frame(
            self.dialog_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        btn_frame.pack(fill="x")

        def cancel_dialog():
            self.dialog_frame.destroy()
            self.dialog_frame = None
            self.dialog_active = False

        def create_playlist():
            playlist_name = name_entry.get().strip()
            if playlist_name:
                if self.playlist.create_playlist(playlist_name):
                    self._update_playlist_selector()
                    # Select the new playlist
                    self.playlist_selector_var.set(playlist_name)
                    self._on_playlist_selected(playlist_name)
                    cancel_dialog()
                    self._show_notification(
                        f"Playlist '{playlist_name}' created",
                        notification_type="success",
                    )
                else:
                    # Show error that playlist already exists
                    self._show_notification(
                        f"Playlist '{playlist_name}' already exists",
                        notification_type="error",
                    )
            else:
                self._show_notification(
                    "Please enter a playlist name", notification_type="error"
                )

        d3.Button(
            btn_frame,
            text="Cancel",
            command=cancel_dialog,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        ).pack(side="right", padx=5)

        d3.Button(
            btn_frame,
            text="Create",
            command=create_playlist,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        ).pack(side="right")

        # Bind Enter key to create playlist
        name_entry.bind("<Return>", lambda event: create_playlist())

    def _confirm_delete_playlist(self):
        """Show confirmation dialog before deleting a playlist"""
        current_playlist = self.playlist_selector_var.get()

        # Don't allow deleting "All Songs"
        if current_playlist == "All Songs":
            self._show_notification(
                "Cannot delete the 'All Songs' playlist", notification_type="info"
            )
            return

        if self.dialog_active:
            return

        ui_config = config["ui"]
        self.dialog_active = True

        # Create the dialog frame
        self.dialog_frame = d3.Frame(
            self.page.page_frame,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=1,
            highlightbackground=ui_config.PRIMARY_COLOR,
        )
        self.dialog_frame.place(
            relx=0.5, rely=0.5, anchor="center", width=300, height=150
        )

        # Dialog header
        header = d3.Label(
            self.dialog_frame,
            text="Confirm Delete",
            font=(ui_config.FONT_FAMILY, 12, "bold"),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
        )
        header.pack(pady=(10, 5))

        # Dialog content
        content_frame = d3.Frame(
            self.dialog_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        content_frame.pack(fill="both", expand=True)

        d3.Label(
            content_frame,
            text=f"Delete playlist '{current_playlist}'?",
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            wraplength=250,
        ).pack(pady=10)

        # Buttons frame
        btn_frame = d3.Frame(
            self.dialog_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        btn_frame.pack(fill="x")

        def cancel_dialog():
            self.dialog_frame.destroy()
            self.dialog_frame = None
            self.dialog_active = False

        def delete_playlist():
            playlist_names = self.playlist.get_playlist_display_names()
            if current_playlist in playlist_names:
                index = playlist_names.index(current_playlist)
                if self.playlist.delete_playlist(index):
                    # Update selector and switch to "All Songs"
                    self._update_playlist_selector()
                    self.playlist_selector_var.set("All Songs")
                    self._on_playlist_selected("All Songs")
                    cancel_dialog()
                    self._show_notification(
                        f"Playlist '{current_playlist}' deleted",
                        notification_type="success",
                    )

        d3.Button(
            btn_frame,
            text="No",
            command=cancel_dialog,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        ).pack(side="right", padx=5)

        d3.Button(
            btn_frame,
            text="Yes",
            command=delete_playlist,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        ).pack(side="right")

    def _show_add_song_dialog(self):
        """Show dialog to add songs to the current playlist"""
        # Don't allow adding songs to "All Songs" playlist
        if self.playlist_selector_var.get() == "All Songs":
            self._show_notification(
                "Cannot add songs to 'All Songs' playlist.\nCreate a new playlist first.",
                notification_type="info",
            )
            return

        if self.dialog_active:
            return

        ui_config = config["ui"]
        self.dialog_active = True

        # Create the dialog frame
        self.dialog_frame = d3.Frame(
            self.page.page_frame,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=1,
            highlightbackground=ui_config.PRIMARY_COLOR,
        )
        self.dialog_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=config["window"].FRAME_WIDTH,
            height=config["window"].FRAME_HEIGHT,
        )

        # Dialog header
        header = d3.Label(
            self.dialog_frame,
            text=f"Add Songs to {self.playlist_selector_var.get()}",
            font=(ui_config.FONT_FAMILY, 12, "bold"),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
        )
        header.pack(pady=(10, 5))

        # Dialog content
        content_frame = d3.Frame(
            self.dialog_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        content_frame.pack(fill="both", expand=True)

        d3.Label(
            content_frame,
            text="Available Songs:",
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            anchor="w",
        ).pack(anchor="w")

        # Create listbox with scrollbar
        list_frame = d3.Frame(content_frame, bg=ui_config.BACKGROUND_COLOR)
        list_frame.pack(side="left")

        scrollbar = d3.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        song_listbox = d3.Listbox(
            list_frame,
            selectmode="extended",
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            yscrollcommand=scrollbar.set,
        )
        song_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=song_listbox.yview)

        # Populate the listbox with available songs
        for idx, song_name in enumerate(self.playlist.available_song_names):
            song_path = self.playlist.available_songs[idx]
            # For custom playlists, store only the filename, not the full path
            song_path = os.path.basename(song_path)
            if (
                song_path
                not in self.playlist.playlists[
                    self.playlist.current_playlist_index
                ].song_paths
            ):
                song_listbox.insert("end", song_name)

        # Buttons frame
        btn_frame = d3.Frame(
            content_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        btn_frame.pack(side="right")

        def cancel_dialog():
            self.dialog_frame.destroy()
            self.dialog_frame = None
            self.dialog_active = False

        def add_selected_songs():
            selected_indices = song_listbox.curselection()
            if not selected_indices:
                self._show_notification("No songs selected", notification_type="error")
                return

            songs_added = 0
            for i in selected_indices:
                if self.playlist.add_song_to_current_playlist(
                    self.playlist.available_song_names.index(song_listbox.get(i))
                ):
                    songs_added += 1

            if songs_added > 0:
                self.playlist.save_playlists()
                self._create_playlist_items()
                cancel_dialog()
                self._show_notification(
                    f"Added {songs_added} song(s) to playlist",
                    notification_type="success",
                )
            else:
                cancel_dialog()
                self._show_notification(
                    "No new songs were added to the playlist", notification_type="info"
                )

        d3.Button(
            btn_frame,
            text="Cancel",
            command=cancel_dialog,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        ).pack()

        d3.Button(
            btn_frame,
            text="Add Selected",
            command=add_selected_songs,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=12,
        ).pack()

    def _confirm_remove_song(self):
        """Show confirmation dialog before removing a song"""
        # Don't allow removing songs from "All Songs" playlist
        if self.playlist_selector_var.get() == "All Songs":
            self._show_notification(
                "Cannot remove songs from 'All Songs' playlist",
                notification_type="info",
            )
            return

        # Check if a song is currently selected
        if self.state.current_song_index is None or not self.playlist.has_songs():
            self._show_notification("No song selected", notification_type="info")
            return

        # Get current song name
        song_name = self.playlist.get_current_song_name(self.state.current_song_index)

        if self.dialog_active:
            return

        ui_config = config["ui"]
        self.dialog_active = True

        # Create the dialog frame
        self.dialog_frame = d3.Frame(
            self.page.page_frame,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=1,
            highlightbackground=ui_config.PRIMARY_COLOR,
        )
        self.dialog_frame.place(
            relx=0.5, rely=0.5, anchor="center", width=300, height=150
        )

        # Dialog header
        header = d3.Label(
            self.dialog_frame,
            text="Confirm Remove",
            font=(ui_config.FONT_FAMILY, 12, "bold"),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
        )
        header.pack(pady=(10, 5))

        # Dialog content
        content_frame = d3.Frame(
            self.dialog_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        content_frame.pack(fill="both", expand=True)

        d3.Label(
            content_frame,
            text=f"Remove '{song_name}' from playlist?",
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            wraplength=250,
        ).pack(pady=10)

        # Buttons frame
        btn_frame = d3.Frame(
            self.dialog_frame,
            bg=ui_config.BACKGROUND_COLOR,
            padx=20,
            pady=10,
        )
        btn_frame.pack(fill="x")

        def cancel_dialog():
            self.dialog_frame.destroy()
            self.dialog_frame = None
            self.dialog_active = False

        def remove_song():
            # Stop playback if this song is playing
            was_playing = self.state.is_playing
            if was_playing:
                pygame.mixer.music.stop()
                self.state.is_playing = False
                self.state.song_paused = False

            # Remove the song
            if self.playlist.remove_song_from_current_playlist(
                self.state.current_song_index
            ):
                # Reset state if no songs left
                if not self.playlist.has_songs():
                    self.state.current_song_index = 0
                    self.state.current_song_length = 0
                    self.reset_state()
                # Handle index if we removed the last song
                elif self.state.current_song_index >= len(self.playlist.playlist_files):
                    self.state.current_song_index = (
                        len(self.playlist.playlist_files) - 1
                    )

                # Update UI
                self._create_playlist_items()
                self._update_song_display()

                # Resume playback if needed
                if was_playing and self.playlist.has_songs():
                    self._start_current_song()
                    self._update_playing_state_ui()

                cancel_dialog()
                self._show_notification(
                    f"Removed '{song_name}' from playlist", notification_type="success"
                )

        d3.Button(
            btn_frame,
            text="No",
            command=cancel_dialog,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        ).pack(side="right", padx=5)

        d3.Button(
            btn_frame,
            text="Yes",
            command=remove_song,
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
            activeforeground=ui_config.PRIMARY_COLOR,
            width=8,
        ).pack(side="right")

    def _remove_current_song(self):
        """Remove the currently selected song from the playlist - replaced by confirmation dialog"""
        self._confirm_remove_song()

    def _delete_current_playlist(self):
        """Delete the currently selected playlist - replaced by confirmation dialog"""
        self._confirm_delete_playlist()


def create(page, root):
    global _music_player_instance
    if not _music_player_instance:
        _music_player_instance = MusicPlayer()
    _music_player_instance.page = page
    _music_player_instance.root = root
    _music_player_instance.create_widgets(page)


def destroy(page, root):
    """Clean up the music player instance"""
    global _music_player_instance
    if _music_player_instance:
        # Clean up scroll bindings first
        _music_player_instance._unbind_scroll_events()

        # Stop timers
        _music_player_instance._stop_song_end_checker()
        _music_player_instance._stop_progress_updates()

        # Cancel any notification timer
        if _music_player_instance.notification_timer:
            _music_player_instance.root.after_cancel(
                _music_player_instance.notification_timer
            )
            _music_player_instance.notification_timer = None

        # Stop audio if needed
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        # Close any open dialogs
        if (
            _music_player_instance.dialog_frame
            and _music_player_instance.dialog_frame.winfo_exists()
        ):
            _music_player_instance.dialog_frame.destroy()

        # Destroy UI
        page.page_frame.destroy()


def is_running():
    """Check if the music player is currently playing music.

    Returns:
        bool: True if music is playing, False otherwise
    """
    global _music_player_instance
    if _music_player_instance:
        return _music_player_instance.state.is_playing
    return False
