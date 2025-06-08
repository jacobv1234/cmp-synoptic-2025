import pytest
import mariadb
import bcrypt
from lib import databaseConnectionFront as db


@pytest.fixture
def mock_db(mocker):
    mock_cursor = mocker.MagicMock()
    mock_connection = mocker.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch("lib.databaseConnectionFront.get_connection", return_value=(mock_connection, mock_cursor))
    return mock_connection, mock_cursor

# Intended behaviour: hashed password does NOT match the entered password
def test_encrypter():
    password = "Test123"
    hashed = db.encrypter(password)

    # Asserts
    assert hashed != password.encode()
    assert bcrypt.checkpw(password.encode(), hashed)

# Intended behaviour: passowrd is hased, decoded and verified successfully
def test_verify_correct(mock_db, mocker):
    # Create mockers
    mock_user = "test"
    mock_password = "password_$64"
    # Encode password
    mock_hashed_password = bcrypt.hashpw(mock_password.encode(), bcrypt.gensalt())
    # Call fixture
    mock_connection, mock_cursor = mock_db
    #Decode password
    mock_cursor.fetchone.return_value = [mock_hashed_password.decode()]

    # Asserts
    assert db.verify(mock_user, mock_password) is True

# Intended behaviour: passowrd is hased, decoded and verified unsuccessfully
def test_verify_incorrect(mock_db, mocker):
    # Create mockers
    mock_user = "test"
    # The real password
    mock_password = "password_$64"
    # Impostor password
    mock_bad_password = "WRONGWRONGHAHAHAHAHAHAHAHAHAHHAWRONGWRONGWRONGHAHAHAHAHAHAHAHAWRONGWRONG"
    # Encode
    mock_hashed_password = bcrypt.hashpw(mock_password.encode(), bcrypt.gensalt())
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = [mock_hashed_password.decode()]

    # Asserts
    assert db.verify(mock_user, mock_bad_password) is False

# Intended behaviour: a mock user is registered successfully
def test_registerUser_success(mock_db, mocker):
    result = db.registerUser(("testuser", "hotgamerdudes@hotmail.com", "password421"))
    assert result is True

# Intended behaviour: a mock user fails to be registered
def test_registerUser_failure(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    # Raise mariadb insertion error so it doesn't throw an actual error in the console
    mock_cursor.execute.side_effect = mariadb.Error("Insert failed")
    

    result = db.registerUser(("failuser", "fail@example.com", "pass"))
    assert result is False

# Intended behaviour: mock user with the id of 11 successfully logs in
def test_logInUser(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    # patching verify so it returns true
    mocker.patch.object(db, "verify", return_value = True)
    # userID and password for verify
    mock_cursor.fetchone.return_value = (11,)
    # Call logInUser
    result = db.logInUser(("testUser", "password"))
    # Assert
    assert result == 11

# Intended behaviour: the returned current trash point value is 123
def test_getCurrentUserTP(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (123,)

    # Call getCurrentUserTP
    result = db.getCurrentUserTP("testUser")
    # Asserts
    assert result == "123"

# Intended behaviour: result matches the return_values from mock_cursor
def test_getAllShopItems(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [("500 Cigarettes",), ("10000 very angry dwarves",)]

    # Call getAllShopItems
    result = db.getAllShopItems()
    # Asserts
    assert result == ["500 Cigarettes", "10000 very angry dwarves"]

# Intended behaviour: result matches the return_values from mock_cursor
def test_getAllShopPrices(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchall.return_value = [(1,), (9999,)]

    # Call getAllShopPrices
    result = db.getAllShopPrices()
    # Asserts
    assert result == [1, 9999]

# Intended behaviour: the returned marker count is 6
def test_getMarkerCountForUser(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (6,)

    # Call getMarkerCountForUser
    result = db.getMarkerCountForUser("testUser")
    # Asserts
    assert result == 6

# Intended behaviour: subtraction is successful and result is true
def test_purchaseSubtraction_success(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (100,)

    result = db.purchaseSubtraction(99, "username")
    assert result is True

# Intended behaviour: subtraction is successful and result is false
def test_purchaseSubtraction_failure(mock_db, mocker):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (1,)

    result = db.purchaseSubtraction(50, "username")
    assert result is False


def test_getUserIcon_success(mock_db):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_icon = "icon.png"
    mock_cursor.fetchone.return_value = (mock_icon,)

    result = db.getUserIcon("testuser")
    assert result == mock_icon
    mock_cursor.execute.assert_called_once_with("SELECT userPic FROM User WHERE username = %s", ("testuser",))
    mock_cursor.close.assert_called_once()

    
def test_getUserIcon_failure(mock_db):
    # Call fixture
    mock_connection, mock_cursor = mock_db
    mock_cursor.execute.side_effect = mariadb.Error("DB error")

    result = db.getUserIcon("testuser")
    assert result == 0
    mock_cursor.close.assert_called_once()