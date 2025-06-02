from lib.appdisplay import AppDisplay
import pytest
import tkinter as tk

@pytest.fixture
# Fixture that mocks a tkinterface window.
def display(mocker):
    mocker.patch("tkinter.Tk")
    mocker.patch("tkinter.Frame")
    mocker.patch("tkinter.Canvas")

    return AppDisplay()

# Intended behaviour: __init__ should be setting display.running as "true"
#                     display.width and display.height should be set to 480 and 720 respectively
def test_display_init(display):
    assert display.running is True
    assert display.width == 480
    assert display.height == 720
    
class DummyWidget:

    def __init__(self):
        self.destroy_called = False
    def destroy(self):
        self.destroy_called = True

    def test_clear_screen():
        from lib.appdisplay import AppDisplay

        app_display = AppDisplay()

        # Add dummy widgets with a destroy method
        widget1 = DummyWidget()
        widget2 = DummyWidget()
        app_display.widgets.append(widget1)
        app_display.cobjects.append(widget2)

        app_display.clear_screen()

        # Assert that .destroy() was called
        assert widget1.destroy_called
        assert widget2.destroy_called
        assert len(app_display.cobjects) == 0
        assert len(app_display.widgets) == 0
