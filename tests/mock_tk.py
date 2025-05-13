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

class Button:
    def __init__(self, master=None, **kwargs):
        self.master = master
        self.kwargs = kwargs
        self.configure = lambda *args, **kwargs: None
        self.place = lambda *args, **kwargs: None
    
    def config(self, *args, **kwargs):
        pass
