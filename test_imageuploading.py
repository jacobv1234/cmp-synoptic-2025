import pytest
import io
from lib import imageuploading as iu
from PIL import Image

# Intended behaviour: result equals the mock_uploads return value, mock_upload is called once
def test_upload_image(mocker):
    # Set mockers
    mock_upload = mocker.patch("lib.imageuploading.cloudinary.uploader.upload")
    mock_upload.return_value = {"secure_url": "https://i.imgur.com/GYk2RfJ.jpeg"}

    mock_filename = "test/image.jpg"

    # Call upload_image
    result = iu.upload_image(mock_filename)

    mock_fileID = mock_filename.replace('/', '_').replace('\\', '_').replace('.', '_')

    # Asserts
    assert result == "https://i.imgur.com/GYk2RfJ.jpeg"
    mock_upload.assert_called_once_with(mock_filename, public_id=mock_fileID)

# Intended behaviour: result is an image, result size matches mock_img size, mock_get is called once
def test_download_image(mocker):
    # Set mockers
    mock_get = mocker.patch("lib.imageuploading.requests.get")
    mock_image_bytes = io.BytesIO()

    # Mock an image
    mock_img = Image.new("RGB", (64, 64), color="yellow")
    mock_img.save(mock_image_bytes, format="PNG")
    mock_image_bytes.seek(0)

    # Mock the response from requests.get
    mock_response = mocker.MagicMock()
    mock_response.content = mock_image_bytes.getvalue()
    mock_get.return_value = mock_response

    # Call download_image
    result = iu.download_image("https://example.com/fakeimage.png")

    # Asserts
    assert isinstance(result, Image.Image)
    assert result.size == (64, 64)
    mock_get.assert_called_once_with("https://example.com/fakeimage.png")