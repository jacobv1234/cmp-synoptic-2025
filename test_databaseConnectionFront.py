import pytest
import bcrypt
from lib import databaseConnectionFront as db

def test_encrypter():
    password = "Test123"
    hashed = db.encrypter(password)

    # Asserts
    assert hashed != password.encode()
    assert bcrypt.checkpw(password.encode(), hashed)
