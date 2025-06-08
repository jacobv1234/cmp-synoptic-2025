import pytest
import tkinter as tk
from lib.appdisplay import AppDisplay

@pytest.fixture
# Fixture that mocks a tkinter GUI
def display(mocker):

    # Prevent draw_front_page from executing its real logic during init
    mocker.patch("lib.appdisplay.draw_front_page")

    mocker.patch("lib.appdisplay.Tk", return_value = mocker.MagicMock(name="MockTk"))
    mocker.patch("lib.appdisplay.Frame", return_value = mocker.MagicMock(name="MockFrame"))
    mocker.patch("lib.appdisplay.Canvas", return_value = mocker.MagicMock(name="MockCanvas"))
    mocker.patch("lib.appdisplay.ImageTk.PhotoImage", return_value=mocker.MagicMock(name="MockPhotoImage"))

    # mock settings
    MockSettings={
    "language": "English",
    "theme": "Light",
    "textsize": "Normal",
    "saved_user": ""
    }

    mockDisplay = AppDisplay(settings=MockSettings)

    # Patch c with create_text and delete
    mockDisplay.c.create_text = mocker.MagicMock(name="create_text", return_value="mockTextId")
    mockDisplay.c.delete = mocker.MagicMock(name="delete")

    # default empty cobj and widgets lists
    mockDisplay.cobjects = []
    mockDisplay.widgets = []
    # mocks for widgets and cobjs
    mock_widget = mocker.MagicMock(name="mock_widget")
    display.widgets = [mock_widget]
    mock_cobj = "mock_cobj"
    display.cobjects = [mock_cobj]

    return mockDisplay

# Intended behaviour: __init__ should be setting display.running as "true"
#                     display.width and display.height should be set to 480 and 720 respectively
def test_display_init(display):
    assert display.running is True
    assert display.width == 480
    assert display.height == 720

# Intended behaviour: cobjects array should be empty
#                     widgets array should be empty
def test_clear_screen(display, mocker):
    # Call clear_screen
    display.clear_screen()
    
    # Asserts
    assert display.cobjects == []
    assert display.widgets == []

# Intended behaviour: checks that we log in with the valuelist containing an entry "helloworld"
def test_log_in_pressed(display, mocker):

    # isinstance expects an entry so we mock it
    entry_mocker = mocker.MagicMock(spec=tk.Entry)
    entry_mocker.get.return_value = "helloworld"
    display.widgets = [entry_mocker]
    
    open_map_mocker = mocker.patch("lib.appdisplay.open_map")

    # Test with loginUser set to True
    mocker_log_in = mocker.patch("lib.appdisplay.logInUser", return_value = True)

    # Call log_in_pressed
    display.log_in_pressed()

    # asserts
    mocker_log_in.assert_called_once_with(["helloworld"])
    # assert open_map is called
    open_map_mocker.assert_called_once_with(display)

# Setter function for register_test, both for success and failures
def setter_register_test(display, mocker, r):
    # Mock entries for user email and password
    entry_username_mocker = mocker.MagicMock(spec=tk.Entry)
    entry_username_mocker.get.return_value = "testusername"
    entry_email_mocker = mocker.MagicMock(spec=tk.Entry)
    entry_email_mocker.get.return_value = "test@pleasework.com"
    entry_password_mocker = mocker.MagicMock(spec=tk.Entry)
    entry_password_mocker.get.return_value = "password"
    entry_confirm_password_mocker = mocker.MagicMock(spec=tk.Entry)
    entry_confirm_password_mocker.get.return_value = "password"
    # assign entry values
    display.widgets = [entry_username_mocker, entry_email_mocker, entry_password_mocker, entry_confirm_password_mocker]

    # Set the return value of registration (true/false)
    register_mocker = mocker.patch("lib.appdisplay.registerUser", return_value = r)
    # Patch draw_front_page
    front_page_mocker  = mocker.patch.object(display, "draw_front_page")

    return display.widgets, register_mocker, front_page_mocker

# Intended behaviour: we register with "test@pleasework.com"
#                     draw_front_page is called properly
#                     a mock entry is created for "test@pleasework.com"
def test_register_pressed_true(display, mocker):
    # Call setter function
    entry_mocker, register_mocker, front_page_mocker = setter_register_test(display, mocker, True)
    
    # Call register_pressed
    display.register_pressed()

    # Asserts
    register_mocker.assert_called_once_with(["testusername","test@pleasework.com","password","password"])
    front_page_mocker.assert_called_once()

# Intended behaviour: a mock error is created in display.cobjects
def test_register_pressed_false(display, mocker):
    entry_mocker, register_mocker, front_page_mocker = setter_register_test(display, mocker, False)

    error_mocker = mocker.patch.object(display.c, "create_text", return_value = "mockError")

    # Call register_pressed
    display.register_pressed()

    ## Assert
    assert "mockError" in display.cobjects

def test_return_to_front_page(display, mocker):
    # Patch mock draw_front_page
    mock_front_page = mocker.patch.object(display, "draw_front_page")
    # mockers
    mock_map_widget = mocker.MagicMock(name="mock_map_widget")
    display.map_widget = mock_map_widget
    # Call open_shopping_page
    display.return_to_front_page()

    # Assert screen cleared
    assert display.cobjects == []
    assert display.widgets == []
    # Assert map_widget destroy called
    mock_map_widget.destroy.assert_called_once()
    # Assert draw_shopping_page called
    mock_front_page.assert_called_once()


# Intended behaviour: Shopping page drawn
def test_open_shopping_page(display, mocker):
    # Patch mock draw_shopping_page
    mock_shopping_page = mocker.patch("lib.appdisplay.draw_shopping_page")
    # Call open_shopping_page
    display.open_shopping_page()
    # Assert clearing screen worked
    assert display.cobjects == []
    assert display.widgets == []
    # Assert draw_shopping_page called
    mock_shopping_page.assert_called_once_with(display)

# Intended behaviour: Markers page drawn
def test_open_markers_page(display, mocker):
    # Patch mock draw_markers_page
    mock_markers_page = mocker.patch("lib.appdisplay.draw_markers_page")
    # Call open_markers_page
    display.open_markers_page()
    # Assert clearing screen worked
    assert display.cobjects == []
    assert display.widgets == []
    # Assert draw_markers_page called
    mock_markers_page.assert_called_once_with(display)

# Intended behaviour: update is called once
def test_update(display, mocker):
    # Mock a window
    mock_window = mocker.MagicMock()
    # Set window to mock
    display.window = mock_window
    # Call update
    display.update()

    mock_window.update.assert_called_once()