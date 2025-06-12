# Module Imports
import mariadb
import sys
import bcrypt as bcrypt
from PIL import Image, ImageTk
from io import BytesIO

def get_connection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="jacobvuk_synoptic",
            password="Fy,tEvM0wmx[",
            host="jacobv123.uk",
            port=3306,
            database="jacobvuk_waste_collector"

        )

        return conn, conn.cursor()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)



def displayDBData():
    # Get Cursor
    conn, cur = get_connection()
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
    # Get Cursor
    conn, cur = get_connection()
    cur.execute(dbEncryptPWGet, userData)
    getEncryptedPassword = cur.fetchone()
    print(dbEncryptPWGet)
    print(getEncryptedPassword)

    return bcrypt.checkpw(password.encode("utf-8"), getEncryptedPassword[0].encode("utf-8"))


def registerUser(regData):
    # Get Cursor
    conn, cur = get_connection()
    try:
        userProfilePicture = Image.open("images/cleanmeakat.png")
        defaultPicture = BytesIO()
        userProfilePicture.save(defaultPicture, format='PNG')
        #addMarkerImg = ImageTk.PhotoImage(userProfilePicture)
        regData = (regData[0], regData[1], encrypter(regData[2]), defaultPicture.getvalue())
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
    conn, cur = get_connection()
    try:
        loginCheck = verify(loginData[0], loginData[1])
        if loginCheck:
            # Fetch the user ID from the database
            cur.execute("SELECT userID FROM User WHERE username = %s", (loginData[0],))
            result = cur.fetchone()
            if result:
                return result[0]  # Return the userID (integer)
            else:
                return False
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        cur.close()

def getCurrentUserTP(username):
    conn, cur = get_connection()
    try:
        getTPData = (username,)
        getTPSelect = "SELECT userTrashPoints FROM User WHERE username = %s"
        cur.execute(getTPSelect, getTPData) #Need to keep data and Sql seperete to avoid sql injections
        getTP = cur.fetchone()
        return str(getTP[0])
        
    except mariadb.Error as e:
        print({e})
        return False
    
    finally:
        cur.close()

def getAllShopItems():
    conn, cur = get_connection()
    shopItemList = []
    try:
        #UPLOAD PROFILE PICTURE BINARY TO DATABASE
        # userProfilePicture = Image.open("images/cleanmeakatSpecialGold.png")
        # defaultPicture = BytesIO()
        # userProfilePicture.save(defaultPicture, format='PNG')
        # regData = (defaultPicture.getvalue(),)
        # dbRegInsert = "UPDATE pointShop SET itemPic = %s WHERE itemName = 'CleanMEerkat GOLD' "
        # cur.execute(dbRegInsert, regData) 
        # conn.commit()
        getAllItems = "SELECT itemName FROM pointShop"
        cur.execute(getAllItems) #Need to keep data and Sql seperete to avoid sql injections
        getItemList = cur.fetchall()
        for tupleItem in getItemList:
            for shopItem in tupleItem:
                shopItemList.append(shopItem)
        return shopItemList
        
    except mariadb.Error as e:
        print({e})
        return []
    
    finally:
        cur.close()

def getAllShopPrices():
    conn, cur = get_connection()
    priceItemList = []
    try:
        getAllItems = "SELECT itemPrice FROM pointShop"
        cur.execute(getAllItems) #Need to keep data and Sql seperete to avoid sql injections
        getPriceList = cur.fetchall()
        for tuplePrice in getPriceList:
            for shopPrice in tuplePrice:
                priceItemList.append(shopPrice)
        return priceItemList
        
    except mariadb.Error as e:
        print({e})
        return []
    
    finally:
        cur.close()

def getMarkerCountForUser(user_id):
    conn, cur = get_connection()
    try:
        query = """
            SELECT COUNT(*) FROM userGarbage
            WHERE userID1 = %s AND (garbageStatus IS NULL OR garbageStatus != 'Cleaned')
        """
        cur.execute(query, (user_id,))
        count = cur.fetchone()[0]
        return count
    except Exception as e:
        print(e)
        return 0
    finally:
        cur.close()


