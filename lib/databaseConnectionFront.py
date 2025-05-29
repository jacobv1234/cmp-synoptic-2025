# Module Imports
import mariadb
import sys

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

