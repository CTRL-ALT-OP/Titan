import tkinter as d3
import os
from importlib import import_module as m_import

specific_order = ["clock","stopwatch"]
list_of_apps = os.listdir("apps")
list_of_apps2 = specific_order
print(list_of_apps)
for app in list_of_apps:
    i = list_of_apps.index(app)
    if (list_of_apps[i] != "__init__.py") and (list_of_apps[i] != '__pycache__'):
        if os.path.isdir("apps/"+list_of_apps[i]) == False:
            if not (list_of_apps[i].strip(".py")) in list_of_apps2:
                list_of_apps2.append(list_of_apps[i].strip(".py"))
print(list_of_apps2)
modules_of_apps = []
for app_import in list_of_apps2:
    modules_of_apps.append(m_import("apps."+app_import))

class app():
    def __init__(self, page, code, root):
        self.code = code
        self.app = modules_of_apps[list_of_apps2.index(code)]
        self.app.create(page, root)
 










def list():
    return list_of_apps2