def purchaseSubtraction(totalShopSum, username, itemsSelected):
    conn, cur = get_connection()
    try:
        data = (username,)
        query = "SELECT userTrashPoints FROM User WHERE username = %s"
        cur.execute(query, data)
        userTP = cur.fetchone()[0]
        print(userTP)
        
        newTP = (userTP-totalShopSum)
        if newTP <0:
            return False
        itemIDList = []
        for item in itemsSelected:
            print (f"Item Name: {item}")
            getItemIDS = "SELECT itemID FROM pointShop WHERE itemName = %s"
            cur.execute(getItemIDS, (item,))
            itemID = cur.fetchone()[0]
            itemIDList.append(itemID)
        for i in itemIDList:
            print(f"item ID: {i}")
            addItemData = ((i), username)
            addItemQuery = "INSERT INTO userItems (itemID, username) VALUES (%s, %s)"
            cur.execute(addItemQuery, addItemData)
        updateData = (newTP, str(username))
        print(f"new tp = {newTP} username = {str(username)}")
        updateQuery = "UPDATE User SET userTrashPoints = %s WHERE username = %s"
        cur.execute(updateQuery, updateData)
        conn.commit()
        return True
    
    except mariadb.Error as e:
        print(e.errno)
        if e.errno == 1062:
            return "Has"
        return 0
    finally:
        cur.close()

def getUserIcon(username):
    conn, cur = get_connection()
    try:
        data = (username,)
        query = "SELECT userPic FROM User WHERE username = %s"
        cur.execute(query, data)
        userPic = cur.fetchone()[0]
        conn.commit()
        return userPic

    
    except Exception as e:
        print(e)
        return 0
    finally:
        cur.close()

def getUserTrashFound(username):
    conn, cur = get_connection()
    try:
        data = (username,)
        query = "SELECT trashFound FROM User WHERE username = %s"
        cur.execute(query, data)
        userTrashFound = cur.fetchone()[0]
        conn.commit()
        return userTrashFound

    
    except Exception as e:
        print(e)
        return 0
    finally:
        cur.close()

def getUserCleaned(username):
    conn, cur = get_connection()
    try:
        data = (username,)
        query = "SELECT trashCleaned FROM User WHERE username = %s"
        cur.execute(query, data)
        userTrashCleaned = cur.fetchone()[0]
        conn.commit()
        return userTrashCleaned

    
    except Exception as e:
        print(e)
        return 0
    finally:
        cur.close()

def getAllUserPfps(username):
    conn, cur = get_connection()
    picIDList = []
    try:
        data = (username,)
        query = "SELECT itemID FROM userItems WHERE username = %s"
        cur.execute(query, data)
        userPicIDs = cur.fetchall()
        conn.commit()
        for i in userPicIDs:
            for j in i:
                picIDList.append(j)
        itemPicNamesList = []
        for itemID in picIDList:
            data = (itemID,)
            query = "SELECT itemName FROM pointShop WHERE itemID = %s"
            cur.execute(query, data)
            itemPicName = cur.fetchone()[0]
            itemPicNamesList.append(itemPicName)
        return itemPicNamesList

    
    except Exception as e:
        print(e)
        return 0
    finally:
        cur.close()

def updateProfilePicture(selectedPfpName, username):
    conn, cur = get_connection()
    try:
        print(selectedPfpName)
        data = (selectedPfpName,)
        query = "SELECT itemPic FROM pointShop WHERE itemName = %s"
        cur.execute(query, data)
        userPicBinary = cur.fetchone()[0]
        updateUserPfpData = (userPicBinary, username)
        updateUserPfpQuery = "UPDATE User SET userPic = %s WHERE username = %s"
        cur.execute(updateUserPfpQuery, updateUserPfpData)
        conn.commit()
        return True

    
    except Exception as e:
        userProfilePicture = Image.open("images/cleanmeakat.png")
        defaultPicture = BytesIO()
        userProfilePicture.save(defaultPicture, format='PNG')
        updateUserPfpData = (defaultPicture.getvalue(), username)
        updateUserPfpQuery = "UPDATE User SET userPic = %s WHERE username = %s"
        cur.execute(updateUserPfpQuery, updateUserPfpData)
        conn.commit()

        return 0
    finally:
        cur.close()

def getUsername(userID):
    conn, cur = get_connection()
    try:
        data = (userID,)
        getAllItems = "SELECT username FROM User WHERE userID = %s"
        cur.execute(getAllItems, data) #Need to keep data and Sql seperete to avoid sql injections
        getUsername = cur.fetchone()[0]
        return getUsername
        
    except mariadb.Error as e:
        print({e})
        return []
    
    finally:
        cur.close()