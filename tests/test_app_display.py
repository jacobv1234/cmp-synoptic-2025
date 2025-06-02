import pytest
from lib.appdisplay import AppDisplay

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

# Intended behaviour: cobjects array should be empty
#                     widgets array should be empty
def test_clear_screen(display, mocker):
    # Set additional mockers
    mock_cobj = mocker.Mock()
    mock_widget =  mocker.Mock()
    # Append arrays with mock objects
    display.cobjects = [mock_cobj]
    display.widgets = [mock_widget]

    # Call clear_screen
    display.clear_screen()
    
    # Asserts
    assert display.cobjects == []
    assert display.widgets == []

# Intended behaviour: checks that we log in with the valuelist containing an entry "helloworld"
def test_log_in_pressed(display, mocker):

    # Set additional mockers

    # isinstance expects an entry so we mock it
    entry_mocker = mocker.Mock(spec=tk.Entry)
    entry_mocker.get.return_value = "helloworld"
    display.widgets = [entry_mocker]
    mocker.patch("lib.appdisplay.open_map")

    # Test with loginUser set to True
    mocker_log_in = mocker.patch("lib.appdisplay.logInUser", return_value = True)

    # Call log_in_pressed
    display.log_in_pressed()

    # asserts
    mocker_log_in.assert_called_once_with(["helloworld"])

# Setter function for register_test, both for success and failures
def setter_register_test(display, mocker, r):
    # Mock entry
    entry_mocker = mocker.Mock(spec=tk.Entry)
    entry_mocker.get.return_value = "test@pleasework.com"
    display.widgets = [entry_mocker]

    # Set the return value of registration (true/false)
    register_mocker = mocker.patch("lib.databaseConnectionFront.registerUser", return_value = r)
    # Patch draw_front_page
    front_page_mocker  = mocker.patch.object(display, "draw_front_page")

    return entry_mocker, register_mocker, front_page_mocker

# Intended behaviour: we register with "test@pleasework.com"
#                     draw_front_page is called properly
#                     a mock entry is created for "test@pleasework.com"
def test_register_pressed_true(display, mocker):
    # Call setter function
    entry_mocker, register_mocker, front_page_mocker = setter_register_test(display, mocker, True)
    
    # Call register_pressed
    display.register_pressed()

    # Asserts
    register_mocker.assert_called_once_with(["test@pleasework.com"])
    front_page_mocker.assert_called_once()
    entry_mocker.insert.assert_called_once_with(0, "test@pleasework.com")

# Intended behaviour: a mock error is created in display.cobjects
def test_register_pressed_false(display, mocker):
    entry_mocker, register_mocker, front_page_mocker = setter_register_test(display, mocker, False)

    error_mocker = mocker.patch.object(display.c, "create_text", return_value = "mockError")

    # Call register_pressed
    display.register_pressed()

    ## Assert
    assert "mockError" in display.cobjects