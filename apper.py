import tkinter as d3
import os
from importlib import import_module as m_import


def _get_app_list():
    specific_order = ["clock", "stopwatch"]
    list_of_apps = os.listdir("apps")
    list_of_apps2 = specific_order

    for app in list_of_apps:
        if (app != "__init__.py") and (app != "__pycache__"):
            if os.path.isdir("apps/" + app) == False:
                if not (app.strip(".py")) in list_of_apps2:
                    list_of_apps2.append(app.strip(".py"))

    return list_of_apps2


def _get_app_modules(app_list):
    modules_of_apps = []
    for app_import in app_list:
        modules_of_apps.append(m_import("apps." + app_import))
    return modules_of_apps


# Module-level initialization (these run once when the module is imported)
_app_list = _get_app_list()
_app_modules = _get_app_modules(_app_list)


class app:
    def __init__(self, page, code, root):
        self.code = code
        self.app = _app_modules[_app_list.index(code)]
        self.app.create(page, root)


def list():
    return _app_list
