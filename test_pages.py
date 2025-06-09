import pytest
from tkinter import Tk
from lib.pages import draw_front_page, draw_register_page

@pytest.fixture
def mock_app(mocker):
    class MockApp:
        def __init__(self):
            self.window = Tk()
            self.width = 480
            self.height = 720
            self.images = {}
            self.widgets = []
            self.cobjects = []
            self.settings = {
                "language": "English",
                "theme": "Light",
                "textsize": "Normal",
                "saved_user": "test"
            }
            self.c = mocker.MagicMock()
            self.clear_screen = mocker.MagicMock()
            self.log_in_pressed = mocker.MagicMock()
            self.draw_register_page = mocker.MagicMock()
            self.register_pressed = mocker.MagicMock()
            self.draw_front_page = mocker.MagicMock()
    return MockApp()

# Intended behaviour: length of widgets and cobjects tuples are correct, clear screen is called once
def test_draw_front_page(mock_app):
    # Call draw_front_page
    draw_front_page(mock_app)
    mock_entry = mock_app.widgets[0]

    # Asserts
    mock_app.clear_screen.assert_called_once()
    assert len(mock_app.widgets) == 4  # 2 entries + 2 buttons
    assert len(mock_app.cobjects) == 3  # 1 image + 2 texts

    # Check saved username is set in entry
    assert mock_entry.get() == "test"

# Intended behaviour: length of widgets and cobjects tuples are correct, clear screen is called once
def test_draw_register_page(mock_app):
    # Call draw_register_page
    draw_register_page(mock_app)

    # Asserts
    mock_app.clear_screen.assert_called_once()
    assert len(mock_app.widgets) == 6   # 4 entries + 2 buttons
    assert len(mock_app.cobjects) == 5  # 1 image + 4 text labels