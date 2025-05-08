import de333r as titan
import apper
from time import sleep
global list_apps
list_apps = apper.list()

global current_page
current_page = 0

global loaded_page
global loaded_app

def switch(direction):
    global list_apps
    global current_page
    global loaded_page
    global loaded_app
    global root
    global bg_root
    
    global switch_l
    global switch_r
    if ((current_page != len(list_apps)-1) and (direction == 1)) or ((current_page != 0) and (direction == -1)):
        switch_l.configure(state='disabled')
        switch_r.configure(state='disabled')
        next_page = titan.page(bg_root,root)
        app = list_apps[current_page + direction]
        next_app = apper.app(next_page, app, root)

        loaded_page.tween(next_page, 300 ,direction=direction)
        def _(next_app, next_page):
            global loaded_page
            global current_page
            global loaded_app
            global switch_l
            global switch_r
            if loaded_page.finished == True:
                current_page += direction
                loaded_app.app.destroy(loaded_page, root)
                loaded_page = next_page
                loaded_app = next_app
                switch_l.configure(state='normal')
                switch_r.configure(state='normal')
            else:
                root.after(20, lambda page = next_page, app = next_app: _(app, page))
        root.after(20, lambda page = next_page, app = next_app: _(app,page))
    elif ((current_page == len(list_apps)-1) and (direction == 1)):
        switch_l.configure(state='disabled')
        switch_r.configure(state='disabled')
        next_page = titan.page(bg_root,root)
        app = list_apps[0]
        next_app = apper.app(next_page, app, root)

        loaded_page.tween(next_page, 300 ,direction=direction)
        def _(next_app, next_page):
            global loaded_page
            global current_page
            global loaded_app
            global switch_l
            global switch_r
            if loaded_page.finished == True:
                current_page = 0
                loaded_app.app.destroy(loaded_page, root)
                loaded_page = next_page
                loaded_app = next_app
                switch_l.configure(state='normal')
                switch_r.configure(state='normal')
            else:
                root.after(20, lambda page = next_page, app = next_app: _(app, page))
        root.after(20, lambda page = next_page, app = next_app: _(app,page))
    elif ((current_page == 0) and (direction == -1)):
        switch_l.configure(state='disabled')
        switch_r.configure(state='disabled')
        next_page = titan.page(bg_root,root)
        app = list_apps[len(list_apps)-1]
        next_app = apper.app(next_page, app, root)

        loaded_page.tween(next_page, 300 ,direction=direction)
        def _(next_app, next_page):
            global loaded_page
            global current_page
            global loaded_app
            global switch_l
            global switch_r
            if loaded_page.finished == True:
                current_page = len(list_apps)-1
                loaded_app.app.destroy(loaded_page, root)
                loaded_page = next_page
                loaded_app = next_app
                switch_l.configure(state='normal')
                switch_r.configure(state='normal')
            else:
                root.after(20, lambda page = next_page, app = next_app: _(app, page))
        root.after(20, lambda page = next_page, app = next_app: _(app,page))
        

global root
global bg_root
global switch_l
global switch_r
root, bg_root, switch_l, switch_r = titan.main.create()

switch_l.configure(command = lambda direction=-1: switch(direction))
switch_r.configure(command = lambda direction=1: switch(direction))

loaded_page = titan.page(bg_root,root)
loaded_app = apper.app(loaded_page, list_apps[0], root)

loaded_page.page_frame.pack()



root.mainloop()
