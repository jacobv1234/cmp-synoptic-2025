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

def mock_map(mocker):
    # Set mockers
    mock_map = mocker.MagicMock()
    # Patch mockers
    mocker.patch("map.tkintermapview.TkinterMapView", return_value=mock_map)
    
    mocker.patch("map.tk.Frame", return_value=mocker.MagicMock())
    mocker.patch("map.Label", return_value=mocker.MagicMock())
    mocker.patch("map.Button", return_value=mocker.MagicMock())
    mocker.patch("map.draw_markers_page")
    mocker.patch("map.getMarkerCountForUser", return_value=1)
    mocker.patch("map.urlopen", return_value=io.BytesIO(b"mock_image"))
    # Mock attributes for a real image
    mocker.patch("map.Image.open", return_value=Image.new("RGBA", (64, 64)))
    mocker.patch("map.ImageTk.PhotoImage", return_value=mocker.MagicMock())

    return mock_map