import os
from importlib import import_module as m_import
from config import config


def _get_app_list():
    """Get list of available apps in specified order."""
    app_config = config["app"]

    specific_order = app_config.APPS_PRIORITY_ORDER
    list_of_apps = os.listdir(app_config.APPS_DIRECTORY)
    list_of_apps2 = specific_order.copy()

    for app in list_of_apps:
        if app not in app_config.RESTRICTED_FILES:
            app_path = os.path.join(app_config.APPS_DIRECTORY, app)
            if not os.path.isdir(app_path):
                app_name = app.strip(".py")
                if app_name not in list_of_apps2:
                    list_of_apps2.append(app_name)

    return list_of_apps2


def _get_app_modules(app_list):
    """Import modules for all apps."""
    modules_of_apps = []
    for app_import in app_list:
        modules_of_apps.append(m_import(f"{config['app'].APPS_DIRECTORY}.{app_import}"))
    return modules_of_apps


# Module-level initialization (these run once when the module is imported)
_app_list = _get_app_list()
_app_modules = _get_app_modules(_app_list)


class app:
    """App loader and manager."""

    def __init__(self, page, code, root):
        self.code = code
        self.app = _app_modules[_app_list.index(code)]
        self.app.create(page, root)


def list():
    """Return list of available apps."""
    return _app_list
