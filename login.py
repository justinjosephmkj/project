import sqlite3
import re

def login():
    username = input("Please enter your email id : ")
    regexEmail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regexEmail, username)):
        password = input("Please enter your password : ")
        connection = sqlite3.connect("walkinclinic.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users where username = ? and password = ?;", [username, password])
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if row == None:
            print("User not found!")
            return False
        else:
            return row
    else:
        print("Invalid email id!")