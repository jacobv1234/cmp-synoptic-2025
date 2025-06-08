import pytest
import tkinter as tk
import io
from PIL import Image
from lib.map import open_map

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

def set_mock_map(mocker):
    # Set mockers
    mock_map = mocker.MagicMock()
    # Patch mockers
    mocker.patch("lib.map.tkintermapview.TkinterMapView", return_value=mock_map)

    mocker.patch("lib.map.tk.Frame", return_value=mocker.MagicMock())
    mocker.patch("lib.map.Label", return_value=mocker.MagicMock())
    mocker.patch("lib.map.Button", return_value=mocker.MagicMock())
    mocker.patch("lib.map.draw_markers_page")
    mocker.patch("lib.map.getMarkerCountForUser", return_value=1)
    mocker.patch("lib.map.urlopen", return_value=io.BytesIO(b"mock_image"))
    # Mock attributes for a real image
    mocker.patch("lib.map.Image.open", return_value=Image.new("RGBA", (64, 64)))
    mocker.patch("lib.map.ImageTk.PhotoImage", return_value=mocker.MagicMock())

    return mock_map

# Generic unit test for open_map
# Intended behaviour: position, zoom, and marker are set appropriately
#                     display.widgets > 0
def test_open(mock_display, mocker):
    # Set mock map
    mock_map = set_mock_map(mocker)
    # Call open map
    open_map(mock_display)

    # Asserts
    mock_map.set_position.assert_called_once_with(-26.2041, 28.0473)
    mock_map.set_zoom.assert_called_once_with(13)
    mock_map.set_marker.assert_called_once_with(-26.2041, 28.0473)

    # Check widgets added
    assert len(mock_display.widgets) > 0

# Intended behaviour: when theme is Dark, label background colour should change to #2A2A2E
def test_dark_theme(mock_display, mocker):
    # Set mock map
    set_mock_map(mocker)
    # set theme to dark
    mock_display.settings["theme"] = "Dark"
    mock_label = mocker.patch("lib.map.Label", return_value=mocker.MagicMock())

    # call open_map
    open_map(mock_display)

    # Unpack arguments for mock_label, we only care about background colour though
    _, kwargs = mock_label.call_args
    # Asserts
    assert kwargs["bg"] == "#2A2A2E"

def test_getMarkerCountForUser(mock_display, mocker):
    set_mock_map(mocker)
    get_count_mock = mocker.patch("lib.map.getMarkerCountForUser", return_value=10)

    # call open_map
    open_map(mock_display)

    # Asserts
    get_count_mock.assert_called_once_with(mock_display.user_id)