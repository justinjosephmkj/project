import sqlite3
import re
from datetime import datetime

def options(userId):
    choice = 1
    while choice != 3:
        while True:
            try:
                print("****************************")
                print("Doctor's Window Menu Options")
                print("****************************")
                print("1. Add Prescription")
                print("2. View Appointments")
                print("3. Logout")
                choice = int(input("Please select an operation (eg: 1) : "))
                break
            except:
                print("Please input a digit (eg: 1)")
        if choice > 3 or choice <= 0:
            print("Invalid choice. Please try again.")
        else:
            if choice == 1:
                addPrescription(userId)
            if choice == 2:
                viewBookings(userId)
    print("5. Logout selected")
    print("Returning to application main window.")


def addPrescription(userId):
    try:
        name = input('Name: ')
        symptoms = input('Symptoms: ')
        medicine = input('Medicines: ')
        comments = input('Comments: ')
        date = input('Date (01-12-2021): ')
        patientId = input('Patient Id: ')

        connection = sqlite3.connect("walkinclinic.db")
        cursor = connection.cursor()
        cursor.execute(
            "insert into PRESCRIPTION (NAME, SYMPTOMS, MEDICINES, COMMENTS, DOCTORID, DATE, PATIENTID) values (?,?,?,?,?,?,?)",
            (name, symptoms, medicine, comments, userId, date, patientId));
        cursor.execute("COMMIT;")
        cursor.close()
        connection.close()
        print("Patient Registration completed successfully.")
    except:
        print("An error occured, please try agian.")

def viewBookings(userId):
    print("Please enter the date to view bookings.")
    date = input("Please enter date (dd-mm-yy, eg: 28-12-2021) : ")
    regexEmail = r'\b[0-9][0-9]-[0-9][0-9]-[2][0][2-9][2-9]\b'
    if re.fullmatch(regexEmail, date):
        dt = datetime.strptime(date, '%d-%m-%Y')
        day = dt.strftime('%a').lower()
        connection = sqlite3.connect("walkinclinic.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM booking where date =? and doctor_id = ? ;", [date, userId])
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result == None:
            print("No bookings for the given date!")
        else:
            connection = sqlite3.connect("walkinclinic.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM booking where date =? and doctor_id = ? ;", [date, userId])
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            bookingIds = []
            for row in result:
                bookingIds.append(row[4])

            connection = sqlite3.connect("walkinclinic.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM slots;", [])
            booking = cursor.fetchall()
            cursor.close()
            connection.close()

            print('Appointments for the give date :')
            print('#Starting Hour #Starting Minute')
            for row in booking:
                if (row[0] in bookingIds):
                    print(row[2], ':', row[3])