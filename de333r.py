import tkinter as d3 #replace tkinter with de333r
global pages

class main():
    def create():
        root = d3.Tk()
        root.resizable(False,False)
        fg_root = d3.Frame(root, width = 350, height = 300)
        fg_root.pack()
        bg_root = d3.Frame(root, width = 300, height = 300)
        bg_root.place(x=25,y=0)
        
        switch_btn_l = d3.Button(root,text = "<") 
        switch_btn_l.place(x=0,y=0,width = 25,relheight = 1)

        switch_btn_r = d3.Button(root,text = ">") 
        switch_btn_r.place(relx=1,y=0,width = 25,relheight = 1, anchor = "ne")
        return root, bg_root, switch_btn_l, switch_btn_r

class page():
    def create(self):
        self.page_frame = d3.Frame(self.root, width = 300, height = 300)
    def tween(self, frame_2, bounding_x, time = 50, direction = 1):
        self.finished = False
        frame_2.page_frame.place(x=0+(direction*bounding_x),y=0)
        def looper(self):
            self.curr_x -= 15
            frame_2.page_frame.place(x=direction*self.curr_x,y=0)
            self.page_frame.place(x=direction*(self.curr_x-self.bounding_x),y=0)
            if self.curr_x > 0:
                self.true_root.update()
                self.true_root.after(int(time/self.bounding_x),lambda self = self: looper(self))
            else:
                self.finished = True
        self.bounding_x = bounding_x
        self.curr_x = bounding_x
        self.true_root.after(int(time/bounding_x),lambda self=self: looper(self))
        self.page_frame.pack_forget()
    def __init__(self, root,true_root):
        self.root = root
        self.true_root = true_root
        self.finished = False
        self.create()



