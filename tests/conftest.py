import pytest
import sys


import mock_tk


# Create a pytest fixture that patches tkinter
@pytest.fixture(autouse=True)
def mock_tkinter(monkeypatch):
    """Mock tkinter for all tests."""
    monkeypatch.setitem(sys.modules, "tkinter", mock_tk)
    monkeypatch.setitem(
        sys.modules, "d3", mock_tk
    )  # For de333r.py which uses d3 as alias
    return mock_tk


@pytest.fixture
def config():
    """Fixture to load configuration."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("config", "/titan/config.py")
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)

    return config_module.config
