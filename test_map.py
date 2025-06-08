import pytest
import tkinter as tk
import io
from PIL import Image

@pytest.fixture
def mock_display(mocker):
    display = mocker.MagicMock()
    display.settings = {
    "language": "English",
    "theme": "Light",
    "textsize": "Normal",
    "saved_user": ""
}
    display.window = mocker.MagicMock()
    display.width = 480
    display.height = 720
    display.widgets = []
    display.user_id = 21
    display.clear_screen = mocker.MagicMock()
    display.return_to_front_page = mocker.MagicMock()
    display.open_shopping_page = mocker.MagicMock()
    display.open_settings_page = mocker.MagicMock()
    return display
