import tkinter as d3


def create(page, root):
    lbl = d3.Label(page.page_frame, text="test_2")
    page.page_frame.configure(bg="red")
    lbl.place(relx=0.5, rely=0.5)


def destroy(page, root):
    page.page_frame.destroy()
