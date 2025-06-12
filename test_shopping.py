import pytest
import tkinter as tk
from lib import shopping

@pytest.fixture
def mock_self(mocker):
    root = tk.Tk()
    mock_obj = mocker.MagicMock()
    mock_obj.window = mocker.MagicMock()
    mock_obj.images = {}
    mock_obj.widgets = []
    mock_obj.width = 480
    mock_obj.height = 720
    mock_obj.open_map = mocker.MagicMock()
    mock_obj.getChecked = mocker.MagicMock()
    yield root, mock_obj
    # Teardown tk window
    root.destroy()

# Intended behaviour: widgets > 5
#                     DB getter functions are called once
#                     DB getters match the assert statements
#                     Coin and trolley images are present
def test_draw_shopping_page(mocker, mock_self):
    root, mock_self = mock_self
    # Mockers
    mock_appdisplay = mocker.patch('lib.appdisplay.AppDisplay.username', 'test')
    mock_getCurrentUserTP = mocker.patch('lib.shopping.getCurrentUserTP', return_value=123)
    mock_getAllShopItems = mocker.patch('lib.shopping.getAllShopItems', return_value=["Kilju", "Tobacco"])
    mock_getAllShopPrices = mocker.patch('lib.shopping.getAllShopPrices', return_value=[1, 999])

    # Mock image bytes
    mock_image_bytes = b"mockbytes"
    mock_urlopen = mocker.patch('lib.shopping.urlopen')
    mock_urlopen.return_value.read.return_value = mock_image_bytes

    # Patch PIL.Image.open to return a mock image with resize method
    class MockImage:
        def resize(self, size):
            return self
    mock_image_open = mocker.patch('lib.shopping.Image.open', return_value=MockImage())

    # Patch ImageTk.PhotoImage to return a string
    mock_photoimage = mocker.patch('lib.shopping.ImageTk.PhotoImage', side_effect=lambda img: f"photoimage_{img}")

    # Mock get_connection
    mock_cursor = mocker.MagicMock()
    mock_cursor.fetchone.return_value = (b"mock_image",)
    mock_connection = mocker.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch("lib.shopping.get_connection", return_value=(mock_connection, mock_cursor))

    # Call draw_shopping_page
    shopping.draw_shopping_page(mock_self)

    # Asserts
    assert len(mock_self.widgets) > 5
    assert mock_self.currency == 123
    assert 'coin' in mock_self.images
    assert 'trolley' in mock_self.images
    assert len(mock_self.itemInfo) == 2

    for (var, mock_name, mock_price), expected_name, expected_price in zip(mock_self.itemInfo, ["Kilju", "Tobacco"], [1, 999]):
        assert mock_name == expected_name
        assert mock_price == expected_price

    # DB function asserts
    mock_getCurrentUserTP.assert_called_once_with("test")
    mock_getAllShopItems.assert_called_once()
    mock_getAllShopPrices.assert_called_once()