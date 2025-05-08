import tkinter as d3
from config import config


class FiveInRow:
    def __init__(self):
        self.turn = "r"
        self.ui_config = config["ui"]
        self.window_config = config["window"]

    def create_board(self, _width):
        self.width = _width
        a = 0
        b = 0
        self.grid = []

        self.grid_pieces = []

        while a < self.width:
            row = []
            row_pieces = []
            while b < self.width:
                label = d3.Button(
                    self.page.page_frame,
                    bg=self.ui_config.BACKGROUND_COLOR,
                    activebackground=self.ui_config.ACTIVE_BACKGROUND_COLOR,
                    text="  ",
                    command=lambda _row=a, _column=b: self.object_pressed(
                        _row, _column
                    ),
                    font=(self.ui_config.FONT_FAMILY, 20, "bold"),
                )
                label.place(
                    x=b * (self.window_config.FRAME_WIDTH / self.width),
                    y=a * (self.window_config.FRAME_HEIGHT / self.width),
                    height=self.window_config.FRAME_HEIGHT / self.width,
                    width=self.window_config.FRAME_WIDTH / self.width,
                )
                row.append(label)
                row_pieces.append("")
                b += 1
            b = 0
            self.grid.append(row)
            self.grid_pieces.append(row_pieces)
            a += 1
        return (self.grid, self.grid_pieces)

    def object_pressed(self, _row, _column):
        if self.turn == "r":
            if self.grid_pieces[_row][_column] not in ["R", "B"]:
                self.turn = "b"
                self.grid[_row][_column].configure(
                    text="X", fg=self.ui_config.SECONDARY_COLOR
                )
                self.grid_pieces[_row][_column] = "R"
                # print(grid_pieces)
                win_r = self.verify_board("R")
                if win_r:
                    print("Red won the game!")
                    btn = d3.Label(
                        self.page.page_frame,
                        text="Red won!\nDo you want to play again?",
                        fg=self.ui_config.PRIMARY_COLOR,
                        font=(self.ui_config.FONT_FAMILY, 14, "bold"),
                        relief="groove",
                        bg=self.ui_config.BACKGROUND_COLOR,
                    )
                    btn.place(relx=0.5, rely=0.5, anchor="center")

                    def do(btn, btn_2):
                        btn.destroy()
                        btn_2.destroy()
                        for row in self.grid:
                            for piece in row:
                                piece.destroy()
                        self.grid = []
                        self.grid, self.grid_pieces = self.create_board(self.width)

                    btn_2 = d3.Button(
                        self.page.page_frame,
                        text="Yes",
                        font=(self.ui_config.FONT_FAMILY, 30, "bold"),
                        fg=self.ui_config.PRIMARY_COLOR,
                        relief="groove",
                        bg=self.ui_config.BACKGROUND_COLOR,
                        activebackground=self.ui_config.ACTIVE_BACKGROUND_COLOR,
                    )
                    btn_2.configure(command=lambda bt1=btn, bt2=btn_2: do(bt1, bt2))
                    btn_2.place(relx=0.5, rely=0.65, anchor="center")

        elif self.turn == "b":
            if self.grid_pieces[_row][_column] not in ["R", "B"]:
                self.turn = "r"
                self.grid[_row][_column].configure(text="O", fg="blue")
                self.grid_pieces[_row][_column] = "B"
                # print(grid_pieces)
                win_r = self.verify_board("B")
                if win_r:
                    print("Blue won the game!")
                    btn = d3.Label(
                        self.page.page_frame,
                        text="Blue won!\nDo you want to play again?",
                        fg=self.ui_config.PRIMARY_COLOR,
                        font=(self.ui_config.FONT_FAMILY, 14, "bold"),
                        relief="groove",
                        bg=self.ui_config.BACKGROUND_COLOR,
                    )
                    btn.place(relx=0.5, rely=0.5, anchor="center")

                    def do(btn, btn_2):
                        btn.destroy()
                        btn_2.destroy()
                        for row in self.grid:
                            for piece in row:
                                piece.destroy()
                        self.grid = []
                        self.grid, self.grid_pieces = self.create_board(self.width)

                    btn_2 = d3.Button(
                        self.page.page_frame,
                        text="Yes",
                        font=(self.ui_config.FONT_FAMILY, 30, "bold"),
                        fg=self.ui_config.PRIMARY_COLOR,
                        relief="groove",
                        bg=self.ui_config.BACKGROUND_COLOR,
                        activebackground=self.ui_config.ACTIVE_BACKGROUND_COLOR,
                    )
                    btn_2.configure(command=lambda bt1=btn, bt2=btn_2: do(bt1, bt2))
                    btn_2.place(relx=0.5, rely=0.65, anchor="center")

    def verify_board(self, player):
        row_num = 0
        column_num = 0
        for rowe in self.grid_pieces:
            for piece in rowe:
                current_coords = [row_num, column_num]
                if self.grid_pieces[row_num][column_num] == player:
                    # check entire radius
                    # check left
                    def check_line(row_change, column_change):
                        # Check for 5 consecutive pieces in a line
                        for i in range(1, 5):
                            # Check if we're still within the grid bounds
                            if (
                                0 <= row_num + (i * row_change) < self.width
                                and 0 <= column_num + (i * column_change) < self.width
                            ):
                                if (
                                    self.grid_pieces[row_num + (i * row_change)][
                                        column_num + (i * column_change)
                                    ]
                                    != player
                                ):
                                    return False
                            else:
                                return False
                        print(f"line found starting at {current_coords}")
                        return True

                    win = False

                    # Check horizontal, vertical, and diagonal lines
                    if column_num <= self.width - 5:
                        win = check_line(0, 1)  # right
                    if not win and row_num <= self.width - 5:
                        win = check_line(1, 0)  # down
                    if not win and column_num >= 4:
                        win = check_line(0, -1)  # left
                    if not win and row_num >= 4:
                        win = check_line(-1, 0)  # up
                    if (
                        not win
                        and column_num <= self.width - 5
                        and row_num <= self.width - 5
                    ):
                        win = check_line(1, 1)  # down-right
                    if not win and column_num >= 4 and row_num <= self.width - 5:
                        win = check_line(1, -1)  # down-left
                    if not win and column_num <= self.width - 5 and row_num >= 4:
                        win = check_line(-1, 1)  # up-right
                    if not win and column_num >= 4 and row_num >= 4:
                        win = check_line(-1, -1)  # up-left

                    if win:
                        return True

                column_num += 1
            column_num = 0
            row_num += 1
        return False

    def create_widgets(self, page):
        self.page = page
        self.width = 10

        self.grid, self.grid_pieces = self.create_board(self.width)

    def destroy_app(self, page):
        page.page_frame.destroy()


_five_in_row_instance = None


def create(_page, root):
    global _five_in_row_instance
    _five_in_row_instance = FiveInRow()
    _five_in_row_instance.root = root
    _five_in_row_instance.create_widgets(_page)


def destroy(page, root):
    global _five_in_row_instance
    if _five_in_row_instance:
        _five_in_row_instance.destroy_app(page)
        _five_in_row_instance = None
