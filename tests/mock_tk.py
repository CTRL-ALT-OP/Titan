"""Mock Tkinter module for testing."""


class Tk:
    def __init__(self):
        self.resizable = lambda *args, **kwargs: None
        self.mainloop = lambda: None
        self.update = lambda: None
        self.after = lambda *args, **kwargs: None

    def destroy(self):
        pass


class Frame:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.pack = lambda *args, **kwargs: None
        self.pack_forget = lambda *args, **kwargs: None
        self.configure = lambda *args, **kwargs: None
        self.place = lambda *args, **kwargs: None
        self.place_forget = lambda: None
        self.destroy = lambda: None

    def config(self, *args, **kwargs):
        pass


class Label:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.place = lambda *args, **kwargs: None
        self.pack = lambda *args, **kwargs: None
        self.grid = lambda *args, **kwargs: None
        self.configure = lambda *args, **kwargs: None


class Button:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.configure = lambda *args, **kwargs: None
        self.place = lambda *args, **kwargs: None
        self.pack = lambda *args, **kwargs: None

    def config(self, *args, **kwargs):
        pass


class Scale:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.place = lambda *args, **kwargs: None
        self.set = lambda value: None
        self.get = lambda: 0
        self.bind = lambda *args, **kwargs: None


class Canvas:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.pack = lambda *args, **kwargs: None
        self.configure = lambda *args, **kwargs: None
        self.yview = lambda *args: None
        self.bind_all = lambda *args, **kwargs: None
        self.unbind_all = lambda *args, **kwargs: None
        self.create_window = lambda *args, **kwargs: None
        self.bbox = lambda *args: (0, 0, 100, 100)


class Scrollbar:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.pack = lambda *args, **kwargs: None
        self.set = lambda *args: None


class StringVar:
    def __init__(self):
        self._value = ""

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class OptionMenu:
    def __init__(self, master, variable, default, *values, **kwargs):
        self.master = master
        self.variable = variable
        self.values = values
        self.config = lambda *args, **kwargs: None
        self.pack = lambda *args, **kwargs: None


class Entry:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.pack = lambda *args, **kwargs: None
        self.focus_set = lambda: None
        self.get = lambda: ""
        self.bind = lambda *args, **kwargs: None


class Listbox:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.pack = lambda *args, **kwargs: None
        self.insert = lambda *args, **kwargs: None
        self.curselection = lambda: []
        self.get = lambda idx: f"song{idx}"


# Mock for tkinter's _setit function (used in OptionMenu)
def _setit(var, value, callback=None):
    def _internal(*args):
        var.set(value)
        if callback:
            callback(value)

    return _internal


# Mock messagebox module
class messagebox:
    @staticmethod
    def showinfo(title, message):
        return None

    @staticmethod
    def showwarning(title, message):
        return None

    @staticmethod
    def showerror(title, message):
        return None

    @staticmethod
    def askyesno(title, message):
        return True

    @staticmethod
    def askokcancel(title, message):
        return True
