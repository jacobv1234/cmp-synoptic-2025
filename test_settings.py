import pytest
import json
from lib.settings import load_settings, save_settings, apply_settings

@pytest.fixture
def sample_settings():
    return {
        "language": "English",
        "theme": "Light",
        "textsize": "Normal",
        "saved_user": "test"
    }

# Intended behaviour: sample settings are dumped into settings.json, which is then loaded as result which should match.
def test_load_settings(tmp_path, sample_settings):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps(sample_settings))

    # Call load_settings
    result = load_settings(path)
    # Asserts
    assert result == sample_settings

# Intended behaviour: settings are saved, then loaded into content, which should match sample settings
def test_save_settings(tmp_path, sample_settings):
    path = tmp_path / "settings.json"
    # Call save_settings
    save_settings(sample_settings, path)

    # Read the json
    content = json.loads(path.read_text())
    # Asserts
    assert content == sample_settings

# Intended behaviour: canvas configure called once with the applied background (white)
#                     open_map and save_settings called once
#                     mock_self settings match the applied settings
def test_apply_settings(mocker, sample_settings):
    mock_self = mocker.MagicMock()
    mock_self.language.get.return_value = "Tahitian"
    mock_self.theme.get.return_value = "Light"
    mock_self.textsize.get.return_value = "Large"
    mock_self.settings = {"saved_user": "test"}
    mock_self.c = mocker.MagicMock()

    # Mock the saved settings
    mock_save_settings = mocker.MagicMock()
    mocker.patch("lib.settings.save_settings", mock_save_settings)
    # Call apply settings
    apply_settings(mock_self)

    # Asserts
    assert mock_self.settings["language"] == "Tahitian"
    assert mock_self.settings["theme"] == "Light"
    assert mock_self.settings["textsize"] == "Large"
    assert mock_self.settings["saved_user"] == "test"
    
    mock_self.c.configure.assert_called_once_with(bg='white')
    mock_self.open_map.assert_called_once()
    mock_save_settings.assert_called_once_with(mock_self.settings)