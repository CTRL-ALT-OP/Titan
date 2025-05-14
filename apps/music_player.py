import tkinter as d3
import os
import pygame
import time
from config import config

# Define constants
SONG_END_CHECK_INTERVAL_MS = 1000
PROGRESS_UPDATE_INTERVAL_MS = 250
TIME_DISPLAY_FORMAT = "{current_min}:{current_sec:02d} / {total_min}:{total_sec:02d}"


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


class PlaylistManager:
    """Class to manage playlist operations"""

    def __init__(self, songs_folder="apps/_music_player/songs"):
        self.songs_folder = songs_folder
        self.playlist_files = []
        self.playlist_display_names = []
        self.songs_loaded = False

    def load_songs(self):
        """Load songs from the songs folder"""
        self.playlist_files = []
        self.playlist_display_names = []

        if not os.path.isdir(self.songs_folder):
            print(f"Songs folder not found: {self.songs_folder}")
            self.playlist_display_names = ["No songs found"]
            self.songs_loaded = True
            return

        for filename in os.listdir(self.songs_folder):
            if filename.endswith((".mp3", ".wav")):
                full_path = os.path.join(self.songs_folder, filename)
                self.playlist_files.append(full_path)
                self.playlist_display_names.append(os.path.splitext(filename)[0])

        if not self.playlist_files:
            self.playlist_display_names = ["No songs found"]

        self.songs_loaded = True

    def get_current_song_path(self, index):
        if not self.playlist_files or index >= len(self.playlist_files):
            return None
        return self.playlist_files[index]

    def get_current_song_name(self, index):
        if not self.playlist_display_names or index >= len(self.playlist_display_names):
            return "No song selected"
        return self.playlist_display_names[index]

    def has_songs(self):
        return bool(self.playlist_files)


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
        self.prev_btn.place(relx=0.35, rely=0.9, anchor="center")

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
        self.pause_play.place(relx=0.5, rely=0.9, anchor="center")

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
        self.next_btn.place(relx=0.65, rely=0.9, anchor="center")

    def _create_playlist_container(self, ui_config):
        """Create the scrollable playlist container"""
        self.playlist_container = d3.Frame(
            self.page.page_frame,
            bg=ui_config.BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.playlist_container.place(
            relx=0.1, rely=0.1, relwidth=0.8, relheight=0.55, anchor="nw"
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
                text="No songs found in apps/_music_player/songs",
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

    def destroy_app(self, page):
        """Clean up resources when app is destroyed"""
        # Clean up scroll bindings first
        self._unbind_scroll_events()

        # Stop timers
        self._stop_song_end_checker()
        self._stop_progress_updates()

        # Stop audio if needed
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        # Destroy UI
        page.page_frame.destroy()


# Module-level instance
_music_player_instance = None


def create(page, root):
    """Create or reuse the music player instance"""
    global _music_player_instance
    if _music_player_instance is None:
        _music_player_instance = MusicPlayer()

    _music_player_instance.root = root
    _music_player_instance.page = page
    _music_player_instance.create_widgets(page)


def destroy(page, root):
    """Clean up the music player instance"""
    global _music_player_instance
    if _music_player_instance:
        # Clean up scroll bindings to prevent event issues
        _music_player_instance._unbind_scroll_events()

        # Keep song end checker active if music is playing
        keep_song_checker_active = (
            _music_player_instance.state.is_playing
            and pygame.mixer.get_init()
            and pygame.mixer.music.get_busy()
        )

        # Destroy the main page frame
        if hasattr(_music_player_instance, "page") and hasattr(
            _music_player_instance.page, "page_frame"
        ):
            _music_player_instance.page.page_frame.destroy()

        # Reset critical attributes
        _music_player_instance.ui_built = False
        _music_player_instance.page = None

        # Clear UI widget references and ensure unbind_all is called before nulling the canvas
        if hasattr(_music_player_instance, "canvas") and _music_player_instance.canvas:
            try:
                _music_player_instance.canvas.unbind_all("<MouseWheel>")
                _music_player_instance.canvas.unbind_all("<Button-4>")
                _music_player_instance.canvas.unbind_all("<Button-5>")
            except Exception:
                pass

        # Clear UI widget references
        _music_player_instance.song_label = None
        _music_player_instance.prev_btn = None
        _music_player_instance.pause_play = None
        _music_player_instance.next_btn = None
        _music_player_instance.playlist_container = None
        _music_player_instance.canvas = None
        _music_player_instance.scrollbar = None
        _music_player_instance.scrollable_frame = None
        _music_player_instance.loading_label_main_ui = None

        # Stop progress updates
        if _music_player_instance.progress_update_id and root:
            root.after_cancel(_music_player_instance.progress_update_id)
        _music_player_instance.progress_update_id = None
        _music_player_instance.progress_slider = None
        _music_player_instance.state.is_seeking = False

        # Handle song end checker
        if keep_song_checker_active:
            if _music_player_instance.song_end_check_id:
                root.after_cancel(_music_player_instance.song_end_check_id)
            # Restart in background mode
            _music_player_instance.song_end_check_id = root.after(
                SONG_END_CHECK_INTERVAL_MS,
                lambda: _music_player_instance._check_song_finished(
                    is_background_mode=True
                ),
            )
        else:
            if _music_player_instance.song_end_check_id and root:
                root.after_cancel(_music_player_instance.song_end_check_id)
            _music_player_instance.song_end_check_id = None
