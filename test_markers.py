import pytest
from tkinter import Tk, StringVar, Frame
from lib import markers

@pytest.fixture
def mock_app_fixture():
    class mockAppDisplay:
        def __init__(self):
            self.marker_icons = {}
    # Create a tk window
    root = Tk()
    # Generate an instance of our mockAppDisplay class, which contains marker icons.
    mock_app = mockAppDisplay()
    yield root, mock_app
    # Teardown
    root.destroy()

# Intended behaviour: Marker type can be selected properly, and all markers should exist in marker_icons
def test_create_marker_type_selector_updates_marker_var(mock_app_fixture):
    root, mock_app = mock_app_fixture
    mock_frame = Frame(root)
    mock_frame.pack()

    mock_marker = StringVar()
    markers.create_marker_type_selector(mock_app, mock_frame, mock_marker, 'white')

    # For loop that sets the marker to the corresponding marker type, then asserts it matches
    for mtype in ['light', 'mild', 'severe', 'dangerous']:
        mock_marker.set(mtype)

        # assert
        assert mock_marker.get() == mtype

    # All four marker types should exist in marker_icons
    assert all(mt in mock_app.marker_icons for mt in ['light', 'mild', 'severe', 'dangerous'])