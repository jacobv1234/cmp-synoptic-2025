# Module Imports
import mariadb
import sys
import bcrypt as bcrypt

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="jacobvuk_synoptic",
        password="Fy,tEvM0wmx[",
        host="jacobv123.uk",
        port=3306,
        database="jacobvuk_waste_collector"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

def displayDBData():
    cur.execute("SELECT * FROM testTable")
    rows = cur.fetchall()
    finalString = "\n".join(map(str, rows)) #Map turns each row to str and join a new line for each one
    return finalString  #We then return the SELECTED rows to display

def encrypter(password):
        salt = bcrypt.gensalt()
        encryptedPassword = bcrypt.hashpw(password.encode("utf-8"), salt)
        return encryptedPassword

def verify(username, password):
    userData = (username,)
    print(userData[0])
    dbEncryptPWGet = "SELECT password FROM User WHERE username = %s"
    print (type(dbEncryptPWGet))
    print(type(userData[0]))
    cur.execute(dbEncryptPWGet, userData)
    getEncryptedPassword = cur.fetchone()
    print(dbEncryptPWGet)
    print(getEncryptedPassword)

    return bcrypt.checkpw(password.encode("utf-8"), getEncryptedPassword[0].encode("utf-8"))


def registerUser(regData):
    try:
        regData = (regData[0], regData[1], encrypter(regData[2]), None)
        dbRegInsert = "INSERT INTO User (username, email, password, userPic) VALUES (%s, %s, %s, %s)"
        cur.execute(dbRegInsert, regData) #Need to keep data and Sql seperete to avoid sql injections
        conn.commit()
        return True
        
    except mariadb.Error as e:
        print({e})
        return False
    
    finally:
        cur.close()

def logInUser(loginData):
    try:
        print("here")
        loginCheck = verify(loginData[0], loginData[1])
        if loginCheck:
            return True
    
    except mariadb.Error as e:
        print({e})
        return False

    finally:
        cur.close()
    

