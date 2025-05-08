import tkinter as d3


class MusicPlayer:
    def __init__(self):
        self.pause_play = None
        self.state = False
        self.font_default = ("Alien Encounters", 60, "bold")

    def play(self):
        if self.state:
            self.pause_play.configure(text="\u23f5")
        else:
            self.pause_play.configure(text="\u23f8")
        self.state = not self.state

    def create_widgets(self, page):
        self.page = page
        self.page.page_frame.configure(bg="black")
        global pause_play
        self.pause_play = d3.Button(
            self.page.page_frame,
            text="\u23f5",
            font=self.font_default,
            command=self.play,
        )
        self.pause_play.place(
            relx=0.5, rely=0.8, relheight=0.2, relwidth=0.2, anchor="center"
        )

    def destroy_app(self, page):
        page.page_frame.destroy()


_music_player_instance = None


def create(page, root):
    global _music_player_instance
    _music_player_instance = MusicPlayer()
    _music_player_instance.root = root
    _music_player_instance.create_widgets(page)


def destroy(page, root):
    global _music_player_instance
    if _music_player_instance:
        _music_player_instance.destroy_app(page)
        _music_player_instance = None
