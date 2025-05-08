import de333r as titan
import apper


class TitanApp:
    def __init__(self):
        self.list_apps = apper.list()
        self.current_page = 0
        self.loaded_page = None
        self.loaded_app = None
        self.root = None
        self.bg_root = None
        self.switch_l = None
        self.switch_r = None

    def switch(self, direction):
        if ((self.current_page != len(self.list_apps) - 1) and (direction == 1)) or (
            (self.current_page != 0) and (direction == -1)
        ):
            self.switch_l.configure(state="disabled")
            self.switch_r.configure(state="disabled")
            next_page = titan.page(self.bg_root, self.root)
            app = self.list_apps[self.current_page + direction]
            next_app = apper.app(next_page, app, self.root)

            self.loaded_page.tween(next_page, 300, direction=direction)

            def check_tween_complete(next_app, next_page):
                if self.loaded_page.finished == True:
                    self.current_page += direction
                    self.loaded_app.app.destroy(self.loaded_page, self.root)
                    self.loaded_page = next_page
                    self.loaded_app = next_app
                    self.switch_l.configure(state="normal")
                    self.switch_r.configure(state="normal")
                else:
                    self.root.after(
                        20, lambda: check_tween_complete(next_app, next_page)
                    )

            self.root.after(20, lambda: check_tween_complete(next_app, next_page))

        elif (self.current_page == len(self.list_apps) - 1) and (direction == 1):
            self.switch_l.configure(state="disabled")
            self.switch_r.configure(state="disabled")
            next_page = titan.page(self.bg_root, self.root)
            app = self.list_apps[0]
            next_app = apper.app(next_page, app, self.root)

            self.loaded_page.tween(next_page, 300, direction=direction)

            def check_tween_complete(next_app, next_page):
                if self.loaded_page.finished == True:
                    self.current_page = 0
                    self.loaded_app.app.destroy(self.loaded_page, self.root)
                    self.loaded_page = next_page
                    self.loaded_app = next_app
                    self.switch_l.configure(state="normal")
                    self.switch_r.configure(state="normal")
                else:
                    self.root.after(
                        20, lambda: check_tween_complete(next_app, next_page)
                    )

            self.root.after(20, lambda: check_tween_complete(next_app, next_page))

        elif (self.current_page == 0) and (direction == -1):
            self.switch_l.configure(state="disabled")
            self.switch_r.configure(state="disabled")
            next_page = titan.page(self.bg_root, self.root)
            app = self.list_apps[len(self.list_apps) - 1]
            next_app = apper.app(next_page, app, self.root)

            self.loaded_page.tween(next_page, 300, direction=direction)

            def check_tween_complete(next_app, next_page):
                if self.loaded_page.finished == True:
                    self.current_page = len(self.list_apps) - 1
                    self.loaded_app.app.destroy(self.loaded_page, self.root)
                    self.loaded_page = next_page
                    self.loaded_app = next_app
                    self.switch_l.configure(state="normal")
                    self.switch_r.configure(state="normal")
                else:
                    self.root.after(
                        20, lambda: check_tween_complete(next_app, next_page)
                    )

            self.root.after(20, lambda: check_tween_complete(next_app, next_page))

    def run(self):
        self.root, self.bg_root, self.switch_l, self.switch_r = titan.main.create()

        self.switch_l.configure(command=lambda: self.switch(-1))
        self.switch_r.configure(command=lambda: self.switch(1))

        self.loaded_page = titan.page(self.bg_root, self.root)
        self.loaded_app = apper.app(self.loaded_page, self.list_apps[0], self.root)

        self.loaded_page.page_frame.pack()

        self.root.mainloop()


if __name__ == "__main__":
    app = TitanApp()
    app.run()
