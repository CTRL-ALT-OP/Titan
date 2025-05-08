from tkinter import *


class Timer:
    def __init__(self, root):
        self.root = root
        self.root.wm_attributes("-topmost", "1")

        self.canvas = Canvas(self.root, width=100, height=100)
        self.canvas.pack()

        self.time = 3600

        self.timer_str = Label(self.root, text=str(self.time), font=("Helvetica", 20))
        self.timer_str.pack()

        self.start_timer()

    def start_timer(self):
        self.timer()

    def timer(self):
        self.time -= 1
        self.timer_str.configure(text=str(self.time))
        self.root.after(1000, self.timer)


if __name__ == "__main__":
    root = Tk()
    app = Timer(root)
    root.mainloop()
