import tkinter as d3
from config import config


class Calculator:
    def __init__(self):
        self.entry = None
        self.current_input = "0"
        self.result = 0
        self.operation = None
        self.first_num = None
        self.page = None
        self.root = None

    def create_widgets(self, page):
        self.page = page
        ui_config = config["ui"]
        self.page.page_frame.configure(bg=ui_config.BACKGROUND_COLOR)

        # Display
        self.entry = d3.Entry(
            self.page.page_frame,
            font=(ui_config.FONT_FAMILY, 20),
            bg=ui_config.BACKGROUND_COLOR,
            fg=ui_config.PRIMARY_COLOR,
            justify="right",
            bd=0,
        )
        self.entry.place(
            relx=0.5, rely=0.1, relwidth=0.9, relheight=0.15, anchor="center"
        )
        self.entry.insert(0, "0")

        # Buttons frame
        btn_frame = d3.Frame(self.page.page_frame, bg=ui_config.BACKGROUND_COLOR)
        btn_frame.place(
            relx=0.5, rely=0.55, relwidth=0.9, relheight=0.75, anchor="center"
        )

        # Button layout
        buttons = [
            "7",
            "8",
            "9",
            "/",
            "4",
            "5",
            "6",
            "*",
            "1",
            "2",
            "3",
            "-",
            "0",
            ".",
            "=",
            "+",
            "C",
        ]

        # Create buttons
        self._create_buttons(btn_frame, buttons, ui_config)

        # Configure grid weights
        for i in range(5):
            btn_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)

    def _create_buttons(self, btn_frame, buttons, ui_config):
        row, col = 0, 0
        for btn_text in buttons:
            is_operator = btn_text in ["+", "-", "*", "/", "=", "C"]
            btn = d3.Button(
                btn_frame,
                text=btn_text,
                font=(ui_config.FONT_FAMILY, 16),
                bg=ui_config.BACKGROUND_COLOR,
                fg=(
                    ui_config.SECONDARY_COLOR
                    if is_operator
                    else ui_config.PRIMARY_COLOR
                ),
                activebackground=ui_config.ACTIVE_BACKGROUND_COLOR,
                activeforeground=ui_config.PRIMARY_COLOR,
                bd=1,
                command=lambda x=btn_text: self.click(x),
            )

            if btn_text == "C":
                btn.grid(
                    row=row, column=col, columnspan=4, sticky="nsew", padx=1, pady=1
                )
                row += 1
            else:
                btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                col += 1
                if col > 3:
                    col = 0
                    row += 1

    def click(self, char):
        if char == "=":
            self._calculate_result()
        elif char == "C":
            self._reset_calculator()
        elif char in ["+", "-", "*", "/"]:
            self._process_operation(char)
        else:
            self._add_digit(char)

    def _calculate_result(self):
        if self.operation and self.first_num is not None and self.current_input:
            self.perform_operation()
            self.current_input = "0"
            self.first_num = None
            self.operation = None

    def _reset_calculator(self):
        self.first_num = None
        self.operation = None
        self.current_input = "0"
        self._update_display("0")

    def _process_operation(self, operator):
        if not self.current_input:
            return

        if self.first_num is None:
            self.first_num = float(self.current_input)
            self.operation = operator
            self.current_input = "0"
        elif self.operation:
            self.perform_operation()
            self.first_num = self.result
            self.operation = operator
            self.current_input = "0"

    def _add_digit(self, char):
        if char == "." and "." in self.current_input:
            return
        if self.current_input == "0" and char != ".":
            self.current_input = char
        else:
            self.current_input += char
        self._update_display(self.current_input)

    def _update_display(self, value):
        self.entry.delete(0, "end")
        self.entry.insert("end", value or "0")

    def perform_operation(self):
        try:
            num2 = float(self.current_input)
            operations = {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y if y != 0 else "Error: Div by 0",
            }

            self.result = operations[self.operation](self.first_num, num2)

            # Format result to remove trailing zeros for whole numbers
            if isinstance(self.result, float) and self.result.is_integer():
                self._update_display(str(int(self.result)))
            else:
                self._update_display(str(self.result))

        except (ValueError, KeyError):
            self._update_display("Error")

    def destroy_app(self, page):
        page.page_frame.destroy()


# Singleton calculator instance
_calculator_instance = None


def get_instance():
    global _calculator_instance
    if not _calculator_instance:
        _calculator_instance = Calculator()
    return _calculator_instance


def create(page, root):
    calculator = get_instance()
    calculator.root = root
    calculator.create_widgets(page)


def destroy(page, root):
    global _calculator_instance
    if _calculator_instance:
        _calculator_instance.destroy_app(page)
        _calculator_instance = None
